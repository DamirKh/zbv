import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import pandas as pd

from dfgui.dfgui import DataframePanel, ColumnSelectionPanel, FilterPanel, HistogramPlot, ScatterPlot

matplotlib.use('WXAgg')


class TimedataPlot(wx.Panel):
    """
    Panel providing a simple time/data plot.
    """

    def __init__(self, parent, df, *args, **kwargs):
        """

        :type df: pd.DataFrame
        """
        assert isinstance(df, pd.DataFrame)
        self.df = df
        self.selected_tags = []
        self._selection_indexes = []
        wx.Panel.__init__(self, parent, *args, **kwargs)

        columns = list(df.columns)
        self.columns = columns
        # self.df_list_ctrl = df_list_ctrl

        self.figure = Figure(facecolor="white", figsize=(1, 1))
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        chart_toolbar = NavigationToolbar2Wx(self.canvas)

        self.button_openchoice_dlg = wx.Button(self, label="Select columns")
        self.Bind(wx.EVT_BUTTON, self.on_button_openchoice_dlg)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(self.button_openchoice_dlg, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        # row_sizer.Add(self.combo_box2, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        row_sizer.Add(chart_toolbar, 0, wx.ALL, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, flag=wx.EXPAND, border=5)
        sizer.Add(row_sizer)
        self.SetSizer(sizer)

    def on_button_openchoice_dlg(self, event):
        with wx.MultiChoiceDialog(self, message="Select tags to show", caption='Select', choices=self.columns,
                                  style=wx.CHOICEDLG_STYLE, pos=wx.DefaultPosition) as choice_dlg:
            assert isinstance(choice_dlg, wx.MultiChoiceDialog)
            choice_dlg.SetSelections(self._selection_indexes)
            if choice_dlg.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            print("User selected tags to show")
            #
            # [list_of_items[e] for e in list_of_indexes]
            self._selection_indexes = choice_dlg.GetSelections()
            self.selected_tags = [self.columns[e] for e in self._selection_indexes]
            print(self.selected_tags)
            self.redraw()

    def redraw(self):
        df = self.df
        self.axes.clear()
        for tag in self.selected_tags:
            dot = '-'
            duty_ratio = df[tag].count() / len(df)
            print('%f density for %s' % (duty_ratio, tag))
            if duty_ratio < 0.3:
                dot = '*'
            elif duty_ratio < 0.5:
                dot = 'o'
            elif duty_ratio < 0.7:
                dot = '.'
            self.axes.plot(df.index.values, df[tag].values, dot, clip_on=True)

        self.canvas.draw()


class MainFrame(wx.Frame):
    """
    GUI window for data view.
    """

    def __init__(self, df):
        wx.Frame.__init__(self, None, -1, "Data view")

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)
        self.nb = nb

        columns = df.columns[:]

        self.CreateStatusBar(2, style=0)
        self.SetStatusWidths([200, -1])

        # create the page windows as children of the notebook
        self.page0 = TimedataPlot(nb, df)
        self.page1 = DataframePanel(nb, df, self.status_bar_callback)
        self.page2 = ColumnSelectionPanel(nb, columns, self.page1.df_list_ctrl)
        self.page3 = FilterPanel(nb, columns, self.page1.df_list_ctrl, self.selection_change_callback)
        self.page4 = HistogramPlot(nb, columns, self.page1.df_list_ctrl)
        self.page5 = ScatterPlot(nb, columns, self.page1.df_list_ctrl)

        # add the pages to the notebook with the label to show on the tab
        # nb.AddPage(self.page1, "Data Frame")
        # nb.AddPage(self.page2, "Columns")
        # nb.AddPage(self.page3, "Filters")
        nb.AddPage(self.page0, "Time")
        nb.AddPage(self.page4, "Histogram")
        nb.AddPage(self.page5, "Scatter Plot")

        nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_change)

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        self.SetSize((800, 600))
        self.Center()

    def on_tab_change(self, event):
        self.page2.list_box.SetFocus()
        page_to_select = event.GetSelection()
        wx.CallAfter(self.fix_focus, page_to_select)
        event.Skip(True)

    def fix_focus(self, page_to_select):
        page = self.nb.GetPage(page_to_select)
        page.SetFocus()
        if isinstance(page, DataframePanel):
            self.page1.df_list_ctrl.SetFocus()
        elif isinstance(page, ColumnSelectionPanel):
            self.page2.list_box.SetFocus()

    def status_bar_callback(self, i, new_text):
        self.SetStatusText(new_text, i)

    def selection_change_callback(self):
        self.page4.redraw()
        self.page5.redraw()

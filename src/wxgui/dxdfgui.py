import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import pandas as pd

from dfgui.dfgui import DataframePanel,  ColumnSelectionPanel, FilterPanel, HistogramPlot, ScatterPlot

matplotlib.use('WXAgg')

# class ScatterPlot(wx.Panel):
#     """
#     Panel providing a scatter plot.
#     """
#     def __init__(self, parent, df, *args, **kwargs):
#         """
#
#         :type df: pd.DataFrame
#         """
#         assert isinstance(df, pd.DataFrame)
#         self.df = df
#         wx.Panel.__init__(self, parent, *args, **kwargs)
#
#         columns_with_neutral_selection = [''] + list(df.columns)
#         # self.columns = columns
#         # self.df_list_ctrl = df_list_ctrl
#
#         self.figure = Figure(facecolor="white", figsize=(1, 1))
#         self.axes = self.figure.add_subplot(111)
#         self.canvas = FigureCanvas(self, -1, self.figure)
#
#         chart_toolbar = NavigationToolbar2Wx(self.canvas)
#
#         self.combo_box1 = wx.ComboBox(self, choices=columns_with_neutral_selection, style=wx.CB_READONLY)
#         self.combo_box2 = wx.ComboBox(self, choices=columns_with_neutral_selection, style=wx.CB_READONLY)
#
#         self.Bind(wx.EVT_COMBOBOX, self.on_combo_box_select)
#
#         row_sizer = wx.BoxSizer(wx.HORIZONTAL)
#         row_sizer.Add(self.combo_box1, 0, wx.ALL | wx.ALIGN_CENTER, 5)
#         row_sizer.Add(self.combo_box2, 0, wx.ALL | wx.ALIGN_CENTER, 5)
#         row_sizer.Add(chart_toolbar, 0, wx.ALL, 5)
#
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.canvas, 1, flag=wx.EXPAND, border=5)
#         sizer.Add(row_sizer)
#         self.SetSizer(sizer)
#
#     def on_combo_box_select(self, event):
#         self.redraw()
#
#     def redraw(self):
#         column_index1 = self.combo_box1.GetSelection()
#         column_index2 = self.combo_box2.GetSelection()
#         if column_index1 != wx.NOT_FOUND and column_index1 != 0 and \
#            column_index2 != wx.NOT_FOUND and column_index2 != 0:
#             # subtract one to remove the neutral selection index
#             column_index1 -= 1
#             column_index2 -= 1
#             df = self.df
#
#             # It looks like using pandas dataframe.plot causes something weird to
#             # crash in wx internally. Therefore we use plain axes.plot functionality.
#             # column_name1 = self.columns[column_index1]
#             # column_name2 = self.columns[column_index2]
#             # df.plot(kind='scatter', x=column_name1, y=column_name2)
#
#             if len(df) > 0:
#                 self.axes.clear()
#                 self.axes.plot(df.iloc[:, column_index1].values, df.iloc[:, column_index2].values, 'o', clip_on=False)
#
#                 self.canvas.draw()


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
        self.page1 = DataframePanel(nb, df, self.status_bar_callback)
        self.page2 = ColumnSelectionPanel(nb, columns, self.page1.df_list_ctrl)
        self.page3 = FilterPanel(nb, columns, self.page1.df_list_ctrl, self.selection_change_callback)
        self.page4 = HistogramPlot(nb, columns, self.page1.df_list_ctrl)
        self.page5 = ScatterPlot(nb, columns, self.page1.df_list_ctrl)

        # add the pages to the notebook with the label to show on the tab
        #nb.AddPage(self.page1, "Data Frame")
        #nb.AddPage(self.page2, "Columns")
        #nb.AddPage(self.page3, "Filters")
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


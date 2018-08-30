#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.2 on Fri Jun 29 19:15:36 2018
#

import wx
import wx.grid

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((733, 636))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.bitmap_button_excel_import = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/excel_imports.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_import = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/table-import-icon.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW | wx.BU_EXACTFIT)
        self.bitmap_button_load = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/inbox_upload.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_save = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/inbox_download.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_2excel = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/excel_exports.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_fillna = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/fill_color.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_downsample = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/drum.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.panel_3 = wx.Panel(self, wx.ID_ANY)
        self.bitmap_button_clear_selection = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/cell_clear.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.choice_derivative = wx.Choice(self.panel_3, wx.ID_ANY, choices=[_("choice 1")])
        self.bitmap_button_add_derivative = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/tag_blue_add.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_show_timed = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/diagramm.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW | wx.BU_EXACTFIT)
        self.bitmap_button_show = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/chart_curve.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW | wx.BU_EXACTFIT)
        self.bitmap_button_add_signal = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/vector_add.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW | wx.BU_EXACTFIT)
        self.bitmap_button_fake = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/user_clown.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW | wx.BU_EXACTFIT)
        self.bitmap_button_delete_selection = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/p/zbv/zbv/src/wxgui/glade_gui/icons/cell_delete.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.window_1 = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        self.window_1_pane_1 = wx.Panel(self.window_1, wx.ID_ANY)
        self.window_1_pane_2 = wx.Panel(self.window_1, wx.ID_ANY)
        self.label_start_time = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("--"))
        self.label_working_dir = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("--"), style=wx.ALIGN_RIGHT)
        self.label_stop_time = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("--"))
        self.label_filename = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("No data yet"), style=wx.ALIGN_RIGHT)
        self.tags_grid = wx.grid.Grid(self.window_1_pane_2, wx.ID_ANY, size=(1, 1))
        self.label_tags_selected_number = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("0"), style=wx.ALIGN_LEFT)
        self.label_hidden_dataframes = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("0"), style=wx.ALIGN_LEFT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_import_excel_btn, self.bitmap_button_excel_import)
        self.Bind(wx.EVT_BUTTON, self.on_import_btn, self.bitmap_button_import)
        self.Bind(wx.EVT_BUTTON, self.on_load_btn, self.bitmap_button_load)
        self.Bind(wx.EVT_BUTTON, self.on_save_btn, self.bitmap_button_save)
        self.Bind(wx.EVT_BUTTON, self.on_export_2excel_btn, self.bitmap_button_2excel)
        self.Bind(wx.EVT_BUTTON, self.on_fillna_btn, self.bitmap_button_fillna)
        self.Bind(wx.EVT_BUTTON, self.on_downsample_btn, self.bitmap_button_downsample)
        self.Bind(wx.EVT_BUTTON, self.on_clear_selection_btn, self.bitmap_button_clear_selection)
        self.Bind(wx.EVT_CHOICE, self.on_choice_derivative_btn, self.choice_derivative)
        self.Bind(wx.EVT_BUTTON, self.on_add_button, self.bitmap_button_add_derivative)
        self.Bind(wx.EVT_BUTTON, self.on_show_btn_old, self.bitmap_button_show_timed)
        self.Bind(wx.EVT_BUTTON, self.on_show_btn, self.bitmap_button_show)
        self.Bind(wx.EVT_BUTTON, self.on_add_signal_btn, self.bitmap_button_add_signal)
        self.Bind(wx.EVT_BUTTON, self.on_fake_btn, self.bitmap_button_fake)
        self.Bind(wx.EVT_BUTTON, self.on_delete_selection_btn, self.bitmap_button_delete_selection)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_CLICK, self.on_select_cell, self.tags_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_LABEL_LEFT_CLICK, self.on_select_cell, self.tags_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_RANGE_SELECT, self.on_select_cell, self.tags_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.on_select_cell, self.tags_grid)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("Data configurator"))
        self.bitmap_button_excel_import.SetToolTip(wx.ToolTip(_("import from excel")))
        self.bitmap_button_excel_import.SetSize(self.bitmap_button_excel_import.GetBestSize())
        self.bitmap_button_import.SetToolTip(wx.ToolTip(_("Import data")))
        self.bitmap_button_import.SetSize(self.bitmap_button_import.GetBestSize())
        self.bitmap_button_load.SetToolTip(wx.ToolTip(_("Load data")))
        self.bitmap_button_load.SetSize(self.bitmap_button_load.GetBestSize())
        self.bitmap_button_save.SetToolTip(wx.ToolTip(_("Save data")))
        self.bitmap_button_save.Enable(False)
        self.bitmap_button_save.SetSize(self.bitmap_button_save.GetBestSize())
        self.bitmap_button_2excel.SetToolTip(wx.ToolTip(_("Export to excel")))
        self.bitmap_button_2excel.Enable(False)
        self.bitmap_button_2excel.SetSize(self.bitmap_button_2excel.GetBestSize())
        self.bitmap_button_fillna.SetToolTip(wx.ToolTip(_("Fill missing data")))
        self.bitmap_button_fillna.Enable(False)
        self.bitmap_button_fillna.SetSize(self.bitmap_button_fillna.GetBestSize())
        self.bitmap_button_downsample.SetToolTip(wx.ToolTip(_("Downsample dataset")))
        self.bitmap_button_downsample.Enable(False)
        self.bitmap_button_downsample.SetSize(self.bitmap_button_downsample.GetBestSize())
        self.bitmap_button_clear_selection.SetToolTip(wx.ToolTip(_("Clear selection")))
        self.bitmap_button_clear_selection.Enable(False)
        self.bitmap_button_clear_selection.SetSize(self.bitmap_button_clear_selection.GetBestSize())
        self.choice_derivative.SetToolTip(wx.ToolTip(_("Select derivative function to add")))
        self.choice_derivative.Enable(False)
        self.bitmap_button_add_derivative.SetToolTip(wx.ToolTip(_("Add tags derived from selected")))
        self.bitmap_button_add_derivative.Enable(False)
        self.bitmap_button_add_derivative.SetSize(self.bitmap_button_add_derivative.GetBestSize())
        self.bitmap_button_show_timed.SetToolTip(wx.ToolTip(_("Show selected tags")))
        self.bitmap_button_show_timed.Enable(False)
        self.bitmap_button_show_timed.SetSize(self.bitmap_button_show_timed.GetBestSize())
        self.bitmap_button_show.SetToolTip(wx.ToolTip(_("Show selected tags")))
        self.bitmap_button_show.Enable(False)
        self.bitmap_button_show.SetSize(self.bitmap_button_show.GetBestSize())
        self.bitmap_button_add_signal.SetToolTip(wx.ToolTip(_("Generate signal")))
        self.bitmap_button_add_signal.SetSize(self.bitmap_button_add_signal.GetBestSize())
        self.bitmap_button_fake.SetToolTip(wx.ToolTip(_("Generate fake data")))
        self.bitmap_button_fake.Enable(False)
        self.bitmap_button_fake.SetSize(self.bitmap_button_fake.GetBestSize())
        self.bitmap_button_delete_selection.SetToolTip(wx.ToolTip(_("Delete selected tags")))
        self.bitmap_button_delete_selection.Enable(False)
        self.bitmap_button_delete_selection.SetSize(self.bitmap_button_delete_selection.GetBestSize())
        self.tags_grid.CreateGrid(10, 4)
        self.tags_grid.EnableEditing(0)
        self.tags_grid.SetSelectionMode(wx.grid.Grid.SelectRows)
        self.tags_grid.SetColLabelValue(0, _("TAG"))
        self.tags_grid.SetColLabelValue(1, _("MIN value"))
        self.tags_grid.SetColLabelValue(2, _("MAX value"))
        self.tags_grid.SetColLabelValue(3, _("NaN"))
        self.window_1.SetMinimumPaneSize(200)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.FlexGridSizer(0, 3, 2, 2)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.bitmap_button_excel_import, 0, 0, 0)
        sizer_2.Add(self.bitmap_button_import, 0, 0, 0)
        sizer_2.Add(self.bitmap_button_load, 0, 0, 0)
        static_line_2 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        sizer_2.Add(static_line_2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_2.Add(self.bitmap_button_save, 0, 0, 0)
        sizer_2.Add(self.bitmap_button_2excel, 0, 0, 0)
        static_line_1 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        sizer_2.Add(static_line_1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_2.Add((0, 0), 0, 0, 0)
        sizer_2.Add((20, 20), 1, 0, 0)
        sizer_2.Add(self.bitmap_button_fillna, 0, 0, 0)
        sizer_2.Add(self.bitmap_button_downsample, 0, 0, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.ALL | wx.EXPAND, 2)
        sizer_4.Add(self.bitmap_button_clear_selection, 0, 0, 0)
        sizer_4.Add(self.choice_derivative, 0, wx.EXPAND, 0)
        sizer_4.Add(self.bitmap_button_add_derivative, 0, 0, 0)
        sizer_4.Add(self.bitmap_button_show_timed, 0, 0, 0)
        sizer_4.Add(self.bitmap_button_show, 0, 0, 0)
        static_line_4 = wx.StaticLine(self.panel_3, wx.ID_ANY, style=wx.LI_VERTICAL)
        sizer_4.Add(static_line_4, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_4.Add(self.bitmap_button_add_signal, 0, 0, 0)
        sizer_4.Add(self.bitmap_button_fake, 0, 0, 0)
        sizer_4.Add((20, 20), 1, 0, 0)
        sizer_4.Add(self.bitmap_button_delete_selection, 0, 0, 0)
        self.panel_3.SetSizer(sizer_4)
        sizer_1.Add(self.panel_3, 0, wx.ALL | wx.EXPAND, 2)
        label_1 = wx.StaticText(self.window_1_pane_1, wx.ID_ANY, _("Under construction"), style=wx.ALIGN_CENTER)
        sizer_3.Add(label_1, 1, wx.ALIGN_CENTER | wx.EXPAND, 0)
        self.window_1_pane_1.SetSizer(sizer_3)
        label_3 = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("Start time:"))
        grid_sizer_2.Add(label_3, 0, 0, 0)
        grid_sizer_2.Add(self.label_start_time, 0, 0, 0)
        grid_sizer_2.Add(self.label_working_dir, 1, wx.ALIGN_RIGHT | wx.LEFT, 10)
        label_6 = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("End time:"))
        grid_sizer_2.Add(label_6, 0, 0, 0)
        grid_sizer_2.Add(self.label_stop_time, 0, 0, 0)
        grid_sizer_2.Add(self.label_filename, 1, wx.ALIGN_RIGHT | wx.LEFT, 10)
        grid_sizer_2.AddGrowableCol(2)
        sizer_5.Add(grid_sizer_2, 0, wx.EXPAND | wx.LEFT, 5)
        sizer_5.Add(self.tags_grid, 1, wx.ALL | wx.EXPAND, 1)
        label_7 = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("Tags selected:"), style=wx.ST_NO_AUTORESIZE)
        sizer_8.Add(label_7, 0, wx.RIGHT, 5)
        sizer_8.Add(self.label_tags_selected_number, 0, 0, 0)
        sizer_8.Add((50, 10), 2, wx.EXPAND, 0)
        label_8 = wx.StaticText(self.window_1_pane_2, wx.ID_ANY, _("Hidden dataframes:"), style=wx.ST_NO_AUTORESIZE)
        sizer_8.Add(label_8, 0, wx.RIGHT, 5)
        sizer_8.Add(self.label_hidden_dataframes, 0, 0, 0)
        sizer_5.Add(sizer_8, 0, 0, 0)
        self.window_1_pane_2.SetSizer(sizer_5)
        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2)
        sizer_1.Add(self.window_1, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def on_import_excel_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_import_excel_btn' not implemented!")
        event.Skip()

    def on_import_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_import_btn' not implemented!")
        event.Skip()

    def on_load_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_load_btn' not implemented!")
        event.Skip()

    def on_save_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_save_btn' not implemented!")
        event.Skip()

    def on_export_2excel_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_export_2excel_btn' not implemented!")
        event.Skip()

    def on_fillna_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_fillna_btn' not implemented!")
        event.Skip()

    def on_downsample_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_downsample_btn' not implemented!")
        event.Skip()

    def on_clear_selection_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_clear_selection_btn' not implemented!")
        event.Skip()

    def on_choice_derivative_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_choice_derivative_btn' not implemented!")
        event.Skip()

    def on_add_button(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_add_button' not implemented!")
        event.Skip()

    def on_show_btn_old(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_show_btn_old' not implemented!")
        event.Skip()

    def on_show_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_show_btn' not implemented!")
        event.Skip()

    def on_add_signal_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_add_signal_btn' not implemented!")
        event.Skip()

    def on_fake_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_fake_btn' not implemented!")
        event.Skip()

    def on_delete_selection_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_delete_selection_btn' not implemented!")
        event.Skip()

    def on_select_cell(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_select_cell' not implemented!")
        event.Skip()

# end of class MyFrame

class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_3 = wx.Panel(self, wx.ID_ANY)
        self.spin_ctrl_double_1 = wx.SpinCtrlDouble(self.panel_3, wx.ID_ANY, "0.0", min=-100000.0, max=100000.0)
        self.Cancel = wx.Button(self, wx.ID_CANCEL, "", style=wx.BU_AUTODRAW)
        self.button_1 = wx.Button(self, wx.ID_OK, "", style=wx.BU_AUTODRAW)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.Cancel)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle(_("Func parametr"))
        self.button_1.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        label_3 = wx.StaticText(self, wx.ID_ANY, _("Please, enter value of shift:"), style=wx.ALIGN_LEFT)
        sizer_4.Add(label_3, 0, wx.ALL, 5)
        sizer_6.Add(self.spin_ctrl_double_1, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        self.panel_3.SetSizer(sizer_6)
        sizer_4.Add(self.panel_3, 1, wx.EXPAND, 0)
        sizer_5.Add(self.Cancel, 0, 0, 0)
        sizer_5.Add(self.button_1, 0, 0, 0)
        sizer_4.Add(sizer_5, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL, 10)
        self.SetSizer(sizer_4)
        sizer_4.Fit(self)
        self.Layout()
        # end wxGlade

    def on_cancel(self, event):  # wxGlade: MyDialog.<event_handler>
        print("Event handler 'on_cancel' not implemented!")
        event.Skip()

    def on_add(self, event):  # wxGlade: MyDialog.<event_handler>
        print("Event handler 'on_add' not implemented!")
        event.Skip()

# end of class MyDialog

class MyDialogRunningMean(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialogRunningMean.__init__
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_3 = wx.Panel(self, wx.ID_ANY)
        self.spin_ctrl_double_1 = wx.SpinCtrlDouble(self.panel_3, wx.ID_ANY, "10.0", min=0.0, max=10000.0)
        self.Cancel = wx.Button(self, wx.ID_CANCEL, "", style=wx.BU_AUTODRAW)
        self.button_1 = wx.Button(self, wx.ID_OK, "", style=wx.BU_AUTODRAW)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_value_change, self.spin_ctrl_double_1)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.Cancel)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialogRunningMean.__set_properties
        self.SetTitle(_("Func parametr"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialogRunningMean.__do_layout
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        label_8 = wx.StaticText(self, wx.ID_ANY, _("This is a \"simple moving average,\" \nits results lag behind the data they apply to."))
        label_8.SetFont(wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, 0, ""))
        sizer_4.Add(label_8, 1, wx.ALL | wx.EXPAND, 10)
        label_3 = wx.StaticText(self.panel_3, wx.ID_ANY, _("Please, enter window size\nin seconds:"), style=wx.ALIGN_LEFT)
        sizer_6.Add(label_3, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_6.Add(self.spin_ctrl_double_1, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        sizer_6.Add((20, 20), 0, 0, 0)
        self.panel_3.SetSizer(sizer_6)
        sizer_4.Add(self.panel_3, 1, wx.EXPAND, 0)
        sizer_5.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_5.Add(self.Cancel, 0, 0, 0)
        sizer_5.Add(self.button_1, 0, 0, 0)
        sizer_4.Add(sizer_5, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL, 10)
        self.SetSizer(sizer_4)
        sizer_4.Fit(self)
        self.Layout()
        # end wxGlade

    def on_value_change(self, event):  # wxGlade: MyDialogRunningMean.<event_handler>
        print("Event handler 'on_value_change' not implemented!")
        event.Skip()

    def on_cancel(self, event):  # wxGlade: MyDialogRunningMean.<event_handler>
        print("Event handler 'on_cancel' not implemented!")
        event.Skip()

    def on_add(self, event):  # wxGlade: MyDialogRunningMean.<event_handler>
        print("Event handler 'on_add' not implemented!")
        event.Skip()

# end of class MyDialogRunningMean

class MyDownsampleDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDownsampleDlg.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_4 = wx.Panel(self, wx.ID_ANY)
        self.label_cur_sample_rate = wx.StaticText(self.panel_4, wx.ID_ANY, _("--"), style=wx.ALIGN_RIGHT)
        self.spin_ctrl_new_samplerate = wx.SpinCtrl(self.panel_4, wx.ID_ANY, "1", min=1, max=1000)
        self.choice_func = wx.Choice(self.panel_4, wx.ID_ANY, choices=[_("choice 1")])
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL, "", style=wx.BU_AUTODRAW)
        self.btn_ok = wx.Button(self, wx.ID_OK, "", style=wx.BU_AUTODRAW)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHOICE, self.on_choice_func, self.choice_func)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.btn_cancel)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDownsampleDlg.__set_properties
        self.SetTitle(_("dialog"))
        self.choice_func.SetToolTip(wx.ToolTip(_("Select function to use while downsamping data")))
        self.btn_ok.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDownsampleDlg.__do_layout
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.FlexGridSizer(0, 3, 3, 3)
        label_5 = wx.StaticText(self.panel_4, wx.ID_ANY, _("Current samplerate:"), style=wx.ALIGN_CENTER | wx.ALIGN_RIGHT)
        grid_sizer_2.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.label_cur_sample_rate, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add((20, 34), 0, 0, 0)
        label_6 = wx.StaticText(self.panel_4, wx.ID_ANY, _("New samplerate:"))
        grid_sizer_2.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.spin_ctrl_new_samplerate, 1, wx.EXPAND, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        label_7 = wx.StaticText(self.panel_4, wx.ID_ANY, _("Function type:"))
        grid_sizer_2.Add(label_7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.choice_func, 1, wx.EXPAND, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        self.panel_4.SetSizer(grid_sizer_2)
        sizer_8.Add(self.panel_4, 1, wx.EXPAND, 0)
        sizer_5.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_5.Add(self.btn_cancel, 0, 0, 0)
        sizer_5.Add(self.btn_ok, 0, 0, 0)
        sizer_8.Add(sizer_5, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_8)
        sizer_8.Fit(self)
        self.Layout()
        # end wxGlade

    def on_choice_func(self, event):  # wxGlade: MyDownsampleDlg.<event_handler>
        print("Event handler 'on_choice_func' not implemented!")
        event.Skip()

    def on_cancel(self, event):  # wxGlade: MyDownsampleDlg.<event_handler>
        print("Event handler 'on_cancel' not implemented!")
        event.Skip()

    def on_ok(self, event):  # wxGlade: MyDownsampleDlg.<event_handler>
        print("Event handler 'on_ok' not implemented!")
        event.Skip()

# end of class MyDownsampleDlg

class MyDialogRunningMeancentered(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialogRunningMeancentered.__init__
        kwds["style"] = kwds.get("style", 0) | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_5 = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SIMPLE)
        self.spin_ctrl_current_samplerate = wx.SpinCtrlDouble(self, wx.ID_ANY, "10.0", min=0.0, max=10000.0)
        self.spin_ctrl_windowsize = wx.SpinCtrlDouble(self, wx.ID_ANY, "10.0", min=0.0, max=10000.0)
        self.Cancel = wx.Button(self, wx.ID_CANCEL, "", style=wx.BU_AUTODRAW)
        self.button_1 = wx.Button(self, wx.ID_OK, "", style=wx.BU_AUTODRAW)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_value_change, self.spin_ctrl_current_samplerate)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_value_change, self.spin_ctrl_windowsize)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.Cancel)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialogRunningMeancentered.__set_properties
        self.SetTitle(_("Func parametr"))
        self.spin_ctrl_current_samplerate.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialogRunningMeancentered.__do_layout
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_3 = wx.FlexGridSizer(0, 2, 5, 5)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        label_8 = wx.StaticText(self.panel_5, wx.ID_ANY, _("This \"running mean centered\" uses a central \nrunning average to align its results with their data. \nThe <Windows size> must be a multiple of the <samplerate>.\n"))
        label_8.SetFont(wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, 0, ""))
        sizer_9.Add(label_8, 2, wx.ALL | wx.EXPAND, 10)
        self.panel_5.SetSizer(sizer_9)
        sizer_4.Add(self.panel_5, 2, wx.ALL | wx.EXPAND, 5)
        label_5 = wx.StaticText(self, wx.ID_ANY, _("Current <samplerate> in seconds:"), style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)
        grid_sizer_3.Add(self.spin_ctrl_current_samplerate, 0, wx.ALL, 3)
        label_4 = wx.StaticText(self, wx.ID_ANY, _("<Window size> in seconds:"), style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)
        grid_sizer_3.Add(self.spin_ctrl_windowsize, 0, wx.ALL, 3)
        grid_sizer_3.AddGrowableCol(1)
        sizer_4.Add(grid_sizer_3, 0, wx.EXPAND, 0)
        sizer_5.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_5.Add(self.Cancel, 0, 0, 0)
        sizer_5.Add(self.button_1, 0, 0, 0)
        sizer_4.Add(sizer_5, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL, 10)
        self.SetSizer(sizer_4)
        sizer_4.Fit(self)
        sizer_4.SetSizeHints(self)
        self.Layout()
        # end wxGlade

    def on_value_change(self, event):  # wxGlade: MyDialogRunningMeancentered.<event_handler>
        print("Event handler 'on_value_change' not implemented!")
        event.Skip()

    def on_cancel(self, event):  # wxGlade: MyDialogRunningMeancentered.<event_handler>
        print("Event handler 'on_cancel' not implemented!")
        event.Skip()

    def on_add(self, event):  # wxGlade: MyDialogRunningMeancentered.<event_handler>
        print("Event handler 'on_add' not implemented!")
        event.Skip()

# end of class MyDialogRunningMeancentered

class MyDialogFakeData(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialogFakeData.__init__
        kwds["style"] = kwds.get("style", 0) | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY, style=wx.NB_FIXEDWIDTH | wx.NB_TOP)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.checkbox_create_faked_tag = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Create faked-data tag"), style=wx.CHK_2STATE)
        self.checkbox_create_norma_flag = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Create <NORMA> tag"), style=wx.CHK_2STATE)
        self.checkbox_create_alarm_flag = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Create <ALARM> tag"), style=wx.CHK_2STATE)
        self.panel_6 = wx.Panel(self, wx.ID_ANY)
        self.Cancel = wx.Button(self.panel_6, wx.ID_CANCEL, "", style=wx.BU_AUTODRAW)
        self.button_1 = wx.Button(self.panel_6, wx.ID_OK, "", style=wx.BU_AUTODRAW)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.Cancel)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialogFakeData.__set_properties
        self.SetTitle(_("Fake Data Generator"))
        self.SetSize((400, 300))
        self.checkbox_create_faked_tag.SetToolTip(wx.ToolTip(_(u"\u0422\u0435\u0433 \u041d\u0415 \u0434\u043e\u043b\u0436\u0435\u043d \u0431\u044b\u0442\u044c \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d \u043f\u0440\u0438 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u0438 \u043c\u043e\u0434\u0435\u043b\u0438 \u0418\u0418. \u0422\u043e\u043b\u044c\u043a\u043e \u0434\u043b\u044f \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430.")))
        self.checkbox_create_faked_tag.SetValue(1)
        self.checkbox_create_norma_flag.SetToolTip(wx.ToolTip(_(u"\u0422\u0435\u0433 \u0434\u043e\u043b\u0436\u0435\u043d \u0431\u044b\u0442\u044c \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d \u0432 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0435 \u0432\u044b\u0445\u043e\u0434\u043d\u043e\u0433\u043e \u043f\u0440\u0438 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u0438 \u043c\u043e\u0434\u0435\u043b\u0438 \u0418\u0418.")))
        self.checkbox_create_norma_flag.Enable(False)
        self.checkbox_create_norma_flag.SetValue(1)
        self.checkbox_create_alarm_flag.SetToolTip(wx.ToolTip(_(u"\u0422\u0435\u0433 \u0434\u043e\u043b\u0436\u0435\u043d \u0431\u044b\u0442\u044c \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d \u0432 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0435 \u0432\u044b\u0445\u043e\u0434\u043d\u043e\u0433\u043e \u043f\u0440\u0438 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u0438 \u043c\u043e\u0434\u0435\u043b\u0438 \u0418\u0418.")))
        self.checkbox_create_alarm_flag.Enable(False)
        self.checkbox_create_alarm_flag.SetValue(1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialogFakeData.__do_layout
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        label_9 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, _("Faked data will be generated for selected tags. New data will be placed in the hidden area. This area will be used while fit model."), style=wx.ALIGN_LEFT | wx.ST_NO_AUTORESIZE)
        sizer_11.Add(label_9, 1, wx.ALL | wx.EXPAND, 3)
        sizer_11.Add(self.checkbox_create_faked_tag, 0, 0, 0)
        sizer_11.Add(self.checkbox_create_norma_flag, 0, 0, 0)
        sizer_11.Add(self.checkbox_create_alarm_flag, 0, 0, 0)
        self.notebook_1_pane_1.SetSizer(sizer_11)
        self.notebook_1.AddPage(self.notebook_1_pane_1, _("Cross diag"))
        sizer_10.Add(self.notebook_1, 2, wx.ALL | wx.EXPAND, 5)
        sizer_5.Add(self.Cancel, 0, 0, 0)
        sizer_5.Add(self.button_1, 0, 0, 0)
        self.panel_6.SetSizer(sizer_5)
        sizer_10.Add(self.panel_6, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        self.SetSizer(sizer_10)
        self.Layout()
        # end wxGlade

    def on_cancel(self, event):  # wxGlade: MyDialogFakeData.<event_handler>
        print("Event handler 'on_cancel' not implemented!")
        event.Skip()

    def on_add(self, event):  # wxGlade: MyDialogFakeData.<event_handler>
        print("Event handler 'on_add' not implemented!")
        event.Skip()

# end of class MyDialogFakeData

class FillDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: FillDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((564, 377))
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY, style=wx.NB_FIXEDWIDTH | wx.NB_TOP)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.choice_intertype = wx.Choice(self.notebook_1_pane_1, wx.ID_ANY, choices=[])
        self.intertype_desc = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, _("Select above the kind of interpolation"))
        self.panel_6 = wx.Panel(self, wx.ID_ANY)
        self.Cancel = wx.Button(self.panel_6, wx.ID_CANCEL, "", style=wx.BU_AUTODRAW)
        self.button_1 = wx.Button(self.panel_6, wx.ID_OK, "", style=wx.BU_AUTODRAW)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHOICE, self.on_choice_intertype, self.choice_intertype)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.Cancel)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: FillDialog.__set_properties
        self.SetTitle(_("dialog_2"))
        self.SetSize((564, 377))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FillDialog.__do_layout
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        label_9 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, _("There are several interpolation facilities available."))
        sizer_11.Add(label_9, 0, wx.ALL, 3)
        sizer_11.Add(self.choice_intertype, 0, wx.ALL, 10)
        sizer_11.Add(self.intertype_desc, 0, wx.ALL, 3)
        sizer_11.Add((0, 0), 0, 0, 0)
        self.notebook_1_pane_1.SetSizer(sizer_11)
        self.notebook_1.AddPage(self.notebook_1_pane_1, _("Interpolation"))
        sizer_12.Add(self.notebook_1, 2, wx.ALL | wx.EXPAND, 5)
        sizer_5.Add(self.Cancel, 0, 0, 0)
        sizer_5.Add(self.button_1, 0, 0, 0)
        self.panel_6.SetSizer(sizer_5)
        sizer_12.Add(self.panel_6, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        self.SetSizer(sizer_12)
        self.Layout()
        # end wxGlade

    def on_choice_intertype(self, event):  # wxGlade: FillDialog.<event_handler>
        print("Event handler 'on_choice_intertype' not implemented!")
        event.Skip()

    def on_cancel(self, event):  # wxGlade: FillDialog.<event_handler>
        print("Event handler 'on_cancel' not implemented!")
        event.Skip()

    def on_add(self, event):  # wxGlade: FillDialog.<event_handler>
        print("Event handler 'on_add' not implemented!")
        event.Skip()

# end of class FillDialog

class MyFrameTest(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrameTest.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.combo_box_1 = wx.ComboBox(self, wx.ID_ANY, choices=[_("choice 1"), _("choice 2"), _("last choice")], style=wx.CB_DROPDOWN | wx.CB_SIMPLE)
        self.choice_1 = wx.Choice(self, wx.ID_ANY, choices=[_("choice 1"), _("2"), _("3")])

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrameTest.__set_properties
        self.SetTitle(_("frame_1"))
        self.choice_1.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrameTest.__do_layout
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_13.Add(self.combo_box_1, 0, 0, 0)
        sizer_13.Add(self.choice_1, 0, 0, 0)
        self.SetSizer(sizer_13)
        self.Layout()
        # end wxGlade

# end of class MyFrameTest

class MyDialog1(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog1.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.signals_notebook = wx.Notebook(self, wx.ID_ANY)
        self.notebook_2_pane_1 = wx.Panel(self.signals_notebook, wx.ID_ANY)
        self.notebook_2_Rectangle = wx.Panel(self.signals_notebook, wx.ID_ANY)
        self.notebook_2_Sawwithrighthanddeclination = wx.Panel(self.signals_notebook, wx.ID_ANY)
        self.notebook_2_Sawwithlefthanddeclination = wx.Panel(self.signals_notebook, wx.ID_ANY)
        self.notebook_2_Triangle = wx.Panel(self.signals_notebook, wx.ID_ANY)
        self.notebook_2_Trianglewiththebasis = wx.Panel(self.signals_notebook, wx.ID_ANY)
        self.notebook_2_Isoscelestrapeze = wx.Panel(self.signals_notebook, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog1.__set_properties
        self.SetTitle(_("Add Signal"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog1.__do_layout
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        self.signals_notebook.AddPage(self.notebook_2_pane_1, _("SIN"))
        self.signals_notebook.AddPage(self.notebook_2_Rectangle, _("Rectangle"))
        self.signals_notebook.AddPage(self.notebook_2_Sawwithrighthanddeclination, _("Saw with right-hand declination"))
        self.signals_notebook.AddPage(self.notebook_2_Sawwithlefthanddeclination, _("Saw with left-hand declination"))
        self.signals_notebook.AddPage(self.notebook_2_Triangle, _("Triangle"))
        self.signals_notebook.AddPage(self.notebook_2_Trianglewiththebasis, _("Triangle with the basis"))
        self.signals_notebook.AddPage(self.notebook_2_Isoscelestrapeze, _("Isosceles trapeze"))
        sizer_7.Add(self.signals_notebook, 1, wx.EXPAND, 0)
        sizer_7.Add((0, 0), 0, 0, 0)
        self.SetSizer(sizer_7)
        sizer_7.Fit(self)
        self.Layout()
        self.Centre()
        # end wxGlade

# end of class MyDialog1

class DataConfApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class DataConfApp

if __name__ == "__main__":
    gettext.install("data_conf") # replace with the appropriate catalog name

    data_conf = DataConfApp(0)
    data_conf.MainLoop()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.2 on Tue May 22 19:58:38 2018
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
        self.bitmap_button_excel_import = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/excel_imports.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_import = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/table-import-icon.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW | wx.BU_EXACTFIT)
        self.bitmap_button_load = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/inbox_upload.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW | wx.BU_EXACTFIT)
        self.bitmap_button_save = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/inbox_download.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_2excel = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/excel_exports.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_show = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/chart_curve.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW | wx.BU_EXACTFIT)
        self.panel_3 = wx.Panel(self, wx.ID_ANY)
        self.bitmap_button_clear_selection = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/cell_clear.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.choice_derivative = wx.Choice(self.panel_3, wx.ID_ANY, choices=[_("choice 1")])
        self.bitmap_button_add_derivative = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/tag_blue_add.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_delete_selection = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/cell_delete.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_fillna = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/fill_color.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.bitmap_button_downsample = wx.BitmapButton(self.panel_3, wx.ID_ANY, wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/drum.png", wx.BITMAP_TYPE_ANY), style=wx.BU_AUTODRAW)
        self.panel_2 = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.FULL_REPAINT_ON_RESIZE)
        self.label_start_time = wx.StaticText(self.panel_2, wx.ID_ANY, _("--"))
        self.label_working_dir = wx.StaticText(self.panel_2, wx.ID_ANY, _("--"), style=wx.ALIGN_RIGHT)
        self.label_stop_time = wx.StaticText(self.panel_2, wx.ID_ANY, _("--"))
        self.label_filename = wx.StaticText(self.panel_2, wx.ID_ANY, _("No data yet"), style=wx.ALIGN_RIGHT)
        self.tags_grid = wx.grid.Grid(self.panel_2, wx.ID_ANY, size=(1, 1))
        self.label_tags_selected_number = wx.StaticText(self.panel_2, wx.ID_ANY, _("0"), style=wx.ALIGN_LEFT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_import_excel_btn, self.bitmap_button_excel_import)
        self.Bind(wx.EVT_BUTTON, self.on_import_btn, self.bitmap_button_import)
        self.Bind(wx.EVT_BUTTON, self.on_load_btn, self.bitmap_button_load)
        self.Bind(wx.EVT_BUTTON, self.on_save_btn, self.bitmap_button_save)
        self.Bind(wx.EVT_BUTTON, self.on_export_2excel_btn, self.bitmap_button_2excel)
        self.Bind(wx.EVT_BUTTON, self.on_show_btn, self.bitmap_button_show)
        self.Bind(wx.EVT_BUTTON, self.on_clear_selection_btn, self.bitmap_button_clear_selection)
        self.Bind(wx.EVT_CHOICE, self.on_choice_derivative_btn, self.choice_derivative)
        self.Bind(wx.EVT_BUTTON, self.on_add_button, self.bitmap_button_add_derivative)
        self.Bind(wx.EVT_BUTTON, self.on_delete_selection_btn, self.bitmap_button_delete_selection)
        self.Bind(wx.EVT_BUTTON, self.on_fillna_btn, self.bitmap_button_fillna)
        self.Bind(wx.EVT_BUTTON, self.on_downsample_btn, self.bitmap_button_downsample)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_CLICK, self.on_select_cell, self.tags_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_LABEL_LEFT_CLICK, self.on_select_cell, self.tags_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_RANGE_SELECT, self.on_select_cell, self.tags_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.on_select_cell, self.tags_grid)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("Data configurator"))
        self.bitmap_button_excel_import.SetToolTip(_("import from excel"))
        self.bitmap_button_excel_import.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/excel_imports-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_excel_import.SetSize(self.bitmap_button_excel_import.GetBestSize())
        self.bitmap_button_import.SetToolTip(_("Import data"))
        self.bitmap_button_import.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/table-import-icon-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_import.SetSize(self.bitmap_button_import.GetBestSize())
        self.bitmap_button_load.SetToolTip(_("Load data"))
        self.bitmap_button_load.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/inbox_upload-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_load.SetSize(self.bitmap_button_load.GetBestSize())
        self.bitmap_button_save.SetToolTip(_("Save data"))
        self.bitmap_button_save.Enable(False)
        self.bitmap_button_save.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/inbox_download-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_save.SetSize(self.bitmap_button_save.GetBestSize())
        self.bitmap_button_2excel.SetToolTip(_("Export to excel"))
        self.bitmap_button_2excel.Enable(False)
        self.bitmap_button_2excel.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/excel_exports-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_2excel.SetSize(self.bitmap_button_2excel.GetBestSize())
        self.bitmap_button_show.SetToolTip(_("Show selected tags"))
        self.bitmap_button_show.Enable(False)
        self.bitmap_button_show.SetSize(self.bitmap_button_show.GetBestSize())
        self.bitmap_button_clear_selection.SetToolTip(_("Clear selection"))
        self.bitmap_button_clear_selection.Enable(False)
        self.bitmap_button_clear_selection.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/cell_clear-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_clear_selection.SetSize(self.bitmap_button_clear_selection.GetBestSize())
        self.choice_derivative.SetToolTip(_("Select derivative function to add"))
        self.choice_derivative.Enable(False)
        self.bitmap_button_add_derivative.SetToolTip(_("Add tags derived from selected"))
        self.bitmap_button_add_derivative.Enable(False)
        self.bitmap_button_add_derivative.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/tag_blue_add-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_add_derivative.SetSize(self.bitmap_button_add_derivative.GetBestSize())
        self.bitmap_button_delete_selection.SetToolTip(_("Delete selected tags"))
        self.bitmap_button_delete_selection.Enable(False)
        self.bitmap_button_delete_selection.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/cell_delete-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_delete_selection.SetSize(self.bitmap_button_delete_selection.GetBestSize())
        self.bitmap_button_fillna.SetToolTip(_("Fill missing data"))
        self.bitmap_button_fillna.Enable(False)
        self.bitmap_button_fillna.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/fill_color-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_fillna.SetSize(self.bitmap_button_fillna.GetBestSize())
        self.bitmap_button_downsample.SetToolTip(_("Downsample dataset"))
        self.bitmap_button_downsample.Enable(False)
        self.bitmap_button_downsample.SetBitmapDisabled(wx.Bitmap("/home/damir/PycharmProjects/zbv/src/wxgui/glade_gui/icons/drum-dis.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_downsample.SetSize(self.bitmap_button_downsample.GetBestSize())
        self.tags_grid.CreateGrid(10, 3)
        self.tags_grid.EnableEditing(0)
        self.tags_grid.SetSelectionMode(wx.grid.Grid.SelectRows)
        self.tags_grid.SetColLabelValue(0, _("TAG"))
        self.tags_grid.SetColLabelValue(1, _("MIN value"))
        self.tags_grid.SetColLabelValue(2, _("MAX value"))
        self.panel_2.SetScrollRate(10, 10)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(0, 3, 2, 2)
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
        sizer_2.Add(self.bitmap_button_show, 0, 0, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.ALL, 2)
        sizer_4.Add(self.bitmap_button_clear_selection, 0, 0, 0)
        sizer_4.Add(self.choice_derivative, 1, wx.EXPAND, 0)
        sizer_4.Add(self.bitmap_button_add_derivative, 0, 0, 0)
        sizer_4.Add(self.bitmap_button_delete_selection, 0, 0, 0)
        static_line_4 = wx.StaticLine(self.panel_3, wx.ID_ANY, style=wx.LI_VERTICAL)
        sizer_4.Add(static_line_4, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_4.Add(self.bitmap_button_fillna, 0, 0, 0)
        sizer_4.Add(self.bitmap_button_downsample, 0, 0, 0)
        self.panel_3.SetSizer(sizer_4)
        sizer_1.Add(self.panel_3, 0, wx.ALL, 2)
        label_1 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Start time:"))
        grid_sizer_1.Add(label_1, 0, 0, 0)
        grid_sizer_1.Add(self.label_start_time, 0, 0, 0)
        grid_sizer_1.Add(self.label_working_dir, 1, wx.ALIGN_RIGHT | wx.LEFT, 10)
        label_2 = wx.StaticText(self.panel_2, wx.ID_ANY, _("End time:"))
        grid_sizer_1.Add(label_2, 0, 0, 0)
        grid_sizer_1.Add(self.label_stop_time, 0, 0, 0)
        grid_sizer_1.Add(self.label_filename, 1, wx.ALIGN_RIGHT | wx.LEFT, 10)
        grid_sizer_1.AddGrowableCol(2)
        sizer_3.Add(grid_sizer_1, 0, wx.EXPAND, 0)
        sizer_3.Add(self.tags_grid, 1, wx.ALL | wx.EXPAND, 1)
        label_4 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Tags selected:"))
        sizer_7.Add(label_4, 0, wx.RIGHT, 5)
        sizer_7.Add(self.label_tags_selected_number, 0, 0, 0)
        sizer_3.Add(sizer_7, 0, 0, 0)
        self.panel_2.SetSizer(sizer_3)
        sizer_1.Add(self.panel_2, 1, wx.ALL | wx.EXPAND, 2)
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

    def on_show_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_show_btn' not implemented!")
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

    def on_delete_selection_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_delete_selection_btn' not implemented!")
        event.Skip()

    def on_fillna_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_fillna_btn' not implemented!")
        event.Skip()

    def on_downsample_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'on_downsample_btn' not implemented!")
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
        self.choice_func.SetToolTip(_("Select function to use while downsamping data"))
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
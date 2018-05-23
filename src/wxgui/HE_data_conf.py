# hand edited data configurator
# import pickle
import wx
import wx.grid as gridlib
import os.path
import datetime
import logging
import tables

from constants import *

from glade_gui.data_conf import MyFrame, MyDialog, \
    MyDialogRunningMean, MyDownsampleDlg, \
    MyDialogRunningMeancentered
from constants import *
import data_reader
from BusyFrame import BusyFrame

# DATA = data_reader.ScadaDataFile()
TAG_column = 0
MINVALUE_column = 1
MAXVALUE_column = 2


def GetLastWorkingDir():
    return r'/home/damir/PycharmProjects/data'


class HEMyDialog(MyDialog):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        # added fraction of shift value
        self.spin_ctrl_double_1.SetDigits(2)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def on_add(self, event):
        self.EndModal(wx.ID_OK)


class HEMyDownSampleDialog(MyDownsampleDlg):
    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def on_ok(self, event):
        self.EndModal(wx.ID_OK)

    def on_choice_func(self, event):
        if self.choice_func.GetSelection() != wx.NOT_FOUND:
            self.btn_ok.Enable()


class HEMyDialogRM(MyDialogRunningMean):
    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def on_add(self, event):
        self.EndModal(wx.ID_OK)


class HEMyDialogRMC(MyDialogRunningMeancentered):
    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def on_add(self, event):
        self.EndModal(wx.ID_OK)



class HEMyFrame(MyFrame, BusyFrame):
    def __init__(self, *args, **kwargs):
        self.DATA = data_reader.ScadaDataFile()
        super().__init__(*args, **kwargs)
        # self.ss_contentNotSaved = False
        self.ss_input_data_pathname = None
        self.ad = self.ad_dydt, self.ad_shift, self.ad_normalise, \
                  self.ad_running_mean, self.ad_std_deviation, \
                  self.ad_running_mean_weight, self.ad_running_mean_centered
        self.choice_derivative.Clear()
        print([i.__doc__ for i in self.ad])
        self.choice_derivative.AppendItems([i.__doc__ for i in self.ad])
        self.choice_derivative.Select(wx.NOT_FOUND)
        self.pathname = GetLastWorkingDir()
        self.ss_prev_rm_window_size = None

    @property
    def ss_contentNotSaved(self):
        return not self.DATA.ss_data_saved

    def on_import_excel_btn(self, event):
        logging.debug('Import data btn')
        if self.ss_contentNotSaved:
            if wx.MessageBox(_("Current content has not been saved! Proceed?"), _("Please confirm"),
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        if os.path.isdir(self.pathname):
            os.chdir(self.pathname)
        elif os.path.isfile(self.pathname):
            os.chdir(os.path.split(self.pathname)[0])

        # ask the user what xlsx file to open
        with wx.FileDialog(self, _("Import excel data file"), wildcard=XLSX_WILDCARD,
                           defaultDir=os.path.basename(self.pathname),
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            # Proceed loading the file chosen by the user
            self.pathname = pathname = fileDialog.GetPath()
            try:
                # disableAll = wx.WindowDisabler()
                # self.wait = BusyInfo("Please wait, \nImport excel data file <<%s>>" % pathname, parent=self)
                # wx.GetApp().Yield()
                self.busy = _("Import excel file")
                self.DATA.import_from_excel(pathname)
                self.busy = False
                # self.wait = None
                # del disableAll
                # wx.GetApp().Yield()
            except IOError or FileNotFoundError:
                wx.LogError("Cannot import data from xslx file '%s'." % pathname)
        self.update_table()
        self.Layout()

    def on_import_btn(self, event):
        logging.debug('Import data btn')
        if self.ss_contentNotSaved:
            if wx.MessageBox(_("Current content has not been saved! Proceed?"), _("Please confirm"),
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return
        if os.path.isdir(self.pathname):
            os.chdir(self.pathname)
        elif os.path.isfile(self.pathname):
            os.chdir(os.path.split(self.pathname)[0])

        # ask the user what new file to open
        with wx.FileDialog(self, _("Open txt data file"), wildcard=_("txt files (*.txt)|*.txt"),
                           defaultDir=os.path.basename(self.pathname),
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            # Proceed loading the file chosen by the user
            self.pathname = pathname = fileDialog.GetPath()
            try:
                self.doImportData(pathname)
                self.label_filename.SetLabelText(os.path.split(pathname)[1])
            except IOError or FileNotFoundError:
                wx.LogError("Cannot open file '%s'." % pathname)
        self.label_working_dir.SetLabelText(os.getcwd())
        self.Layout()

    def on_save_btn(self, event):
        logging.debug('Save data button')
        proposed_filename_wo_ext = os.path.splitext(os.path.basename(self.pathname))[0]
        logging.debug(proposed_filename_wo_ext)
        proposed_directory = os.path.split(self.pathname)[0]

        # ###
        # def OnSaveAs(self, event):
        #
        #     with wx.FileDialog(self, "Save XYZ file", wildcard="XYZ files (*.xyz)|*.xyz",
        #                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
        #
        #         if fileDialog.ShowModal() == wx.ID_CANCEL:
        #             return  # the user changed their mind
        #
        #         # save the current contents in the file
        #         pathname = fileDialog.GetPath()
        #         try:
        #             with open(pathname, 'w') as file:
        #                 self.doSaveData(file)
        #         except IOError:
        #             wx.LogError("Cannot save current data in file '%s'." % pathname)
        # ###

        # https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
        with wx.FileDialog(self, "Save data", wildcard=ZBV_DATA_WILDCARD,
                           defaultDir=proposed_directory,
                           defaultFile=proposed_filename_wo_ext + '.zbvdata',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                self.DATA.save_data(pathname)
                wx.MessageBox("Current data saved in to\n%s" % pathname, "Saved",
                              wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP, self)
                self.label_working_dir.SetLabelText(os.getcwd())
                self.label_filename.SetLabelText(os.path.split(pathname)[1])
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)
            except tables.exceptions.HDF5ExtError:
                wx.LogError("Cannot save current data in file '%s'. \n File busy?" % pathname)

    def on_load_btn(self, event):
        logging.debug('Load data button')
        proposed_filename_wo_ext = os.path.splitext(os.path.basename(self.pathname))[0]
        logging.debug(proposed_filename_wo_ext)
        proposed_directory = os.path.split(self.pathname)[0]

        with wx.FileDialog(self, "Load data", wildcard=ZBV_DATA_WILDCARD,
                           defaultDir=proposed_directory,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # load from the file
            pathname = fileDialog.GetPath()
            try:
                self.DATA.load_data(pathname)
                self.label_working_dir.SetLabelText(os.getcwd())
                self.label_filename.SetLabelText(os.path.split(pathname)[1])
            except IOError:
                wx.LogError("Cannot load data from file '%s'." % pathname)
            except KeyError:
                wx.LogError(
                    "Cannot load data from file '%s\n Probably, file was create with very old version of zbv'." % pathname)
        self.Layout()
        self.update_table()
        self.bitmap_button_save.Enable(True)
        self.choice_derivative.Enable(True)

    def doImportData(self, pathname):
        logging.info('Load file <<%s>>' % pathname)
        self.busy = _("Import data from <%s>" % pathname)
        self.DATA.import_data_from_csv(pathname)
        self.busy = False
        self.update_table()

    def update_table(self):
        self.busy_cursor = wx.BusyCursor()
        if self.tags_grid.GetNumberRows():  # wx таблица не пуста
            self.tags_grid.DeleteRows(pos=0, numRows=self.tags_grid.GetNumberRows())
        else:  # таблица пуста - удалять нечего
            pass
        self.label_start_time.SetLabelText(str(self.DATA.time_start))
        self.label_stop_time.SetLabelText(str(self.DATA.time_stop))
        G = self.tags_grid
        for idx, tag in enumerate(self.DATA.tags_list):
            G.AppendRows(numRows=1)
            G.SetCellValue(idx, TAG_column, tag)
            G.AutoSizeColumn(TAG_column)

            G.SetCellEditor(idx, MINVALUE_column, gridlib.GridCellFloatEditor())
            G.SetCellValue(idx, MINVALUE_column, '%.7f' % self.DATA.tag_min(tag))
            G.SetCellAlignment(idx, MINVALUE_column, wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
            G.AutoSizeColumn(MINVALUE_column)

            G.SetCellEditor(idx, MAXVALUE_column, gridlib.GridCellFloatEditor())
            G.SetCellValue(idx, MAXVALUE_column, '%.7f' % self.DATA.tag_max(tag))
            G.SetCellAlignment(idx, MAXVALUE_column, wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
            G.AutoSizeColumn(MAXVALUE_column)
        # update buttons
        if self.DATA.tags_list:  # не пустой список тэгов
            self.bitmap_button_fillna.Enable(True)
            self.bitmap_button_save.Enable(True)
            self.choice_derivative.Enable(True)
            self.bitmap_button_downsample.Enable(True)
            if self.DATA.data.size < 300000:
                self.bitmap_button_2excel.Enable()
                self.bitmap_button_2excel.SetToolTip(_("Export to excel"))
            else:
                self.bitmap_button_2excel.SetToolTip("Too much data! %i" % self.DATA.data.size)
                self.bitmap_button_2excel.Enable(False)
        else:  # пустой список тегов
            self.bitmap_button_downsample.Enable(False)
            self.bitmap_button_2excel.Enable(False)
            self.bitmap_button_save.Enable(False)
            self.on_clear_selection_btn(None)
            self.choice_derivative.Enable(False)

        self.Layout()
        self.busy_cursor = None

    def on_show_btn(self, event):
        self.DATA.show_me_data(self.get_selected_tags())

    def on_fillna_btn(self, event):
        self.DATA.fill_na_data()

    def on_delete_selection_btn(self, event):
        """Delete selected tags"""
        tags = self.get_selected_tags()
        if not len(tags):
            return
        self.busy = "Deleting..."
        for tag in tags:
            self.DATA.delete_tag(tag)
        self.busy = False
        self.update_table()

    def on_choice_derivative_btn(self, event):
        if len(self.get_selected_tags()):
            self.bitmap_button_add_derivative.Enable()

    def on_select_cell(self, event):
        if len(self.get_selected_tags()):  # there are some rows selected
            self.bitmap_button_show.Enable()
            self.bitmap_button_clear_selection.Enable()
            self.bitmap_button_delete_selection.Enable()
            if self.choice_derivative.GetSelection() != wx.NOT_FOUND:  # and one of derivative selected
                self.bitmap_button_add_derivative.Enable()
        else:
            self.bitmap_button_add_derivative.Enable(False)
            self.bitmap_button_show.Enable(False)
            self.bitmap_button_clear_selection.Enable(False)
            self.bitmap_button_add_derivative.Enable(False)
            self.bitmap_button_delete_selection.Enable(False)
        self.label_tags_selected_number.SetLabelText(str(len(self.get_selected_tags())))
        event.Skip()

    def on_add_button(self, event):
        func_doc = self.choice_derivative.GetStringSelection()
        for ad_func in self.ad:
            if ad_func.__doc__ == func_doc:
                logging.debug("<%s> selected" % ad_func)
                ad_func()
                self.update_table()
                self.busy = False
                break

    def on_clear_selection_btn(self, event):
        self.tags_grid.ClearSelection()
        self.bitmap_button_add_derivative.Enable(False)
        self.bitmap_button_show.Enable(False)
        self.bitmap_button_clear_selection.Enable(False)
        self.bitmap_button_delete_selection.Enable(False)

    def on_export_2excel_btn(self, event):
        logging.debug('Export to excel button')
        proposed_filename_wo_ext = os.path.splitext(os.path.basename(self.pathname))[0]
        logging.debug(proposed_filename_wo_ext)
        proposed_directory = os.path.split(self.pathname)[0]

        # https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
        with wx.FileDialog(self, "Export to excel", wildcard=XLSX_WILDCARD,
                           defaultDir=proposed_directory,
                           defaultFile=proposed_filename_wo_ext + '.xlsx',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                tags = self.get_selected_tags()
                if not tags:
                    tags = None
                self.DATA.export_2excel(pathname, tags_list=tags)
                wx.MessageBox("Current data exported in to excel file \n%s" % pathname, "Exported",
                              wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP, self)
                # self.label_working_dir.SetLabelText(os.getcwd())
                # self.label_filename.SetLabelText(os.path.split(pathname)[1])
            except IOError:
                wx.LogError("Cannot export data in to excel file '%s'." % pathname)

    def ad_dydt(self):
        """Derivative (dy/dt)"""
        tags = self.get_selected_tags()
        self.busy = "Calculating Derivative (dy/dt)..."
        for tag in tags:
            self.DATA.ad_dydt(tag)

    def ad_shift(self):
        """Shift value"""
        tags = self.get_selected_tags()
        if not len(tags):
            return
        dlg = HEMyDialog(parent=self, id=wx.ID_ANY)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        shift_value = float(dlg.spin_ctrl_double_1.GetValue())
        print(shift_value)
        self.busy = "Calculating Shift ..."
        for tag in tags:
            self.DATA.ad_shift(tag, shift_value)

    def on_downsample_btn(self, event):
        """Downsample dialog"""
        # http://pandas.pydata.org/pandas-docs/stable/timeseries.html#resampling
        # sum, mean, std, sem, max, min, median, first, last, ohlc
        downsampling_funcs = {
            'Sum of group': 'sum',
            'Pad': 'pad',
            'Mean of group': 'mean',
            # 'Standard deviation': 'std',
            # 'Standard error of the mean': 'sem',
            'Max of group': 'max',
            'Min of group': 'min',
            '! Median': 'median',
            'First of group value': 'first',
            'Last of group values': 'last',
            #'Ohlc': 'ohlc'

        }
        dlg = HEMyDownSampleDialog(parent=self, id=wx.ID_ANY)
        dlg.choice_func.Clear()
        dlg.choice_func.AppendItems(list(downsampling_funcs.keys()))
        dlg.label_cur_sample_rate.SetLabelText('%.1f' % self.DATA.config.get('freq in Secs', 0))
        dlg.Layout()
        res = dlg.ShowModal()
        if res == wx.ID_CANCEL:
            return
        elif res == wx.ID_OK:
            new_sample_rate = '%iS' % int(dlg.spin_ctrl_new_samplerate.GetValue())
            func = dlg.choice_func.GetStringSelection()
            self.DATA.data = getattr(self.DATA.data.resample(new_sample_rate), downsampling_funcs[func])()
            self.DATA.config['freq'] = new_sample_rate
            self.DATA.config['freq in Secs'] = int(dlg.spin_ctrl_new_samplerate.GetValue())
            # self.config['freq'] = 'S'
            # self.config['freq in Secs'] = 1
        self.update_table()
        self.Layout()

    def ad_normalise(self):
        """Normalize to 0..1"""
        tags = self.get_selected_tags()
        if not len(tags):
            return
        self.busy = "Normalizing..."
        for tag in tags:
            self.DATA.ad_normalise(tag)

    def ad_running_mean(self):
        """Running mean"""
        tags = self.get_selected_tags()
        if not len(tags):
            return
        dlg = HEMyDialogRM(parent=self, id=wx.ID_ANY)
        if self.ss_prev_rm_window_size is not None:
            dlg.spin_ctrl_double_1.SetValue(self.ss_prev_rm_window_size)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        window_size = int(dlg.spin_ctrl_double_1.GetValue())
        self.busy = "Calculating Running mean..."
        for tag in tags:
            self.DATA.ad_running_mean(tag, window_size)
        self.ss_prev_rm_window_size = window_size

    def ad_running_mean_centered(self):
        """Running mean centered"""
        tags = self.get_selected_tags()
        if not len(tags):
            return
        if not self.DATA.config.get('freq in Secs', 0):
            # unknown samplerate
            wx.MessageBox("I do not know the Samplerate!\nFirst set Samplerate with the drum button,\nthen fill the gaps of data.", "Unknown parameter",
                          wx.OK | wx.ICON_STOP | wx.STAY_ON_TOP, self)
            return
        else: # samplerate configured and it is non zero
            samplerate = self.DATA.config['freq in Secs']

        dlg = HEMyDialogRMC(parent=self, id=wx.ID_ANY)
        dlg.spin_ctrl_current_samplerate.SetValue(samplerate)
        if self.ss_prev_rm_window_size is not None:
            dlg.spin_ctrl_windowsize.SetValue(self.ss_prev_rm_window_size)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        window_size = int(dlg.spin_ctrl_windowsize.GetValue())
        self.busy = "Calculating Running mean..."
        for tag in tags:
            self.DATA.ad_running_mean_adv(tag, window_size)
        self.ss_prev_rm_window_size = window_size

    def ad_running_mean_weight(self):
        """"Exp moving averages"""
        tags = self.get_selected_tags()
        if not len(tags):
            return
        dlg = HEMyDialogRM(parent=self, id=wx.ID_ANY)
        if self.ss_prev_rm_window_size is not None:
            dlg.spin_ctrl_double_1.SetValue(self.ss_prev_rm_window_size)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        window_size = int(dlg.spin_ctrl_double_1.GetValue())
        self.busy = "Calculating Exp moving averages..."
        for tag in tags:
            self.DATA.ad_running_mean_weight(tag, window_size)
        self.ss_prev_rm_window_size = window_size

    def ad_std_deviation(self):
        """Standard deviation"""
        tags = self.get_selected_tags()
        if not len(tags):
            return
        dlg = HEMyDialogRM(parent=self, id=wx.ID_ANY)
        if self.ss_prev_rm_window_size is not None:
            dlg.spin_ctrl_double_1.SetValue(self.ss_prev_rm_window_size)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        window_size = int(dlg.spin_ctrl_double_1.GetValue())
        # print(window_size)
        for tag in tags:
            self.DATA.ad_std_deviation(tag, window_size)
        self.ss_prev_rm_window_size = window_size


    def get_selected_tags(self):
        """Returns list of selected tags"""
        ret = []
        selected_rows = self.tags_grid.GetSelectedRows()
        for r in selected_rows:
            ret.append(self.tags_grid.GetCellValue(row=r, col=0))
        # logging.debug("Selected tags: %s" % ret)
        return ret

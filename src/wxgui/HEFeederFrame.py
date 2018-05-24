import os
import logging
import datetime
import wx
import wx.adv
import pandas as pd
import matplotlib.pyplot as plt

from glade_gui.feeder import FeederFrame, MyDialogSelectDateTime

from constants import *

import data_reader

DATA = data_reader.ScadaDataFile()

import model

MODEL = model.Model()

import feeder


def GetLastWorkingDir():
    return r'/home/damir/PycharmProjects/data'


class HEMyDialogSelectDateTime(MyDialogSelectDateTime):
    def __init__(self, start_from, up_to, start=True, *args, **kwds):
        super().__init__(*args, **kwds)
        assert isinstance(start_from, datetime.datetime)
        assert isinstance(up_to, datetime.datetime)
        self.dt = start_from if start else up_to
        self.calendar_ctrl_1.SetDateRange(lowerdate=up_to, upperdate=start_from)
        if start:
            self.SetTitle('Select START time')
        else:
            self.SetTitle('Select STOP time')

        self.slider_1.SetMax(up_to.timestamp())
        print(up_to.timestamp())
        self.slider_1.SetMin(start_from.timestamp())
        print(start_from.timestamp())
        self.slider_1.SetPageSize(3600)
        self.slider_1.Enable()

    def on_scroll_slider(self, event):
        dt = datetime.datetime.fromtimestamp(self.slider_1.GetValue())
        self.dt = dt
        self.calendar_ctrl_1.SetDate(dt)
        self.time_start_selector.SetValue(dt)
        self.slider_1.SetFocus()
        event.Skip()

    def on_calendar_changed(self, event):
        dt = self.calendar_ctrl_1.GetDate()
        tm = self.time_start_selector.GetValue()
        assert isinstance(dt, wx.DateTime)
        # assert isinstance(tm, datetime.datetime)
        print(dt)
        print(tm)
        # print(datetime.datetime.combine(dt.date(), tm.time()))
        self.slider_1.SetValue(dt.GetTicks())
        dt = datetime.datetime.fromtimestamp(self.slider_1.GetValue())
        self.dt = dt

    def on_cancel_btn(self, event):
        self.EndModal(wx.CANCEL)

    def on_ok_button(self, event):
        self.EndModal(wx.OK)


class HEFeederFrame(FeederFrame):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.pathname = GetLastWorkingDir()
        self.ss_model_path = 'Not loaded'
        self.ss_dataset_filename = 'Not loaded'

    def update(self):
        for update_func in dir(self):
            if update_func.startswith('_upd'):
                self.__getattribute__(update_func)()
        self.Layout()

    def _upd_lbl_model_filename(self):
        self.lbl_model_name.SetLabelText(os.path.split(self.ss_model_path)[1])

    def _upd_lbl_dataset_filename(self):
        self.lbl_dataset_name.SetLabelText(os.path.split(self.ss_dataset_filename)[1])

    def _upd_btn_savemodel(self):
        self.bitmap_button_save_model.Enable(MODEL.ss_loaded and not MODEL.ss_saved)

    def _upd_bitmap_button_show(self):
        try:
            self.bitmap_button_show.Enable(len(DATA.tags_list))
        except AttributeError:
            self.bitmap_button_show.Enable(False)

    def _upd_bitmap_button_fit(self):
        self.bitmap_button_fit.Enable(self.model_can_be_trained)

    def _upd_bitmap_button_predict(self):
        self.bitmap_button_predict.Enable(self.model_can_predict)

    def _upd_bitmap_button_save_dataset(self):
        self.bitmap_button_save.Enable(DATA.ss_data_present)

    @property
    def model_can_be_trained(self):
        if not MODEL.ss_loaded or not DATA.ss_data_present:
            return False
        if set(MODEL.data_conf[INPUT_TAGS_NAMES]).issubset(DATA.tags) and \
           set(MODEL.data_conf[OUTPUT_TAGS_NAMES]).issubset(DATA.tags):
            return True
        else:
            return False

    @property
    def model_can_predict(self):
        if not MODEL.ss_loaded or not DATA.ss_data_present:
            return False
        if set(MODEL.data_conf[INPUT_TAGS_NAMES]).issubset(DATA.tags):
            return True
        else:
            return False

    def on_save_model_btn(self, event):
        # print(self.ss_start_time)
        # print(self.ss_stop_time)
        print(MODEL.conf)
        MODEL.model.summary()
        event.Skip()
        pass

    def on_load_data_btn(self, event):
        global DATA
        proposed_filename_wo_ext = os.path.splitext(os.path.basename(self.pathname))[0]
        logging.debug(proposed_filename_wo_ext)
        proposed_directory = os.path.split(self.pathname)[0]

        with wx.FileDialog(self, "Load data", wildcard=ZBV_DATA_WILDCARD,
                           defaultDir=proposed_directory,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
                           # defaultFile=proposed_filename_wo_ext,
                           ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # load from the file
            pathname = fileDialog.GetPath()
            try:
                DATA.load_data(pathname)
                # self.label_working_dir.SetLabelText(os.getcwd())
                # self.label_filename.SetLabelText(os.path.split(pathname)[1])
            except IOError:
                wx.LogError("Cannot load data from file '%s'." % pathname)

        # self.bitmap_button_show.Enable()
        # self.lbl_dataset_name.SetLabelText(os.path.split(path_wo_ext)[1])
        self.ss_dataset_filename = pathname
        self.update()

    def on_save_btn(self, event):
        global DATA
        proposed_filename_wo_ext = os.path.splitext(os.path.basename(self.pathname))[0]
        logging.debug(proposed_filename_wo_ext)
        proposed_directory = os.path.split(self.pathname)[0]

        with wx.FileDialog(self, "Save data", wildcard=ZBV_DATA_WILDCARD,
                           defaultDir=proposed_directory,
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                           # defaultFile=proposed_filename_wo_ext,
                           ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                DATA.save_data(pathname)
            except IOError:
                wx.LogError("Cannot load data from file '%s'." % pathname)

        # self.bitmap_button_show.Enable()
        # self.lbl_dataset_name.SetLabelText(os.path.split(path_wo_ext)[1])
        self.ss_dataset_filename = pathname
        self.update()

    def on_btn_openmodel(self, event):
        global MODEL
        with wx.FileDialog(self, "Load model", wildcard=ZBV_MODEL_WILDCARD,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                if MODEL.loadmodel(pathname):
                    # model_config, data_config, optimizer=model_optimizer, loss=self.choice_loss.GetStringSelection()

                    # global model_config  #CHECK it
                    # model_config = MODEL.layers
                    global data_config
                    data_config = MODEL.data_conf
                    # global model_optimizer #CHECK
                    # model_optimizer = MODEL.optimizer
                    wx.MessageBox("Model loaded from \n%s" % pathname, "Success",
                                  wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP, self)
                    self.ss_model_path = pathname
                    # self.lbl_model_name.SetLabelText(os.path.split(pathname)[1])
                else:
                    raise IOError
            except IOError or AttributeError:
                wx.LogError("Cannot load model from file '%s'." % pathname)
        self.update()

    def on_btn_savemodel(self, event):
        global MODEL
        # os.path.basename(self.ss_input_data_pathname)
        proposed_filename_wo_ext = ''  # os.path.splitext(os.path.basename(self.ss_input_data_pathname))[0]
        proposed_directory = GetLastWorkingDir()  # os.path.split(self.ss_input_data_pathname)[0]

        with wx.FileDialog(self, "Save model", wildcard=ZBV_MODEL_WILDCARD,
                           defaultDir=proposed_directory,
                           defaultFile=proposed_filename_wo_ext + '.zbvmod',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                if MODEL.savemodel(pathname):
                    wx.MessageBox("Model saved to\n%s" % pathname, "Saved",
                                  wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP, self)
                    # self.ss_input_data_pathname.SetLabelText(os.path.split(pathname)[1]) todo add label with model filename
                else:
                    raise IOError
            except IOError:
                wx.LogError("Cannot save model to file '%s'." % pathname)

    def on_btn_start_select(self, event):
        dlg = HEMyDialogSelectDateTime(parent=self, start_from=DATA.time_start, up_to=DATA.time_stop, start=True)
        if dlg.ShowModal() == wx.OK:
            self.ss_start_time = dlg.dt
            self.label_start_from.SetLabelText(str(self.ss_start_time))

    def on_btn_stop_select(self, event):
        dlg = HEMyDialogSelectDateTime(parent=self, start_from=DATA.time_start, up_to=DATA.time_stop, start=False)
        if dlg.ShowModal() == wx.OK:
            self.ss_stop_time = dlg.dt
            self.label_end_on.SetLabelText(str(self.ss_stop_time))
            self.Layout()

    def on_show_btn(self, event):
        global DATA
        DATA.show_me_data()

    def on_btn_fit(self, event):
        F = feeder.MyTimeseriesGenerator(MODEL.data_conf, DATA)
        MODEL.model.fit_generator(F, shuffle=True, epochs=200)

    def on_btn_predict(self, event):
        global DATA
        F = feeder.MyTimeseriesGenerator(MODEL.data_conf, DATA)
        # https://keras.io/models/sequential/#predict_generator
        preds = MODEL.model.predict_generator(F)
        pred_tag_names = []
        for tag in MODEL.data_conf[OUTPUT_TAGS_NAMES]:
            pred_tag_names.append( '*PREDICT*%s' % tag )

        print(pred_tag_names)
        print(preds)

        df = pd.DataFrame(preds, columns=pred_tag_names)
        df.plot()
        plt.legend(loc='best')
        plt.show()

        #DATA.data[pred_tag_names] = pred_series
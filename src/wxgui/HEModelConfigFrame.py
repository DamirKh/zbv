# Hand edited MyFrame
# import pickle
import wx
import os.path
import datetime

from constants import *

from glade_gui.ModelConfigFrame import ModelConfigFrame
from HEMyFrame import HEMyFrame
from glade_gui.MyModelViewer import MyModelViewer
from layers_opt import DEFINED_LAYERS
from loss_and_optim import DEFINED_OPTIMIZERS, loss_functions

from model import Model
from keras.utils import plot_model

from data_reader import ScadaDataFile

DATA = ScadaDataFile()

layers_names = [x.__doc__.split()[0] for x in DEFINED_LAYERS]
optimizers_names = [x.__doc__.split()[0] for x in DEFINED_OPTIMIZERS]

DEFINED_LAYERS_DICT = dict(zip(layers_names, DEFINED_LAYERS))
DEFINED_OPTIMIZERS_DICT = dict(zip(optimizers_names, DEFINED_OPTIMIZERS))
print(layers_names)
MAX_LEVELS = 7

model_config = [None, None, None, None, None, None, None, ]
data_config = {INPUT_TAGS_TOTAL: 0,
               OUTPUT_TAGS_TOTAL: 0,
               }

model_optimizer = None


def Layers_in_model():
    """Count defined layers"""
    i = 0
    for l in model_config:
        if not l is None:
            i += 1
    return i


class HEMyModelViewer(MyModelViewer):
    def __init__(self, filepath, *args, **kwds):
        super().__init__(*args, **kwds)
        self.bitmap_2.SetBitmap(wx.Bitmap(filepath, wx.BITMAP_TYPE_ANY))
        self.Layout()

    def on_close_btn(self, event):
        self.EndModal(0)


class HEModelConfigFrame(ModelConfigFrame):
    def __init__(self, model_config=[], view_only=False, *args, **kwargs):
        if True:
            self.ss_contentNotSaved = False
            self.ss_view_only = view_only
        self.model_config = model_config

        super().__init__(*args, **kwargs)
        # more binds here

        if not self.model_config:
            self.On_open_data_source_button(event=None)
            self.Prepare_layer_selectors()
            self.prepare_optimizer_selector()
            self.prepare_choice_loss_selector()

        self.Layout()

    def On_open_data_source_button(self, event):
        if self.ss_contentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open data file", wildcard=ZBV_DATA_WILDCARD,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            # Proceed loading the file chosen by the user
            self.ss_input_data_pathname = pathname = fileDialog.GetPath()
            try:
                self.doLoadData(pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)
            except KeyError:
                wx.LogError("Cannot load data file '%s'." % pathname)

    def doLoadData(self, filepath):
        global DATA
        DATA.load_data(filepath)
        self.meta_tags_list = DATA.tags_list
        print("tag list %s" % self.meta_tags_list)
        self.meta_tags = DATA.tags
        self.meta_time_start = DATA.time_start
        print("Data starts from %s" % self.meta_time_start)
        self.meta_time_stop = DATA.time_stop
        print("Data ends at %s" % self.meta_time_stop)
        self.meta_time_delta = DATA.time_delta
        print("Data lenth %i seconds" % self.meta_time_delta.total_seconds())
        self.UpdateTagList(self.meta_tags_list)
        self.label_data_source_name.SetLabelText(os.path.basename(self.ss_input_data_pathname))
        self.Layout()

    def UpdateTagList(self, tag_list):
        self.input_check_list_box.Clear()
        self.input_check_list_box.AppendItems(tag_list)
        self.output_check_list_box.Clear()
        self.output_check_list_box.AppendItems(tag_list)

        if self.simplemode:
            # https://stackoverflow.com/a/15968995/8124158  About keep items checked/unchecked
            print('Simple config mode')
            cross_tags = [tag for tag in tag_list if tag.endswith('=')]
            print(cross_tags)
            self.output_check_list_box.SetCheckedStrings(cross_tags)

        if not self.ss_view_only:
            self.input_check_list_box.Enable(True)
            self.output_check_list_box.Enable(True)
            self.OnInputCheckListBox(None)
            self.OnOutputCheckListBox(None)

    @property
    def simplemode(self):
        return self.checkbox_simplemode.GetValue()
        # return True

    def OnInputCheckListBox(self, e):
        '''count selected input tags'''
        self.input_tags_total_value = number = len(self.input_check_list_box.GetCheckedItems())
        text = self.label_input_tags_total.GetLabelText()[:-2]
        self.label_input_tags_total.SetLabelText(text + '%02i' % number)
        # print(self.input_check_list_box.GetCheckedStrings())
        if self.simplemode and e is not None:
            index = e.GetSelection()
            label = self.input_check_list_box.GetString(index)
            assert isinstance(label, str)
            if label.endswith('='):
                self.input_check_list_box.Check(index, False)
                self.input_check_list_box

    def OnOutputCheckListBox(self, event):
        '''count selected output tags'''
        self.output_tags_total_value = number = len(self.output_check_list_box.GetCheckedItems())
        text = self.label_output_tags_total.GetLabelText()[:-2]
        self.label_output_tags_total.SetLabelText(text + '%02i' % number)

    def on_edit_btn(self, event, layer):
        """Configure level"""
        lc = model_config[layer]
        print(lc)
        frame = HEMyFrame(layer_config=lc, parent=self, id=-1, title='Configure layer %i' % layer)
        res = frame.ShowModal()
        if res == wx.ID_OK:
            self.ss_contentNotSaved = True

    def on_choice_btn(self, event, layer):
        CurrentChoiceButton = event.GetEventObject()
        LayerTypeStr = CurrentChoiceButton.GetString(CurrentChoiceButton.GetSelection())
        value = 5
        if layer == MAX_LEVELS - 1:  # умолчательное значение для последнего слоя равно кол-ву выходных тегов
            value = self.output_tags_total_value if self.output_tags_total_value else value
        if layer == 0:  # умолчательное значение для первого слоя равно кол-ву вход тегов*2+1
            value = self.input_tags_total_value * 2 + 1 if self.input_tags_total_value else value

        model_config[layer] = DEFINED_LAYERS_DICT[LayerTypeStr](number=layer, value=value, bad_option=True)  # TODO!
        print('%s selected on layer #%i' % (LayerTypeStr, layer))
        for button in self.level_edit_btns[layer], self.level_delete_btns[layer]:
            button.Enable(True)
        self.ss_contentNotSaved = True

    def on_del_btn(self, event, layer):
        model_config[layer] = None
        self.level_selector_btns[layer].SetSelection(wx.NOT_FOUND)
        for button in self.level_edit_btns[layer], self.level_delete_btns[layer]:
            button.Enable(False)
        self.ss_contentNotSaved = True

    def Prepare_layer_selectors(self):
        print('Prepare choices')

        self.level_delete_btns = (self.button_300,
                                  self.button_301,
                                  self.button_302,
                                  self.button_303,
                                  self.button_304,
                                  self.button_305,
                                  self.button_306,
                                  )
        self.level_edit_btns = (self.button_200,
                                self.button_201,
                                self.button_202,
                                self.button_203,
                                self.button_204,
                                self.button_205,
                                self.button_206,
                                )

        self.level_selector_btns = \
            LevelSelectorBtns = (self.choice_100,
                                 self.choice_101,
                                 self.choice_102,
                                 self.choice_103,
                                 self.choice_104,
                                 self.choice_105,
                                 self.choice_106)

        for choice in LevelSelectorBtns:
            choice.Clear()
            choice.AppendItems(layers_names)
            choice.Enable()

    def prepare_optimizer_selector(self):
        self.choice_optimizer.Clear()
        self.choice_optimizer.AppendItems(optimizers_names)
        self.choice_optimizer.Enable()

    def on_choice_optimizer_btn(self, event):
        global model_optimizer
        self.button_edit_optimizer.Enable()
        CurrentChoiceButton = event.GetEventObject()
        OptimizerTypeStr = CurrentChoiceButton.GetString(CurrentChoiceButton.GetSelection())
        model_optimizer = DEFINED_OPTIMIZERS_DICT[OptimizerTypeStr]()
        self.ss_contentNotSaved = True

    def on_edit_optimizer_btn(self, event):
        """Configure optimizer"""
        print(model_optimizer)
        frame = HEMyFrame(layer_config=model_optimizer, parent=self, id=-1,
                          title='Configure optimizer %s' % model_optimizer.__doc__.split()[0])
        res = frame.ShowModal()
        if res == wx.ID_OK:
            self.ss_contentNotSaved = True

    def on_choice_loss_btn(self, event):
        event.Skip()

    def prepare_choice_loss_selector(self):
        self.choice_loss.Clear()
        self.choice_loss.AppendItems(loss_functions)
        self.choice_loss.Enable()
        self.choice_loss.SetSelection(0)

    def on_recompile_model_btn(self, event):
        self.test_compile()

    def print_to_info_label(self, s):
        if s is None:
            return
        current_text = self.info_label.GetLabelText()
        self.info_label.SetLabelText(current_text + '\n' + s)
        self.Layout()

    def test_compile(self):
        """Testing model compilation"""
        self.info_label.SetLabelText('%s' % datetime.datetime.now())
        data_config[INPUT_TAGS_TOTAL] = self.input_tags_total_value
        data_config[OUTPUT_TAGS_TOTAL] = self.output_tags_total_value
        data_config[INPUT_TAGS_NAMES] = self.input_check_list_box.GetCheckedStrings()
        data_config[OUTPUT_TAGS_NAMES] = self.output_check_list_box.GetCheckedStrings()
        data_config[WINDOW_SIZE] = self.windowsize_spin_ctrl.GetValue()
        try:
            test_model = Model(model_config, data_config, optimizer=model_optimizer,
                               loss=self.choice_loss.GetStringSelection())
            test_model.compile2()
            # txt = test_model.model.summary(print_fn = print_fn)
            self.KerasModel = test_model
            self.print_to_info_label(_("Compiled successfully"))
            self.show_model()
        except ValueError:
            self.print_to_info_label(_("Sorry,\nCompilation failed!"))
        self.Layout()

    def show_model(self):
        # https://keras.io/visualization/
        plot_model(self.KerasModel.model, to_file='model.png')
        imgdlg = HEMyModelViewer(parent=self, filepath='model.png')
        imgdlg.Layout()
        imgdlg.ShowModal()

    def on_save_model_btn(self, event):
        # os.path.basename(self.ss_input_data_pathname)
        proposed_filename_wo_ext = os.path.splitext(os.path.basename(self.ss_input_data_pathname))[0]
        proposed_directory = os.path.split(self.ss_input_data_pathname)[0]

        with wx.FileDialog(self, "Save model", wildcard=ZBV_MODEL_WILDCARD,
                           defaultDir=proposed_directory,
                           defaultFile=proposed_filename_wo_ext + '.zbvmod',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                if self.KerasModel.savemodel(pathname):
                    wx.MessageBox("Model saved to\n%s" % pathname, "Saved",
                                  wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP, self)
                    # self.ss_input_data_pathname.SetLabelText(os.path.split(pathname)[1]) todo add label with model filename
                    self.print_to_info_label('Model folder <%s>' % os.path.split(pathname)[0])
                    self.print_to_info_label('Filename: <%s>' % os.path.split(pathname)[1])
                else:
                    raise IOError
            except IOError:
                wx.LogError("Cannot save model to file '%s'." % pathname)

    def on_load_model_btn(self):
        wx.LogMessage("Not implemented!")
        return

        with wx.FileDialog(self, "Load model", wildcard=ZBV_MODEL_WILDCARD,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            pathname = fileDialog.GetPath()
            self.ss_view_only = True
            try:
                model = Model()
                if model.loadmodel(pathname):
                    # model_config, data_config, optimizer=model_optimizer, loss=self.choice_loss.GetStringSelection()

                    global model_config
                    model_config = model.layers

                    global data_config
                    data_config = model.data_conf

                    global model_optimizer
                    model_optimizer = model.optimizer

                    self.choice_loss.SetStringSelection(model.loss)
                    tag_list_from_model = list(set(data_config[INPUT_TAGS_NAMES]) + set(data_config[OUTPUT_TAGS_NAMES]))
                    self.UpdateTagList(tag_list_from_model)
                    for tag in data_config[INPUT_TAGS_NAMES]:
                        self.input_check_list_box

                    wx.MessageBox("Model loaded from \n%s" % pathname, "Success",
                                  wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP, self)
                    # self.ss_input_data_pathname.SetLabelText(os.path.split(pathname)[1]) todo add label with model filename
                    self.print_to_info_label('Model folder <%s>' % os.path.split(pathname)[0])
                    self.print_to_info_label('Filename: <%s>' % os.path.split(pathname)[1])
                else:
                    raise IOError()
            except IOError or AttributeError:
                wx.LogError("Cannot load model from file '%s'." % pathname)

# Hand edited MyFrame
from collections import OrderedDict
import wx.propgrid as wxpg
import wx


import layers_opt
#from glade_gui.MyFrame import MyFrame
from glade_gui.LayerConfDlg import LayerConfDlg as MyFrame


class HEMyFrame(MyFrame):
    def __init__(self, layer_config, *args, **kwargs):
        assert isinstance(layer_config, layers_opt.CommonLayerConfig)
        super().__init__(*args, **kwargs)
        self.Bind(wxpg.EVT_PG_CHANGED, self.OnPropGridChange)

        self.layer_config = lc = layer_config
        # print(layer_config)
        self.label_1.SetLabelText(lc.name)
        self.hyperlink_1.SetURL(lc.www)
        self.hyperlink_1.SetLabelText(lc.www)
        self.wxprop_layerconf_pair = OrderedDict()  # wx object to layer property config connectivity
        self.fill_property_grid()
        # self.Bind(wx.EVT_CLOSE, self.OnClose)

    def fill_property_grid(self):
        print('Filling property grid')
        pair = self.wxprop_layerconf_pair
        pg = self.property_grid_1
        lc = self.layer_config
        pg.Append(wxpg.PropertyCategory("1 - Basic Properties"))
        if len(lc.keys()):
            for p in lc.keys():
                # print('    property <<%s>>'%p)
                proper = lc[p]   # Конфигурационный объект потомок CommonProp
                value = lc[p]()
                curprop = None
                # p - parametr name
                # value - default value of parametr
                if isinstance(proper, layers_opt.BoolProp):  # дискретный параметр
                    curprop = pg.Append(wxpg.BoolProperty(p, value=value))  # объект wx

                elif isinstance(proper, layers_opt.RealRangeProp):  # вещественный параметр
                    curprop = pg.Append(wxpg.FloatProperty(p, value=value))

                elif isinstance(proper, layers_opt.IntRangeProp):  # целочисленый параметр
                    curprop = pg.Append(wxpg.IntProperty(p, value=value))

                elif isinstance(proper, layers_opt.SelectOneProp): # выбор один из многих
                    choices = wxpg.PGChoices()
                    for choice in proper:
                        choices.Add(label=choice, value=wxpg.PG_INVALID_VALUE)
                    default_coice = choices.GetIndicesForStrings([value,])[0]
                    # print(default_coice)
                    curprop = pg.Append(wxpg.EnumProperty(label=p, name=p, choices=choices))
                    curprop.SetChoiceSelection(default_coice)

                if curprop is not None:
                    curprop.SetHelpString(proper.__doc__)
                    pair[curprop] = proper  # свойство wx, свойство CommonProp
        else: # no properties
            print(' No properties')
            empty_prop = pg.Append(wxpg.StringProperty(label='No editable property', value='May be for a while'))
            empty_prop.SetHelpString('Nothing to tweek here')
            pg.Enable(False)
        print('End of filling property grid')

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p:
            print('%s changed to "%s"\n' % (p.GetName(), p.GetValueAsString()))

    def OnPropertySelectionCanged(self, event):
        p = event.GetProperty()
        if p:
            # print(p)
            # print(event)
            current_help = self.wxprop_layerconf_pair[p].www
            self.hyperlink_2.SetURL(current_help)
            self.hyperlink_2.SetToolTip(current_help)

    def OnButtonCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnButtonOK(self, event):
        for wxprop, proper in self.wxprop_layerconf_pair.items():
            if isinstance(proper, layers_opt.BoolProp):  # возвращаем значение дискретного параметра  в layer_conf
                proper(wxprop.GetValue())
                # print(proper.__doc__, wxprop.GetValue())
                # print(proper.__doc__, proper())
            elif isinstance(proper, layers_opt.IntRangeProp):  # целочисленый параметр
                proper(wxprop.GetValue())
                #print(proper.__doc__, wxprop.GetValue())
                #print(proper.__doc__, proper())
            elif isinstance(proper, layers_opt.SelectOneProp):  # выбор один из многих
                proper(wxprop.GetValueAsString())
                #print(proper.__doc__, wxprop.GetValueAsString())
                #print(proper.__doc__, proper())
        self.EndModal(wx.ID_OK)

    def OnClose(self, event):
        # print('Close attempting')
        # print("Changed?", self.property_grid_1.IsPageModified(0))
        if event.CanVeto() and self.property_grid_1.IsPageModified(0):
            if wx.MessageBox("You've made changes... continue closing?",
                             "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
                event.Veto()
                return
        #self.Destroy()  # you may also do:  event.Skip()


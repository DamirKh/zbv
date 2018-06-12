# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version May 24 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class FeederFrame
###########################################################################

class FeederFrame ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Feeder"), pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        self.m_statusBar1 = self.CreateStatusBar( 2, wx.STB_SIZEGRIP, wx.ID_ANY )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_toolBar1 = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
        self.bitmap_button_load = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Load data"), wx.Bitmap( u"glade_gui/icons/inbox_upload.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Load data"), wx.EmptyString, None ) 
        
        self.bitmap_button_show = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Quick show data"), wx.Bitmap( u"glade_gui/icons/chart_curve.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Quick show data"), wx.EmptyString, None ) 
        
        self.bitmap_button_open_model = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Load Model"), wx.Bitmap( u"glade_gui/icons/emotion_surrender.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Load Model"), wx.EmptyString, None ) 
        
        self.bitmap_button_fit = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Feed and fit"), wx.Bitmap( u"glade_gui/icons/emotion_gourmand_big.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Feed and fit"), wx.EmptyString, None ) 
        
        self.m_toolBar1.Realize() 
        
        bSizer1.Add( self.m_toolBar1, 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.Bind( wx.EVT_TOOL, self.on_load_data_btn, id = self.bitmap_button_load.GetId() )
        self.Bind( wx.EVT_TOOL, self.on_show_btn, id = self.bitmap_button_show.GetId() )
        self.Bind( wx.EVT_TOOL, self.on_btn_openmodel, id = self.bitmap_button_open_model.GetId() )
        self.Bind( wx.EVT_TOOL, self.on_btn_fit, id = self.bitmap_button_fit.GetId() )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def on_load_data_btn( self, event ):
        event.Skip()
    
    def on_show_btn( self, event ):
        event.Skip()
    
    def on_btn_openmodel( self, event ):
        event.Skip()
    
    def on_btn_fit( self, event ):
        event.Skip()
    


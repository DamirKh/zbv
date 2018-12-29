# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version May 24 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Sinus", pos = wx.DefaultPosition, size = wx.Size( 260,425 ), style = wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHints( wx.Size( 260,425 ), wx.DefaultSize )
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer4 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        fgSizer2 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer2.AddGrowableCol( 0 )
        fgSizer2.SetFlexibleDirection( wx.HORIZONTAL )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Amplitude", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        fgSizer2.Add( self.m_staticText1, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.m_spinCtrlDouble1 = wx.SpinCtrlDouble( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 2.000000, 1 )
        fgSizer2.Add( self.m_spinCtrlDouble1, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Period", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        fgSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.m_spinCtrlDouble2 = wx.SpinCtrlDouble( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0, 1 )
        fgSizer2.Add( self.m_spinCtrlDouble2, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        self.m_panel1.SetSizer( fgSizer2 )
        self.m_panel1.Layout()
        fgSizer2.Fit( self.m_panel1 )
        bSizer4.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.m_bpButton1 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"glade_gui/icons/sinus.jpeg", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        bSizer4.Add( self.m_bpButton1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )
        
        m_sdbSizer2 = wx.StdDialogButtonSizer()
        self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
        m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
        self.m_sdbSizer2Cancel = wx.Button( self, wx.ID_CANCEL )
        m_sdbSizer2.AddButton( self.m_sdbSizer2Cancel )
        m_sdbSizer2.Realize();
        
        bSizer2.Add( m_sdbSizer2, 1, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.BOTTOM|wx.EXPAND|wx.TOP, 10 )
        
        
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.m_spinCtrlDouble2.Bind( wx.EVT_SPINCTRLDOUBLE, self.OnSpinCtrlDouble )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def OnSpinCtrlDouble( self, event ):
        event.Skip()
    


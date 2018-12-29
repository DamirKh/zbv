#!/usr/bin/env python

import gettext
import logging

import wx

from HE_data_conf import HEMyFrame  # основной гуй программы подготовки данных

# Logging configuration
logging.basicConfig(filename='data_conf.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class App(wx.App):

    def __init__(self, redirect=True, filename=None):
        print("App __init__")
        wx.App.__init__(self, redirect, filename, useBestVisual=True)

    def OnInit(self):
        # Writing to stdout
        print("OnInit")
        # Creating the frame
        self.frame = HEMyFrame(parent=None, id=-1, title='Data configurator')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        # Writing to stderr
        #print("A pretend error message", file=sys.stderr)
        return True

    def OnExit(self):
        print("OnExit")
        return 0


if __name__ == '__main__':
    # (1) Text redirection starts here
    # https://wxpython.org/Phoenix/docs/html/internationalization.html
    gettext.install("app")  # replace with the appropriate catalog name
    app = App(redirect=False)
    print("before MainLoop")
    logging.debug("Logging via logging")
    logging.error('Error via logging')
    # (2) The main event loop is entered here
    app.MainLoop()
    print("after MainLoop")

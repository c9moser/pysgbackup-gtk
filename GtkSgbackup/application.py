
from gi.repository import Gtk,GObject,GLib

import sgbackup

from .appwindow import AppWindow

class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.__sgbackup_app = sgbackup.Application()
        self.sgbackup_app.initialize()
        self.__appwindow = None

    def __del__(self):
        self.sgbackup_app.destroy()

    @GObject.Property
    def appwindow(self):
        return self.__appwindow
    
    @GObject.Property
    def sgbackup_app(self):
        return self.__sgbackup_app
    
    def do_activate(self):
        if self.__appwindow is None:
            self.__appwindow = AppWindow(self,self.sgbackup_app)
            self.appwindow.connect('destroy',self._on_appwindow_destroy)

        self.appwindow.present()

    def _on_appwindow_destroy(self,appwindow):
        if hasattr(self,'__appwindow') and appwindow == self.__appwindow:
            self.__appwindow = None

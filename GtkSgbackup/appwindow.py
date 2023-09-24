
from gi.repository import Gtk,GObject

from .gameview import GameView
from .backupview import BackupView
class AppWindow(Gtk.ApplicationWindow):
    def __init__(self,app,sgbackup_app):
        Gtk.ApplicationWindow.__init__(self,application=app)
        self.__sgbackup_app = sgbackup_app
        self.set_default_size(800,800)
        self.set_resizable(True)
        self.__vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.__vpaned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        self.__gameview = GameView(self.sgbackup_app)
        self.vpaned.set_start_child(self.gameview)
        
        self.__backupview = BackupView(self.gameview)
        self.backupview.attach_to_gameview(self.gameview)
        self.vpaned.set_end_child(self.backupview)
        
        self.vpaned.set_resize_start_child(True)
        self.vpaned.set_resize_end_child(True)
        self.vpaned.set_vexpand(True)
        self.vpaned.set_valign(Gtk.Align.FILL)

        self.vbox.append(self.vpaned)

        self.__statusbar = Gtk.Statusbar()
        self.vbox.append(self.statusbar)

        self.set_child(self.vbox)

    @GObject.Property
    def sgbackup_app(self):
        return self.__sgbackup_app
    
    @GObject.Property
    def vbox(self):
        return self.__vbox
    
    @GObject.Property
    def vpaned(self):
        return self.__vpaned
    
    @GObject.Property
    def gameview(self):
        return self.__gameview
    
    @GObject.Property
    def backupview(self):
        return self.__backupview
    
    @GObject.Property
    def statusbar(self):
        return self.__statusbar
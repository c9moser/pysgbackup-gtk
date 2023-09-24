
from gi.repository import Gtk,GLib,GObject

import os
import datetime
import sgbackup
from . import gameview

class BackupView(Gtk.ScrolledWindow):
    (
        COLUMN_FILENAME,
        COLUMN_PATH,
        CLOMUN_DATE_STRING,
        COLUMN_DATE,
        COLUMN_FINISHED,
    ) = range(5)

    def __init__(self,sgbackup_app:sgbackup.Application):
        Gtk.ScrolledWindow.__init__(self)
        self.__sgbackup_app = sgbackup_app
        self.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.ALWAYS)
        self.__treeview = self.__create_treeview()
        self.__gameview = None
        self.__gameview_slot_selection_changed = None

        self.set_child(self.treeview)

    def __create_model(self):
        def compare_date(model,row1,row2,user_data):
            sort_column, x = model.get_sort_column_id()
            value1 = model.get_value(row1,sort_column)
            value2 = model.get_value(row2,sort_column)

            if value1 < value2:
                return -1
            elif value1 == value2:
                return 0
            else:
                return 1
            
        model = Gtk.ListStore(str,str,str,GObject.TYPE_PYOBJECT,bool)
        model.set_sort_func(self.COLUMN_DATE,compare_date,0)
        return model


    def __create_treeview(self):
        tv = Gtk.TreeView.new_with_model(self.__create_model())

        tvc = Gtk.TreeViewColumn("Finished",Gtk.CellRendererToggle(),active=self.COLUMN_FINISHED)
        tvc.set_sort_column_id(self.COLUMN_FINISHED)
        tv.append_column(tvc)

        tvc = Gtk.TreeViewColumn("Filename",Gtk.CellRendererText(),text=self.COLUMN_FILENAME)
        tvc.set_sort_column_id(self.COLUMN_FILENAME)
        tv.append_column(tvc)

        tvc = Gtk.TreeViewColumn("Date",Gtk.CellRendererText(),text=self.CLOMUN_DATE_STRING)
        tvc.set_sort_column_id(self.COLUMN_DATE)
        tv.append_column(tvc)

        return tv
    
    @GObject.Property
    def treeview(self):
        return self.__treeview
    
    @GObject.Property
    def sgbackup_app(self):
        return self.__sgbackup_app

    @GObject.Property
    def gameview(self):
        return self.__gameview
    
    def attach_to_gameview(self,gameview):
        if self.__gameview is not None:
            if self.__gameview_slot_selection_changed is not None:
                self.__gameview.treeview.get_selection().disconnect('changed',self.__gameview_slot_selection_changed)
                self.__gameview_slot_selection_changed = None
            self.__gameview = None

        self.__gameview = gameview
        self.__gameview_slot_selection_changed = self.gameview.treeview.get_selection().connect('changed',self._on_gameview_selection_changed)
        self._on_gameview_selection_changed(self.gameview.treeview.get_selection())

    def _on_gameview_selection_changed(self,selection):
        gv_model, gv_iter = selection.get_selected()
        bv_model = self.treeview.get_model()
        if (bv_model):
            bv_model.clear()
        else:
            bv_model = self.__create_model()
            self.treeview.set_model(bv_model)

        if gv_iter is not None and gv_model.iter_is_valid(gv_iter):
            game = gv_model[gv_iter][gameview.GameView.COLUMN_GAME]
            for bf in game.backups:
                if not os.path.exists(bf):
                    continue

                filename = os.path.basename(bf)
                if filename.startswith("{}.finished.".format(game.savegame_name)):
                    finished = True
                else:
                    finished = False

                try:
                    stat = os.stat(bf)
                    timestamp = datetime.datetime.fromtimestamp(stat.st_ctime)
                except:
                    continue
                
                bv_model.append((filename,bf,timestamp.ctime(),timestamp,finished))

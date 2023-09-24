from gi.repository import Gtk,GObject
import sgbackup
class GameView(Gtk.ScrolledWindow):
    (
        COLUMN_GAME_ID,
        COLUMN_GAME_NAME,
        COLUMN_SAVEGAME_NAME,
        COLUMN_SAVEGAME_ROOT,
        COLUMN_SAVEGAME_DIR,
        COLUMN_INSTALLDIR,
        COLUMN_STEAM_APPID,
        COLUMN_FINISHED,
        COLUMN_GAME        
    ) = range(9)

    def __init__(self,sgbackup_app:sgbackup.Application):
        Gtk.ScrolledWindow.__init__(self)
        self.__sgbackup_app = sgbackup_app
        self.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.ALWAYS)
        self.__treeview = self.__create_treeview()
        self.set_child(self.treeview)

    def __create_treemodel(self):
        model = Gtk.ListStore(
            str, # game id
            str, # game name
            str, # backup name
            str, # backup root
            str, # backup dir
            str, # installdir
            int, # steam appid
            bool, # finished
            GObject.TYPE_PYOBJECT, # Game instance
        )

        for game in self.sgbackup_app.games.games:
            model.append((
                game.game_id,
                game.game_name,
                game.savegame_name,
                game.savegame_root,
                game.savegame_dir,
                game.installdir,
                game.steam_appid,
                game.is_finished,
                game))

        return model
    
    def __create_treeview(self):
        tv = Gtk.TreeView.new_with_model(self.__create_treemodel())

        tvc = Gtk.TreeViewColumn("ID",Gtk.CellRendererText(),text=self.COLUMN_GAME_ID)
        tvc.set_sort_column_id(self.COLUMN_GAME_ID)
        tv.append_column(tvc)

        tvc = Gtk.TreeViewColumn("Name",Gtk.CellRendererText(),text=self.COLUMN_GAME_NAME)
        tvc.set_sort_column_id(self.COLUMN_GAME_NAME)
        tv.append_column(tvc)

        tvc = Gtk.TreeViewColumn("Finished",Gtk.CellRendererToggle(),active=self.COLUMN_FINISHED)
        tvc.set_sort_column_id(self.COLUMN_FINISHED)
        tv.append_column(tvc)

        tvc = Gtk.TreeViewColumn("SaveGame name",Gtk.CellRendererText(),text=self.COLUMN_SAVEGAME_NAME)
        tvc.set_sort_column_id(self.COLUMN_SAVEGAME_NAME)
        tv.append_column(tvc)

        tvc = Gtk.TreeViewColumn("Steam AppID",Gtk.CellRendererText(),text=self.COLUMN_STEAM_APPID)
        tvc.set_sort_column_id(self.COLUMN_STEAM_APPID)
        tv.append_column(tvc)

        return tv
    
    @GObject.Property
    def treeview(self):
        return self.__treeview
    
    @GObject.Property
    def sgbackup_app(self):
        return self.__sgbackup_app
    
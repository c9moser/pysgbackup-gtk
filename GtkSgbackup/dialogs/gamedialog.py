
from gi.repository import Gtk,GObject
import sgbackup

class GameDialog(Gtk.Dialog):
    def __init__(self,parent:Gtk.Window,sgbackup_app:sgbackup.Application,game=None):
        Gtk.Dialog.__init__(self,"GtkSgbackup: Game",parent)
        self.__sgbackup_app = sgbackup_app

        if game is not None and not isinstance(game,sgbackup.game.Game):
            raise TypeError("game is not an sgbackup.game.Game instance!")
        self.__initial_game = game

        self.__game_id_entry = Gtk.Entry()
        self.__game_name_entry = Gtk.Entry()
        self.__savegame_name_entry = Gtk.Entry()
        self.__savegame_root_entry = Gtk.Entry()
        self.__savegame_root_button = Gtk.Button()
        self.__savegame_dir_entry = Gtk.Entry()
        self.__savegame_dir_button = Gtk.Button()
        self.__steam_appid_entry = Gtk.Entry()

        if self.initial_game:
            self.__game_id_entry.set_text(self.initial_game.game_id)
            self.__game_name_entry.set_text(self.initial_game.game_name)
            self.__savegame_name_entry.set_text(self.initial_game.savegame_name)
            self.__savegame_root_entry.set_text(self.initial_game.savegame_root_template)
            self.__savegame_dir_entry.set_text(self.initial_game.savegame_dir_template)
            if self.initial_game.steam_appid:
                self.__steam_appid_entry.set_text(str(self.__initial_game.steam_appid))

    @GObject.Property
    def initial_game(self):
        return self.__initial_game
    
    @GObject.Property
    def is_valid(self):
        if (self.game_id and self.game_name and self.savegame_name and self.savegame_dir and self.savegame_root):
            return True
        return False
    
    @GObject.Property
    def game(self):
        if not self.is_valid:
            return None
        if self.initial_game:
            self.initial_game.game_name = self.game_name
            self.initial_game.savegame_name = self.savegame_name
            self.initial_game.savegame_root = self.savegame_root
            self.initial_game.savegame_dir = self.savegame_dir
            self.initial_game.steam_appid = self.steam_appid
            if self.initial_game.game_id != self.game_id:
                self.initial_game.game_id = self.game_id

            return self.initial_game
        
        return sgbackup.game.Game(
            self.sgbackup_app,
            self.game_id,
            self.game_name,
            savegame_name=self.savegame_name,
            savegame_root=self.savegame_root,
            savegame_dir=self.savegame_dir,
            steam_appid=self.steam_appid)

    @GObject.Property
    def sgbackup_app(self):
        return self.__sgbackup_app
    
    @GObject.Property
    def game_id(self):
        return self.__game_id_entry.get_text()
    @game_id.setter
    def game_id(self,id:str)
        self.__game_id_entry.set_text(id)

    @GObject.Property
    def game_name(self):
        return self.__game_name_entry.get_text()
    @game_name.setter
    def game_name(self,name:str):
        self.__game_name_entry.set_text(name)

    @GObject.Property
    def savegame_name(self):
        return self.__savegame_name_entry.get_text()
    @savegame_name.setter
    def savegame_name(self,sgname:str):
        self.__savegame_name_entry.set_text(sgname)
    
    @GObject.Property
    def savegame_root(self):
        return self.__savegame_root_entry.get_text()
    @savegame_root.setter
    def savegame_root(self,sgroot:str):
        self.__savegame_root_entry.set_text(sgroot)

    @GObject.Property
    def savegame_dir(self):
        return self.__savegame_dir_entry.get_text()
    @savegame_dir.setter
    def savegame_dir(self,sgdir:str)
        self.__savegame_dir_entry.set_text(sgdir)

    @GObject.Property
    def steam_appid(self):
        try:
            text = self.__steam_appid_entry.get_text()
            if not text:
                return 0
            return int(text)
        except:
            return 0
    @steam_appid.setter
    def steam_appid(self,appid:int):
        if appid < 0:
            appid = 0
        if appid == 0:
            self.__steam_appid_entry.set_text("")
        else:
            self.__steam_appid_entry.set_text(int(appid))
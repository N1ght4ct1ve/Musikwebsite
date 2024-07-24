# app/lib/shared.py
from app.globals import Globals
from app.lib.vlc_player import MusicPlayer

player = MusicPlayer(Globals.SONG_FOLDER)

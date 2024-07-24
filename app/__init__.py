import base64
import os
from flask import Flask

from app.globals import Globals
from app.lib.shared import player
from app.lib.helpers import update_queue
from app.lib.helpers import *

def create_app():
    initialize_player()

    app = Flask(__name__)
    app.secret_key = generate_secret_key()
    app.config.update(TEMPLATES_AUTO_RELOAD = True)

    from .main.routes import main_bp
    from .musicplayer.routes import musicplayer_bp

    update_queue()  # Call to update_queue where needed

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(musicplayer_bp, url_prefix='/musicplayer')



    return app

def generate_secret_key():
    random_bytes = os.urandom(24)
    secret_key = base64.b64encode(random_bytes).decode('utf-8')
    return secret_key

# app/lib/shared.py
def initialize_player():
    from app.globals import Globals
    from app.lib.vlc_player import MusicPlayer
    global player
    player = MusicPlayer(Globals.SONG_FOLDER)
    player.register_event("song_end", on_song_end)
    player.register_event("song_start", on_song_start)
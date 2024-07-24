from app import create_app


from app.globals import Globals
from app.lib.helpers import *
from app.lib import vlc_player
from app.musicplayer.routes import update_queue

app = create_app()

if __name__ == '__main__':

    if not os.path.exists(Globals.SONG_FOLDER):
        os.makedirs(Globals.SONG_FOLDER)

    

    app.run(port=5000, debug=True)

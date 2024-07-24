import re
from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from PIL import Image
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

#####Global variablen
from app.globals import Globals
from app.lib.helpers import *
from app.lib.youtube_downloader import download_from_youtube # Eigene Funktion :D
from app import player

musicplayer_bp = Blueprint('musicplayer', __name__)

@musicplayer_bp.route('/')
def index():
    mp3_files = []
    for file in os.listdir(Globals.SONG_FOLDER):
        if file.endswith(".mp3"):
            mp3_files.append(file[:-4])
        mp3_files = sorted(mp3_files)
    update_song()
    return render_template(Globals.html_dir_musicplayer+"musicplayer.html", playback_queue=Globals.current_queue, files=mp3_files, current_song=Globals.current_song)

@musicplayer_bp.route('/queue')
def get_queue():
    queue = player.get_queue()
    update_song()
    return jsonify({"queue": Globals.current_queue, "current_song": Globals.current_song})

@musicplayer_bp.route('/upload', methods=['POST'])
def upload_file():
    print(request)
    file = request.files['file']
    if file and file.filename.endswith('.mp3'):
        file_path = os.path.join(Globals.SONG_FOLDER, file.filename)
        file.save(file_path)
    else:
        if request.form['string'] == 'true':
            url = request.form['url']
            if not url:
                return render_template(Globals.html_dir_errors+'error.html', error_message="Keine URL angegeben."), 400

            if url and (url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/") or url.startswith("https://music.youtube.com/watch?v=")):
                result = download_from_youtube(url, Globals.SONG_FOLDER)

                if 'error' in result:
                    return render_template(Globals.html_dir_errors+'error.html', error_message=f"Fehler: {result['error']}"), 400
                else:
                    title = result.get('title', None)
                    add_to_queue(title)
    return redirect(url_for('index'))

@musicplayer_bp.route('/download', methods=['POST'])
def download_file():
    url = request.form['url']
    if not url:
        return render_template(Globals.html_dir_errors+'error.html', error_message="Keine URL angegeben."), 400

    if url and (url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/") or url.startswith("https://music.youtube.com/watch?v=")):
        result = download_from_youtube(url, Globals.SONG_FOLDER)

        if 'error' in result:
            return render_template(Globals.html_dir_errors+'error.html', error_message=f"Fehler: {result['error']}"), 400
        else:
            title = result.get('title', None)
            add_to_queue(title)
    else:
        return render_template(Globals.html_dir_errors+'error.html', error_message="Ungültige URL. Bitte geben Sie eine gültige YouTube-URL ein."), 400
    return redirect(url_for('index'))

@musicplayer_bp.route('/enqueue', methods=['POST'])
def enqueue_file():
    file = request.data.decode('utf-8')
    add_to_queue(file)
    return redirect(url_for('index'))

@musicplayer_bp.route('/start', methods=['POST'])
def start():
    print(50*"-")
    print(f"Hab Start Command bekommen \n braucht man grad aber nicht")
    print(50*"-")
    return '', 204

@musicplayer_bp.route('/resume', methods=['POST'])
def resume():
    update_queue()
    if Globals.current_queue:
        update_song(Globals.current_queue[0])
        player.play()
    return '', 204

@musicplayer_bp.route('/pause', methods=['POST'])
def stop():
    player.pause()
    return '', 204

@musicplayer_bp.route('/setvolume', methods=['POST'])
def set_volume():
    volume = request.data.decode('utf-8')
    try: 
        volume = int(volume)
    except:
        volume = 100
    if volume <= 150:
        player.set_volume(volume)
    return '', 204

@musicplayer_bp.route('/skip', methods=['POST'])
def skip():
    update_song(player.get_queue()[0])
    player.skip()
    update_queue()
    return '', 204

@musicplayer_bp.errorhandler(404)
def page_not_found(e):
    return render_template(Globals.html_dir_errors+'404.html'), 404




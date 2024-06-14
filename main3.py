# Importiert notwendige Module und Pakete
from flask import Flask, request, render_template, redirect, url_for, jsonify
import yt_dlp as youtube_dl
import os
import re
from threading import Thread, Event
from queue import Queue
import vlc_player
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import traceback
from PIL import Image

# Initialisiert die Flask-App
app = Flask(__name__)

# Legt den Ordner für Music fest und erstellt ihn, falls er nicht existiert
SONG_FOLDER = 'music/'
TEMP_IMG = 'static/temp/'
WORDS_TO_REMOVE = ['official video', 'lyric video', 'audio', 'music video']


if not os.path.exists(SONG_FOLDER):
    os.makedirs(SONG_FOLDER)

# Initialisiert eine Warteschlange für Dateien, eine Wiedergabeliste und Variablen für das aktuelle Lied
queue = Queue()
playback_queue = []
current_song = {"title": "", "cover": ""}


""" ---- Hilfsfunktionen ---- """

def add_to_queue(title):
    player.add_to_queue(title)

    print(50*"-")
    print(player.get_queue()) # Kann iwann weg
    print(50*"-")

# Hilfsfunktion zur Bereinigung des Titels (Noch unnötig)
def clean_title(title):
    cleaned_title = title
    for word in WORDS_TO_REMOVE:
        cleaned_title = cleaned_title.replace(word, '')
    cleaned_title = clean_title_with_regex(cleaned_title)
    return cleaned_title.strip()

def clean_title_with_regex(title):
    # Beispiel-Regex: Entfernt alles, was in runden Klammern steht (Noch unnötig)
    cleaned_title = re.sub(r'\(.*?\)', '', title)
    return cleaned_title.strip()

def download_from_youtube(url):
    ydl_opts = {
        'verbose': True,
        'format': 'mp3/bestaudio/best',
        'outtmpl': os.path.join(SONG_FOLDER, '%(title)s.%(ext)s'),
        'writethumbnail': True,
        'embedthumbnail': True,
        'postprocessors': [{
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        },
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality' : 'best',
        },
        {
            'key': 'EmbedThumbnail',
        },
        ]
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.download([url])
    
    return info


# Funktion zum Anpassen des Seitenverhältnisses der Thumbnails
def adjust_thumbnail(thumbnail_path, output_path, desired_ratio=(1, 1)):
    with Image.open(thumbnail_path) as img:
        # Größe des Bildes berechnen, um das gewünschte Seitenverhältnis zu erhalten
        width, height = img.size
        desired_width, desired_height = desired_ratio
        aspect_ratio = desired_width / desired_height

        if width / height > aspect_ratio:
            new_width = int(height * aspect_ratio)
            new_height = height
        else:
            new_width = width
            new_height = int(width / aspect_ratio)

        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        # Bild zuschneiden und speichern
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save(output_path)

""" ---- HTML Funktionen ---- """


# Definiert die Route für die Startseite
@app.route('/')
def index():
    # Listet alle Dateien im Upload-Ordner auf und rendert das Index-Template
    mp3_files = []
    for file in os.listdir(SONG_FOLDER):
        # Prüfen, ob die Dateiendung ".mp3" ist
        if file.endswith(".mp3"):
            mp3_files.append(file[:-4])
        mp3_files = sorted(mp3_files)
    return render_template("index.html", playback_queue=playback_queue, files=mp3_files, current_song=current_song)


# Definiert die Route zum Abrufen der Warteschlange
@app.route('/queue')
def get_queue():
    queue = player.get_queue()
    # Gibt die aktuelle Wiedergabeliste und das aktuelle Lied als JSON zurück
    return jsonify({"queue": queue, "current_song": current_song})


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.mp3'):
        file_path = os.path.join(SONG_FOLDER, file.filename)
        file.save(file_path)

    else:
        #return jsonify({"error": "Invalid file format"}), 400
        return render_template('error.html', error_message="Ungültiges Dateiformat. Bitte laden Sie nur MP3-Dateien hoch."), 400
    return redirect(url_for('index'))



@app.route('/download', methods=['POST'])
def download_file():
    url = request.form['url']
    if url and ("youtube.com" or "youtu.be" in url):
        info_dict = download_from_youtube(url)
        title = info_dict.get('title', None)
        add_to_queue(title)
    else:
        #return jsonify({"error": "Invalid URL"}), 400
        return render_template('error.html', error_message="Ungültige URL. Bitte geben Sie eine gültige YouTube-URL ein."), 400
    return redirect(url_for('index'))


# Definiert die Route zum Einreihen von Dateien in die Wiedergabeliste
@app.route('/enqueue', methods=['POST'])
def enqueue_file():
    print(request)
    file = request.data.decode('utf-8')
    print(file)
    player.add_to_queue(file)
    return redirect(url_for('index'))

# Definiert die Route zum Starten der Wiedergabe
@app.route('/start', methods=['POST'])
def start():
    print(50*"-")
    print("Hab Start Command bekommen")
    print(50*"-")
    player.play()
    return '', 204

# Definiert die Route zum Starten der Wiedergabe
@app.route('/resume', methods=['POST'])
def resume():
    print(50*"-")
    print("Hab Resume Command bekommen")
    print(50*"-")
    player.pause()
    return '', 204

# Definiert die Route zum Stoppen der Wiedergabe
@app.route('/pause', methods=['POST'])
def stop():
    print(50*"-")
    print("Hab Pause Command bekommen")
    print(50*"-")
    player.pause()
    return '', 204


# Definiert die Route zum Überspringen des aktuellen Liedes
@app.route('/skip', methods=['POST'])
def skip():
    print(50*"-")
    print("Hab Skip Command bekommen")
    print(50*"-")
    player.skip()

    return '', 204


# Definiert eine benutzerdefinierte Fehlerseite für den HTTP-Statuscode 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Funktion zur Wiedergabe von Audio
def play_audio():
    
    print("Ich tu so, als ob ich Audio abspiele! :D ")
       


# Startet die Flask-App und den Audio-Player-Thread
if __name__ == '__main__':
    # Definiert den Audio-Player-Thread
    player = vlc_player.MusicPlayer(SONG_FOLDER)

    
    # Startet die Flask-App
    app.config.update(
        TEMPLATES_AUTO_RELOAD = True
    )
    app.register_error_handler(404, page_not_found)  # Registriert die benutzerdefinierte Fehlerseite
    app.run(host='0.0.0.0', port=5000)

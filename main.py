# Importiert notwendige Module und Pakete
from flask import Flask, request, render_template, redirect, url_for, jsonify
import yt_dlp as youtube_dl
import os
from threading import Thread, Event
from queue import Queue
from pydub import AudioSegment
import simpleaudio as sa
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import traceback
from PIL import Image

# Initialisiert die Flask-App
app = Flask(__name__)

# Legt den Ordner für Music fest und erstellt ihn, falls er nicht existiert
SONG_FOLDER = 'music'
TEMP_IMG = 'static/temp/'
if not os.path.exists(SONG_FOLDER):
    os.makedirs(SONG_FOLDER)

# Initialisiert eine Warteschlange für Dateien, eine Wiedergabeliste und Variablen für das aktuelle Lied
queue = Queue()
playback_queue = []
current_song = {"title": "", "cover": ""}

# Initialisiert Events zum Stoppen und Überspringen von Liedern
stop_event = Event()
skip_event = Event()

# Definiert die Route für die Startseite
@app.route('/')
def index():
    # Listet alle Dateien im Upload-Ordner auf und rendert das Index-Template
    mp3_files = []
    for file in os.listdir(SONG_FOLDER):
        # Prüfen, ob die Dateiendung ".mp3" ist
        if file.endswith(".mp3"):
            mp3_files.append(file)
        mp3_files = sorted(mp3_files)
        
    return render_template("index.html", playback_queue=playback_queue, files=mp3_files, current_song=current_song)

# Definiert die Route zum Abrufen der Warteschlange
@app.route('/queue')
def get_queue():
    # Gibt die aktuelle Wiedergabeliste und das aktuelle Lied als JSON zurück
    return jsonify({"queue": playback_queue, "current_song": current_song})

"""# Definiert die Route zum Hochladen von Dateien
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(SONG_FOLDER, file.filename)
        file.save(file_path)
        queue.put(file_path)
        playback_queue.append(file.filename)
    return redirect(url_for('index'))"""

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.mp3'):
        file_path = os.path.join(SONG_FOLDER, file.filename)
        file.save(file_path)
        queue.put(file_path)
        playback_queue.append(file.filename)
    else:
        #return jsonify({"error": "Invalid file format"}), 400
        return render_template('error.html', error_message="Ungültiges Dateiformat. Bitte laden Sie nur MP3-Dateien hoch."), 400
    return redirect(url_for('index'))

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

"""# Definiert die Route zum Herunterladen von Dateien von YouTube
@app.route('/download', methods=['POST'])
def download_file():
    url = request.form['url']
    if url:
        info_dict = download_from_youtube(url)
        title = info_dict.get('title', None)
        add_to_queue(title)
        #thumbnail = info_dict.get('thumbnail', None)
        #if title:

    return redirect(url_for('index'))"""

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



def add_to_queue(title):
    file_path = os.path.join(SONG_FOLDER, f"{title}.mp3")
    queue.put(file_path)
    playback_queue.append(f"{title}.mp3")




# Definiert die Route zum Einreihen von Dateien in die Wiedergabeliste
@app.route('/enqueue', methods=['POST'])
def enqueue_file():
    file = request.form['file']
    if file:
        file_path = os.path.join(SONG_FOLDER, file)
        queue.put(file_path)
        playback_queue.append(file)
    return redirect(url_for('index'))

# Definiert die Route zum Starten der Wiedergabe
@app.route('/start', methods=['POST'])
def start():
    if not player_thread.is_alive():
        player_thread.start()
    return '', 204

# Definiert die Route zum Stoppen der Wiedergabe
@app.route('/stop', methods=['POST'])
def stop():
    stop_event.set()
    return '', 204

# Definiert die Route zum Überspringen des aktuellen Liedes
@app.route('/skip', methods=['POST'])
def skip():
    skip_event.set()
    return '', 204

# Definiert eine benutzerdefinierte Fehlerseite für den HTTP-Statuscode 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


""""""
# Funktion zur Wiedergabe von Audio
def play_audio():
    while True:
        stop_event.clear()
        skip_event.clear()
        file_path = queue.get()
        if file_path:
            playback_queue.remove(os.path.basename(file_path))
            current_song["title"] = os.path.basename(file_path)
            # Extrahiert das Cover-Bild, falls vorhanden
            audio = MP3(file_path, ID3=ID3)
            if audio.tags.getall("APIC"):
                for tag in audio.tags.getall("APIC"):
                    if tag.type == 3:  # Vorderes Cover
                        cover_path = os.path.join(TEMP_IMG, f"{current_song['title'][:-3]}.jpg")
                        
                        #cover_path = os.path.join(TEMP_IMG, f"temp.jpg")
                        with open(cover_path, 'wb') as img:
                            img.write(tag.data)
                        adjust_thumbnail(cover_path,cover_path)
                        current_song["cover"] = cover_path
                        break
            else:
                current_song["cover"] = ""
            song = AudioSegment.from_mp3(file_path)
            try:
                play_obj = sa.play_buffer(
                    song.raw_data,
                    num_channels=song.channels,
                    bytes_per_sample=song.sample_width,
                    sample_rate=song.frame_rate
                )
                while play_obj.is_playing():
                    if stop_event.is_set():
                        play_obj.stop()
                        return
                    if skip_event.is_set():
                        play_obj.stop()
                        break
                play_obj.wait_done()
            except Exception as e:
                # Protokolliere den Fehler und fahre mit der Wiedergabe des nächsten Songs fort
                print(f"Fehler beim Abspielen von '{current_song['title']}': {e}")
                traceback.print_exc()  # Protokolliere die Stack-Trace-Informationen
                continue

# Startet die Flask-App und den Audio-Player-Thread
if __name__ == '__main__':
    # Definiert den Audio-Player-Thread
    player_thread = Thread(target=play_audio, daemon=True)
    player_thread.start()
    
    # Startet die Flask-App
    app.register_error_handler(404, page_not_found)  # Registriert die benutzerdefinierte Fehlerseite
    app.run(host='0.0.0.0', port=5000)

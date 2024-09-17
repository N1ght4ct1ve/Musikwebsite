# Importiert notwendige Module und Pakete
import os
import re
import vlc_player # Eigene Funktion :D
from PIL import Image
from youtube_downloader import download_from_youtube # Eigene Funktion :D
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
# from threading import Thread, Event
from flask import Flask, request, render_template, redirect, url_for, jsonify


# Initialisiert die Flask-App
app = Flask(__name__)

# Legt den Ordner für Music fest und erstellt ihn, falls er nicht existiert
SONG_FOLDER = 'music/'
TEMP_IMG = 'static/temp/'
WORDS_TO_REMOVE = ['official video', 'lyric video', 'audio', 'music video']
current_song = {"title": "", "cover": ""}
current_queue = []

if not os.path.exists(SONG_FOLDER):
    os.makedirs(SONG_FOLDER)



""" ---- Hilfsfunktionen ---- """
def add_to_queue(title):
    player.add_to_queue(title)
    update_queue()


def update_queue():
    global current_queue
    current_queue = player.get_queue()
    print(50*"-")
    print(current_queue)
    print(50*"-")

def update_song(song = None):
    global current_song
    neuer_song = player.current_song()
    if neuer_song:
            current_song["title"] = neuer_song
            update_cover(neuer_song)
    elif song:
        current_song["title"] = song
        update_cover(song)
    else:
        current_song["title"] = "No song yet"
        current_song["cover"] = "static/temp/default.png"

    
    # print(50*"-")
    # print(current_song)
    # print(50*"-")


def on_song_end(song_title):
    print(f"Callback: Lied beendet - {song_title}")

def on_song_start(song_title):
    print(f"Callback: Lied startet - {song_title}")
    update_song()



def update_cover(song):
    global current_song
    # Extrahiert das Cover-Bild, falls vorhanden
    audio = MP3(f"{SONG_FOLDER}/{song}.mp3", ID3=ID3)
    if audio.tags.getall("APIC"):
        for tag in audio.tags.getall("APIC"):
            if tag.type == 3:  # Vorderes Cover
                cover_path = os.path.join(TEMP_IMG, f"{current_song['title']}.jpg")
                try:
                    with open(cover_path, 'wb') as img:
                        img.write(tag.data)
                    adjust_thumbnail(cover_path, cover_path)  # Passt das Thumbnail an
                    current_song["cover"] = cover_path
                    break
                except:
                    current_song["cover"] = "static/temp/default.png"  # Setzt das Cover auf leer, wenn keins vorhanden ist
                    break
    else:
        current_song["cover"] = "static/temp/default.png"  # Setzt das Cover auf leer, wenn keins vorhanden ist
    


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
    #update_song()
    return render_template("index.html", playback_queue=current_queue, files=mp3_files, current_song=current_song)


# Definiert die Route zum Abrufen der Warteschlange
@app.route('/queue')
def get_queue():
    queue = player.get_queue()
    #update_song()
    # Gibt die aktuelle Wiedergabeliste und das aktuelle Lied als JSON zurück
    return jsonify({"queue": current_queue, "current_song": current_song})


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.mp3'):
        file_path = os.path.join(SONG_FOLDER, file.filename)
        file.save(file_path)

    else:
        return render_template('error.html', error_message="Ungültiges Dateiformat. Bitte lade nur MP3-Dateien hoch."), 400
    return redirect(url_for('index'))



@app.route('/download', methods=['POST'])
def download_file():
    url = request.form['url']

    if not url:
        return render_template('error.html', error_message="Keine URL angegeben."), 400

    if url and url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/") or url.startswith("https://music.youtube.com/watch?v="):
        result = download_from_youtube(url, SONG_FOLDER)

        if 'error' in result:
            print(f"Fehler: {result['error']}")
            return render_template('error.html', error_message=f"Fehler: {result['error']}"), 400
        else:
            print(f"Erfolgreich heruntergeladen: {result['title']}")
            title = result.get('title', None)
            add_to_queue(title)

    else:
        #return jsonify({"error": "Invalid URL"}), 400
        return render_template('error.html', error_message="Ungültige URL. Bitte gib eine gültige YouTube-URL ein."), 400
    return redirect(url_for('index'))


# Definiert die Route zum Einreihen von Dateien in die Wiedergabeliste
@app.route('/enqueue', methods=['POST'])
def enqueue_file():
    file = request.data.decode('utf-8')
    print(f"Neuer Song für die Queue: {file}")
    add_to_queue(file)
    
    return redirect(url_for('index'))



# Definiert die Route zum Starten der Wiedergabe
@app.route('/resume', methods=['POST'])
def resume():
    global current_queue
    print(50*"-")
    print("Hab Resume Command bekommen")
    print(50*"-")
    
    print(f"Aktueller song: {player.current_song()}")
    update_queue()
    if current_queue:
        #update_song(current_queue[0])
        player.play()
    return '', 204

# Definiert die Route zum Stoppen der Wiedergabe
@app.route('/pause', methods=['POST'])
def stop():
    print(50*"-")
    print("Hab Pause Command bekommen")
    print(50*"-")
    player.pause()
    return '', 204

# Definiert die Route zur Lautstärkeänderung der Wiedergabe
@app.route('/setvolume', methods=['POST'])
def set_volume():
    volume = request.data.decode('utf-8')
    print(volume)
    try: 
        volume = int(volume)
    except:
        print("Irgendwer hat Volume verkackt")
        volume = 100
    if volume <= 150:
        player.set_volume(volume)


    print(50*"-")
    print("Hab Lautstärke Command bekommen")
    print(50*"-")
    return '', 204



# Definiert die Route zum Überspringen des aktuellen Liedes
@app.route('/skip', methods=['POST'])
def skip():
    print(50*"-")
    print("Hab Skip Command bekommen")
    print(50*"-")
    #update_song(player.get_queue()[0])
    player.skip()
    update_queue()

    return '', 204


# Definiert die Route zum LoopTogglen des aktuellen Liedes
@app.route('/toggle_loop', methods=['POST'])
def toggle_loop():
    print(50*"-")
    print("Hab LoopToggle Command bekommen")
    print(50*"-")
    #update_song(player.get_queue()[0])
    player.toggle_loop()
    update_queue()
    return '', 204


# Definiert die Route zum Shuffle der aktuellen Queue
@app.route('/toggle_shuffle', methods=['POST'])
def toggle_shuffle():
    print(50*"-")
    print("Hab Shuffle Command bekommen")
    print(50*"-")
    player.toggle_shuffle()
    update_queue()

    return '', 204

# Definiert eine benutzerdefinierte Fehlerseite für den HTTP-Statuscode 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



# Startet die Flask-App und den Audio-Player-Thread
if __name__ == '__main__':
    # Definiert den Audio-Player-Thread
    player = vlc_player.MusicPlayer(SONG_FOLDER)
    update_queue()
    player.register_event("song_end", on_song_end)
    player.register_event("song_start", on_song_start)
    
    # Startet die Flask-App
    app.config.update(
        TEMPLATES_AUTO_RELOAD = True
    )
    app.register_error_handler(404, page_not_found)  # Registriert die benutzerdefinierte Fehlerseite
    app.run(host='0.0.0.0', port=80)

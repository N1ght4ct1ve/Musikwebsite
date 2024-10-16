# Importiert notwendige Module und Pakete
import os
import re
import threading # Mal schauen, ob es klappt
import vlc_player # Eigene Funktion :D
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from youtube_downloader import download_from_youtube, get_title_from_youtube # Eigene Funktion :D
from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from youtubesearchpython import VideosSearch # Braucht man um Songs mit dem Namen zu suchen
from dotenv import load_dotenv


port = input("Bitte gib den Port ein, auf dem der Server laufen soll (Standard: 80, geht auf Linux nicht richtig): ")

if os.path.exists(".env"):
    print(f".env Datei existiert bereits")
    load_dotenv()
    spotify_available = bool(os.getenv('AVAILABLE'))
else:
    spotify_available = False
    client_id = "12345"
    client_secret = "12345"

    available = input("Willst du Spotify Links nutzen können? (Ja/Nein): ")
    if (available.lower() in "ja") or (available.lower() in "yes"):
        spotify_available = True
        client_id = input("Bitte gib deinen Spotify Client ID ein: ")
        client_secret = input("Bitte gib deinen Spotify Client Secret ein: ")
    default_values = {
        "AVAILABLE": spotify_available,
        "CLIENT_ID": client_id,
        "CLIENT_SECRET": client_secret,
    }
    with open(".env", "w") as file:
        for key, value in default_values.items():
            file.write(f"{key}={value}\n")
    print(f".env wurde erstellt {'und Spotify wurde aktiviert.' if spotify_available else 'aber Spotify ist nicht verfügbar'}")
   
if spotify_available:
        from spotify_search import get_track_info # Eigenes Modul zum Suchen von Spotify-Songs (Spotify API und spotipy ()`pip install spotipy`) erforderlich)

# Initialisiert die Flask-App
app = Flask(__name__)

# Legt den Ordner für Music fest und erstellt ihn, falls er nicht existiert
SONG_FOLDER = 'music/'
TEMP_IMG = 'static/temp/'
current_song = {"title": "", "cover": ""}
current_queue = []
download_queue = []

# Erstellt den Ordner für die Musikdateien, falls er nicht existiert
if not os.path.exists(SONG_FOLDER):
    os.makedirs(SONG_FOLDER)



""" ---- Hilfsfunktionen ---- """
# Funktion zum Hinzufügen eines Songs zur Player Warteschlange
def add_to_queue(title):
    player.add_to_queue(title)
    update_queue()

# Funktion zum Aktualisieren der globalen Warteschlange
def update_queue():
    global current_queue
    current_queue = player.get_queue()
    print(50*"-")
    print(current_queue)
    print(50*"-")

# Funktion zum Aktualisieren des aktuellen Songs der globalen Variable
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

# Callback-Funktion, die aufgerufen wird, wenn ein Lied beendet wurde
def on_song_end(song_title):
    print(f"Callback: Lied beendet - {song_title}")

# Callback-Funktion, die aufgerufen wird, wenn ein neues Lied gestartet wird
def on_song_start(song_title):
    print(f"Callback: Lied startet - {song_title}")
    update_song()

# Funktion zum Aktualisieren des Covers eines Songs
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

# Funktion zum Herunterladen von Songs von YouTube
def start_downloads():
    # Wenn die Download-Warteschlange leer ist, nichts tun
    if not download_queue:
        return

    # Nehme den ersten Song aus der Warteschlange
    url = download_queue.pop(0)

    if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/") or url.startswith("https://music.youtube.com/watch?v="):
        result = download_from_youtube(url, SONG_FOLDER)

        if 'error' in result:
            print(f"Fehler: {result['error']}")
            # Hier könntest du den Status aktualisieren, wenn der Download fehlschlägt
        else:
            print(f"Erfolgreich heruntergeladen: {result['title']}")
            title = result.get('title', None)
            add_to_queue(title)

    elif url.startswith("https://open.spotify.com/"):
        if not spotify_available:
            print("Spotify ist nicht aktiviert.")
            return
        
        if url.startswith("https://open.spotify.com/playlist/"):
            print("Spotify Playlists sind nicht unterstützt.")
            return
        else:
            song_name, artist = get_track_info(url)
            videosSearch = VideosSearch(f"{song_name} {artist}", limit=2)
            link = videosSearch.result()['result'][0]['link']
            result = download_from_youtube(link, SONG_FOLDER)
            if 'error' in result:
                print(f"Fehler: {result['error']}")
            else:
                print(f"Erfolgreich heruntergeladen: {result['title']}")
                title = result.get('title', None)
                add_to_queue(title)

    else:
        videosSearch = VideosSearch(url, limit=2)
        url = videosSearch.result()['result'][0]['link']
        result = download_from_youtube(url, SONG_FOLDER)

        if 'error' in result:
            print(f"Fehler: {result['error']}")
        else:
            print(f"Erfolgreich heruntergeladen: {result['title']}")
            title = result.get('title', None)
            add_to_queue(title)

    # Starte den nächsten Download
    start_downloads()

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

    # Hol den Download-Status aus der Session (falls vorhanden)
    download_status = session.pop('download_status', None)
    
    # update_song() kannst du weiterhin hier aufrufen, falls nötig
    return render_template("index.html", 
                           playback_queue=current_queue, 
                           files=mp3_files, 
                           current_song=current_song,
                           download_status=download_status)

# Definiert die Route zum Abrufen der Warteschlange
@app.route('/queue')
def get_queue():
    queue = player.get_queue()
    #update_song()
    # Gibt die aktuelle Wiedergabeliste und das aktuelle Lied als JSON zurück
    return jsonify({"queue": current_queue, "current_song": current_song})

# Definiert die Route zum Hochladen von Dateien
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.mp3'):
        file_path = os.path.join(SONG_FOLDER, file.filename)
        file.save(file_path)

    else:
        return render_template('error.html', error_message="Ungültiges Dateiformat. Bitte lade nur MP3-Dateien hoch."), 400
    return redirect(url_for('index'))

# Definiert die Route zum Herunterladen von Songs
@app.route('/download', methods=['POST'])
def download_song():
    url = request.form['url']
    
    # Überprüfen, ob die URL leer ist
    if not url:
        session['download_status'] = 'Fehler: Keine URL angegeben.'
        return redirect(url_for('index'))  # Leitet zurück zur Startseite
      
    download_queue.append(url)
    session['download_status'] = 'Download erfolgreich in die Warteschlange eingereiht.'
    download_thread = threading.Thread(target=start_downloads, daemon=True)
    download_thread.start()

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

# Definiert die Route zur Lautstärkeänderung der Wiedergabe (gibt noch keine Anbindung in der index.html)
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

# Definiert die Route zum LoopTogglen des aktuellen Liedes (gibt noch keine Anbindung in der index.html)
@app.route('/toggle_loop', methods=['POST'])
def toggle_loop():
    print(50*"-")
    print("Hab LoopToggle Command bekommen")
    print(50*"-")
    #update_song(player.get_queue()[0])
    player.toggle_loop()
    update_queue()
    return '', 204

# Definiert die Route zum Shuffle der aktuellen Queue (gibt noch keine Anbindung in der index.html)
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

""" ---- Steuerung der App ---- """
def terminal_input():
    while True:
        command = input("Befehl: ")
        if command == "skip":
            player.skip()
        elif command == "pause":
            player.pause()
        elif command == "resume":
            player.play()
        elif command == "volume":
            volume = int(input("Lautstärke: "))
            player.set_volume(volume)
        elif command == "queue":
            print(player.get_queue())
        elif command == "current":
            print(player.current_song())
        elif command == "exit":
            player.kill()
            break
        else:
            print("Ungültiger Befehl, es gibt folgende Befehle: skip, pause, resume, volume, queue, current, exit")


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
    # Startet den Player-Thread geht nicht...
    #threading.Thread(target=terminal_input, daemon=True).start()

    app.register_error_handler(404, page_not_found)  # Registriert die benutzerdefinierte Fehlerseite
    app.secret_key = os.urandom(24)  # Generiert einen zufälligen Schlüssel für die Sitzungsverwaltung
    app.run(host='0.0.0.0', port=port if port else 80)  # Startet die App auf dem angegebenen Port

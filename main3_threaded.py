# Importiert notwendige Module und Pakete
import os
import re


from PIL import Image
#from queue import Queue
import yt_dlp as youtube_dl
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from threading import Thread, Event
import threading
from flask import Flask, request, render_template, redirect, url_for, jsonify
from dotenv import load_dotenv
# import traceback


# Eigene Module ################# 
import vlc_player
import Database


SONG_FOLDER = 'music/'
TEMP_IMG = 'static/temp/'
WORDS_TO_REMOVE = ['official video', 'lyric video', 'audio', 'music video']

current_queue = []
current_song = {"title": "", "cover": ""}


class Additionals:
    def add_to_queue(title):
        player.add_to_queue(title)
        Additionals.update_song()
        Additionals.update_queue()


    def update_queue():
        global current_queue
        current_queue = player.get_queue()
        print(50*"-")
        print(current_queue)
        print(50*"-")

    def update_song(song = None):
        global current_song
        if song:
            current_song["title"] = song
            Additionals.update_cover(song)

        else:
            current_song["title"] = "No song yet"
            current_song["cover"] = "static/temp/default.png"

        
        print(50*"-")
        print(current_song)
        print(50*"-")

    def update_cover(song):
        global current_song
        # Extrahiert das Cover-Bild, falls vorhanden
        audio = MP3(f"{SONG_FOLDER}/{song}.mp3", ID3=ID3)
        if audio.tags.getall("APIC"):
            for tag in audio.tags.getall("APIC"):
                if tag.type == 3:  # Vorderes Cover
                    cover_path = os.path.join(TEMP_IMG, f"{current_song['title'][:-4]}.jpg")
                    try:
                        with open(cover_path, 'wb') as img:
                            img.write(tag.data)
                        Additionals.adjust_thumbnail(cover_path, cover_path)  # Passt das Thumbnail an
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
        cleaned_title = Additionals.clean_title_with_regex(cleaned_title)
        return cleaned_title.strip()

    def clean_title_with_regex(self,title):
        # Beispiel-Regex: Entfernt alles, was in runden Klammern steht (Noch unnötig)
        cleaned_title = re.sub(r'\(.*?\)', '', title)
        return cleaned_title.strip()

    def download_from_youtube(self,url):
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

class HTMLServer(threading.Thread):
    def __init__(self, port) -> None:
        global server
        global player

        global SONG_FOLDER
        global TEMP_IMG
        
        global queue
        global playback_queue
        global current_song
        global stop_event
        global skip_event


        threading.Thread.__init__(self)
        load_dotenv()

        self.app = Flask(__name__)
        self.port = port

    def run(self):
        # Definiert die Route für die Startseite
        @self.app.route('/')
        def index():
            # Listet alle Dateien im Upload-Ordner auf und rendert das Index-Template
            mp3_files = []
            for file in os.listdir(self.SONG_FOLDER):
                # Prüfen, ob die Dateiendung ".mp3" ist
                if file.endswith(".mp3"):
                    mp3_files.append(file[:-4])
                mp3_files = sorted(mp3_files)

            return render_template("index.html", playback_queue=self.current_queue, files=mp3_files, current_song=self.current_song)


        # Definiert die Route zum Abrufen der Warteschlange
        @self.app.route('/queue')
        def get_queue():
            queue = self.player.get_queue()
            # Gibt die aktuelle Wiedergabeliste und das aktuelle Lied als JSON zurück
            return jsonify({"queue": self.current_queue, "current_song": self.current_song})


        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            file = request.files['file']
            if file and file.filename.endswith('.mp3'):
                file_path = os.path.join(self.SONG_FOLDER, file.filename)
                file.save(file_path)

            else:
                #return jsonify({"error": "Invalid file format"}), 400
                return render_template('error.html', error_message="Ungültiges Dateiformat. Bitte laden Sie nur MP3-Dateien hoch."), 400
            return redirect(url_for('index'))



        @self.app.route('/download', methods=['POST'])
        def download_file():
            url = request.form['url']
            if url and ("youtube.com" or "youtu.be" in url):
                info_dict = Additionals.download_from_youtube(url)
                title = info_dict.get('title', None)
                Additionals.add_to_queue(title)
            else:
                #return jsonify({"error": "Invalid URL"}), 400
                return render_template('error.html', error_message="Ungültige URL. Bitte geben Sie eine gültige YouTube-URL ein."), 400
            return redirect(url_for('index'))


        # Definiert die Route zum Einreihen von Dateien in die Wiedergabeliste
        @self.app.route('/enqueue', methods=['POST'])
        def enqueue_file():
            print(request)
            file = request.data.decode('utf-8')
            print(file)
            Additionals.add_to_queue(file)
            
            return redirect(url_for('index'))

        # Definiert die Route zum Starten der Wiedergabe
        @self.app.route('/start', methods=['POST'])
        def start():
            print(50*"-")
            print("Hab Start Command bekommen")
            print(50*"-")
            self.player.play()
            return '', 204

        # Definiert die Route zum Starten der Wiedergabe
        @self.app.route('/resume', methods=['POST'])
        def resume():
            print(50*"-")
            print("Hab Resume Command bekommen")
            print(50*"-")
            self.player.pause()
            return '', 204

        # Definiert die Route zum Stoppen der Wiedergabe
        @self.app.route('/pause', methods=['POST'])
        def stop():
            print(50*"-")
            print("Hab Pause Command bekommen")
            print(50*"-")
            self.player.pause()
            return '', 204


        # Definiert die Route zum Überspringen des aktuellen Liedes
        @self.app.route('/skip', methods=['POST'])
        def skip():
            print(50*"-")
            print("Hab Skip Command bekommen")
            print(50*"-")
            Additionals.update_song(player.get_queue()[0])
            player.skip()
            Additionals.update_queue()

            return '', 204


        # Definiert eine benutzerdefinierte Fehlerseite für den HTTP-Statuscode 404
        @self.app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404
        
         # Startet die Flask-App
        self.app.config.update(
            TEMPLATES_AUTO_RELOAD = True
        )
        self.app.register_error_handler(404, page_not_found)  # Registriert die benutzerdefinierte Fehlerseite
        self.app.run(host='0.0.0.0', port=self.port)



if __name__ == "__main__":
    if not os.path.exists(SONG_FOLDER):
        os.makedirs(SONG_FOLDER)

    # Definiert den Audio-Player-Thread
    player = vlc_player.MusicPlayer(SONG_FOLDER)
    Additionals.update_queue()

    #database = Database()

    app:Thread = HTMLServer(5000)
    app.daemon = True
    app.start()
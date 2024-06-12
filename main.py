from flask import Flask, request, render_template, redirect, url_for, jsonify
import yt_dlp as youtube_dl
import os
from threading import Thread, Event
from queue import Queue
from pydub import AudioSegment
import simpleaudio as sa
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

queue = Queue()
playback_queue = []
current_song = {"title": "", "cover": ""}
stop_event = Event()
skip_event = Event()


@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", playback_queue=playback_queue, files=files, current_song=current_song)

@app.route('/queue')
def get_queue():
    return jsonify({"queue": playback_queue, "current_song": current_song})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        queue.put(file_path)
        playback_queue.append(file.filename)
    return redirect(url_for('index'))

@app.route('/download', methods=['POST'])
def download_file():
    url = request.form['url']
    if url:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(UPLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)
            thumbnail = info_dict.get('thumbnail', None)
            if title:
                file_path = os.path.join(UPLOAD_FOLDER, f"{title}.mp3")
                queue.put(file_path)
                playback_queue.append(f"{title}.mp3")
                if thumbnail:
                    # Download the thumbnail and embed it into the mp3 file
                    thumbnail_path = os.path.join(UPLOAD_FOLDER, f"{title}.jpg")
                    os.system(f"wget {thumbnail} -O {thumbnail_path}")
                    audio = MP3(file_path, ID3=ID3)
                    audio.tags.add(
                        APIC(
                            encoding=3,  # UTF-8
                            mime='image/jpeg',  # image/jpeg or image/png
                            type=3,  # cover(front)
                            desc='Cover',
                            data=open(thumbnail_path, 'rb').read()
                        )
                    )
                    audio.save()
    return redirect(url_for('index'))

@app.route('/enqueue', methods=['POST'])
def enqueue_file():
    file = request.form['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        queue.put(file_path)
        playback_queue.append(file)
    return redirect(url_for('index'))

@app.route('/start', methods=['POST'])
def start():
    if not player_thread.is_alive():
        player_thread.start()
    return '', 204

@app.route('/stop', methods=['POST'])
def stop():
    stop_event.set()
    return '', 204

@app.route('/skip', methods=['POST'])
def skip():
    skip_event.set()
    return '', 204

def play_audio():
    while True:
        stop_event.clear()
        skip_event.clear()
        file_path = queue.get()
        if file_path:
            playback_queue.remove(os.path.basename(file_path))
            current_song["title"] = os.path.basename(file_path)
            # Extract cover image if exists
            audio = MP3(file_path, ID3=ID3)
            if audio.tags.getall("APIC"):
                for tag in audio.tags.getall("APIC"):
                    if tag.type == 3:  # front cover
                        cover_path = os.path.join(UPLOAD_FOLDER, f"{current_song['title']}_cover.jpg")
                        with open(cover_path, 'wb') as img:
                            img.write(tag.data)
                        current_song["cover"] = cover_path
                        break
            else:
                current_song["cover"] = ""
            song = AudioSegment.from_mp3(file_path)
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

if __name__ == '__main__':
    player_thread = Thread(target=play_audio, daemon=True)
    player_thread.start()
    app.run(host='0.0.0.0', port=5000)

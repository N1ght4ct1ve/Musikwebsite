import os, re

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image

from app.globals import Globals
from app.lib.shared import player


""" ---- Hilfsfunktionen ---- """
def add_to_queue(title):
    player.add_to_queue(title)
    update_queue()


def update_queue():
    Globals.current_queue = player.get_queue()
    print(50*"-")
    print(Globals.current_queue)
    print(50*"-")

def update_song(song = None):
    neuer_song = player.current_song()
    if neuer_song:
        Globals.current_song["title"] = neuer_song
        update_cover(neuer_song)
    elif song:
        Globals.current_song["title"] = song
        update_cover(song)
    else:
        Globals.current_song["title"] = "No song yet"
        Globals.current_song["cover"] = "static/temp/default.png"


def on_song_end(song_title):
    print(f"Callback: Lied beendet - {song_title}")

def on_song_start(song_title):
    print(f"Callback: Lied startet - {song_title}")

def update_cover(song):
    # Extrahiert das Cover-Bild, falls vorhanden
    audio = MP3(f"{Globals.SONG_FOLDER}/{song}.mp3", ID3=ID3)
    if audio.tags.getall("APIC"):
        for tag in audio.tags.getall("APIC"):
            if tag.type == 3:  # Vorderes Cover
                cover_path = os.path.join(Globals.TEMP_IMG, f"{Globals.current_song['title']}.jpg")
                try:
                    with open(cover_path, 'wb') as img:
                        img.write(tag.data)
                    adjust_thumbnail(cover_path, cover_path)  # Passt das Thumbnail an
                    Globals.current_song["cover"] = cover_path
                    break
                except:
                    Globals.current_song["cover"] = "static/temp/default.png"  # Setzt das Cover auf leer, wenn keins vorhanden ist
                    break
    else:
        Globals.current_song["cover"] = "static/temp/default.png"  # Setzt das Cover auf leer, wenn keins vorhanden ist

def clean_title(title):
    cleaned_title = title
    for word in Globals.WORDS_TO_REMOVE:
        cleaned_title = cleaned_title.replace(word, '')
    cleaned_title = clean_title_with_regex(cleaned_title)
    return cleaned_title.strip()

def clean_title_with_regex(title):
    # Beispiel-Regex: Entfernt alles, was in runden Klammern steht (Noch unnötig)
    cleaned_title = re.sub(r'\(.*?\)', '', title)
    return cleaned_title.strip()

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
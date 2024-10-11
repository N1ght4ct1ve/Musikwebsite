import os
import re
import yt_dlp as youtube_dl

SONG_FOLDER = 'music/'
WORDS_TO_REMOVE = ['official video', 'lyric video', 'audio', 'music video']
minimal_duration = 5
maximal_duration = 600

def clean_title(title):
    """Entfernt unerwünschte Wörter aus dem Titel."""
    for word in WORDS_TO_REMOVE:
        title = title.replace(word, '')
    # Entferne doppelte Leerzeichen und trimme den Titel
    title = clean_title_with_regex(title)
    return ' '.join(title.split()).strip()

def clean_title_with_regex(title):
    # Entfernt alles, was in runden Klammern steht
    cleaned_title = re.sub(r'\(.*?\)', '', title)
    return cleaned_title

def duration_live_and_playlist_filter(info_dict, incomplete):
    global minimal_duration, maximal_duration

    if 'entries' in info_dict:
        return 'Die URL ist eine Playlist.'
    if info_dict.get('is_live'):
        return 'Das Video ist ein Livestream.'
    duration = info_dict.get('duration')
    if duration is None:
        return 'Die Dauer des Videos konnte nicht bestimmt werden.'
    if minimal_duration <= duration <= maximal_duration:
        return None
    return 'Das Video ist nicht zwischen 10 Sekunden und 10 Minuten lang.'

def get_title_from_youtube(url):
    try:
        with youtube_dl.YoutubeDL({'format': 'mp3/bestaudio'}) as ydl:
            # Informationen zum Video abrufen
            info = ydl.extract_info(url, download=False)
            title = clean_title(info.get('title', 'Unknown Title'))
            return title

    except youtube_dl.utils.DownloadError as e:
        return str(e)
    except Exception as e:
        return str(e)

def download_from_youtube(url, path):
    global minimal_duration, maximal_duration
    try:
        with youtube_dl.YoutubeDL({'format': 'mp3/bestaudio'}) as ydl:
            # Informationen zum Video abrufen
            info = ydl.extract_info(url, download=False)
            
            # Prüfen, ob ein Filter-Fehler aufgetreten ist
            if 'entries' in info or info.get('is_live') or not (minimal_duration <= info.get('duration', 0) <= maximal_duration):
                return {'error': f'Filterbedingungen nicht erfüllt: URL ist entweder eine Playlist, ein Livestream oder die Dauer liegt nicht im gewünschten Bereich von {minimal_duration} Sekunden bis {maximal_duration} Sekunden.'}
            
            # Titel bereinigen
            title = clean_title(info.get('title', 'Unknown Title'))

            # Optionen für den Download konfigurieren
            ydl_opts = {
                'verbose': True,
                'format': 'mp3/bestaudio/best',
                'outtmpl': os.path.join(path, f'{title}.%(ext)s'),  # Bereinigten Titel verwenden
                'writethumbnail': True,
                'embedthumbnail': True,
                'match_filter': duration_live_and_playlist_filter,
                'postprocessors': [{
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                },
                    {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': 'best',
                },
                    {
                    'key': 'EmbedThumbnail',
                },
                ]
            }

            # Download durchführen
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            info['title'] = title
            return info
    except youtube_dl.utils.DownloadError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    result = download_from_youtube("https://www.youtube.com/watch?v=Dx0MGYe4jR4&pp=ygUJa3JhZnRrbHVi", SONG_FOLDER)
    if 'error' in result:
        print(f"Fehler: {result['error']}")
    else:
        print(f"Erfolgreich heruntergeladen: {result['title']}")

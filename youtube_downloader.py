import os
import yt_dlp as youtube_dl

SONG_FOLDER = 'music/'  # Passen Sie den Pfad entsprechend an


def duration_live_and_playlist_filter(info_dict, incomplete):
    if 'entries' in info_dict:
        return 'Die URL ist eine Playlist.'
    if info_dict.get('is_live'):
        return 'Das Video ist ein Livestream.'
    duration = info_dict.get('duration')
    if duration is None:
        return 'Die Dauer des Videos konnte nicht bestimmt werden.'
    if 10 <= duration <= 600:
        return None
    return 'Das Video ist nicht zwischen 10 Sekunden und 10 Minuten lang.'


def download_from_youtube(url, path):
    ydl_opts = {
        'verbose': True,
        'format': 'mp3/bestaudio/best',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
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

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Prüfen, ob ein Filter-Fehler aufgetreten ist
            if 'entries' in info or info.get('is_live') or not (5 <= info.get('duration', 0) <= 600):
                return {'error': 'Filterbedingungen nicht erfüllt: URL ist entweder eine Playlist, ein Livestream oder die Dauer liegt nicht im gewünschten Bereich.'}
            ydl.download([url])
        return info
    except youtube_dl.utils.DownloadError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}


if __name__ == "__main__":
    # result = download_from_youtube("https://www.youtube.com/watch?v=NjMPOO9WV7E", SONG_FOLDER)
    # result2 = download_from_youtube("https://music.youtube.com/watch?v=a9br6ckspug&si=iX1q1iNqPXVxSeIg", SONG_FOLDER)
    result = download_from_youtube(
        "https://www.youtube.com/watch?v=XXYlFuWEuKI&list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj", SONG_FOLDER)
    if 'error' in result:
        print(f"Fehler: {result['error']}")
    else:
        print(f"Erfolgreich heruntergeladen: {result['title']}")

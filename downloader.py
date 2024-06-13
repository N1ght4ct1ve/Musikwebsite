import os
import yt_dlp as youtube_dl

SONG_FOLDER = './music'

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


# Beispielaufruf:
test = download_from_youtube('https://youtu.be/iWpCdUQLWwU')

print(50*"-")
print(test)

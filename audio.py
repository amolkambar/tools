import yt_dlp

from pytube import Playlist
import os

folder_name=input("Input Folder name for the files: ")

os.mkdir(folder_name)

playlist_url = input("Paste Playlist URL: ")

ids = Playlist(playlist_url)

URLS=[]

for id in ids:
    URLS.append(id)
print(f"Downloading {len(URLS)} files")

ydl_opts = {
    'quiet': True, 
    'no_warnings':True,
    'output':r'test',
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
    'outtmpl':folder_name + '/%(title)s.%(ext)s'
}


import threading
import concurrent.futures

def download_audio(file):
    links = [file]
    yt_dlp.YoutubeDL(ydl_opts).download(links)

with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_audio, URLS)


import os
import time
import yt_dlp
from pytube import Playlist
import threading
import concurrent.futures


folder_name=input("Input Folder name for the files: ")
os.mkdir(folder_name)

playlist_url = input("Paste Playlist URL: ")
ids = Playlist(playlist_url)

start_time = time.time()

URLS=[]
for id in ids:
    URLS.append(id)
print(f"Downloading {len(URLS)} files")

ydl_opts = {
    'quiet': True, 
    'no_warnings':True,
    'output':r'test',
    'format': 'm4a/bestaudio/best',
    'metadatafromtitle':True,
    'writethumbnail':True,
    'outtmpl':folder_name + '/%(title)s.%(ext)s',
    'postprocessors':[{'key': 'FFmpegMetadata',
                        'add_metadata': True,},
                      {'key': 'EmbedThumbnail',}]
}

def download_audio(file):
    links = [file]
    yt_dlp.YoutubeDL(ydl_opts).download(links)

with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_audio, URLS)

print(f'Download completed in {int(time.time()-start_time)} Seconds')

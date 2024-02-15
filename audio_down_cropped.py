import os
import time

import music_tag
from PIL import Image
from PIL.ImageTk import PhotoImage

import yt_dlp
from pytube import Playlist
import threading
import concurrent.futures

# ------------------Download--------------------------
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
                        'add_metadata': True,},]
}

def download_audio(file):
    links = [file]
    yt_dlp.YoutubeDL(ydl_opts).download(links)

with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_audio, URLS)

print(f'Download completed in {int(time.time()-start_time)} Seconds')


#----------------Post-processing----------------------------
def edit_tags(audio_file):
    artwork = os.path.splitext(audio_file)[0] + '.webp' 
    with Image.open(artwork) as img:
        # crop
        width, height = img.size
        new_width, new_height = height, height
        left = (width - new_width)/2
        top = (height - new_height)/2
        right = (width + new_width)/2
        bottom = (height + new_height)/2
        img = img.crop((left, top, right, bottom))
        # rename
        artwork_file = os.path.splitext(artwork)[0]
        artwork_file += '.jpeg'
        img.save(artwork_file, "JPEG", optimize=True)
        # add art file
        f = music_tag.load_file(audio_file)
        with open(artwork_file, 'rb') as img_in:
            f['artwork'] = img_in.read()
        f.save()
        os.remove(artwork_file)
    os.remove(artwork)

def find_all_m4a():
    m4a_files = []
    for root, dirs, files in os.walk(f'{folder_name}/'):
        for file in files:
            if file.endswith(".m4a"):
                m4a_files.append(folder_name + '/' + file)
    return m4a_files

audio_files = find_all_m4a()
print(f"Editing Tags for {len(audio_files)} files.")
start_time = time.time()
for file in audio_files:
    edit_tags(file)
print(f"Editing Completed in {int(time.time()-start_time)} seconds")

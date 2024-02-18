import time
import requests as rq
from bs4 import BeautifulSoup
import concurrent.futures

def get_url(page):
    return f"https://www.albumoftheyear.org/must-hear/{page}/"

# initialise file for saving
file_name = 'mustlistens.csv'
with open(file_name, 'w') as file:
    file.write('Album,Artist,Year\n')

start_ts = time.time()
max_page = 16
mustlistens = []

def add_albums(page):
    global mustlistens

    print(f'Scanning page number:{page}')
    resp = rq.get(get_url(page),
              headers = {'User-Agent': 'Popular browser\'s user-agent',})
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    
    for albumBlock in soup.select('.albumBlock'):
        artist  = albumBlock.select_one('.artistTitle').text.replace(',', '&')
        album   = albumBlock.select_one('.albumTitle').text.replace(',', '')
        date    = albumBlock.select_one('.date').text
        mustlistens.append((album, artist, date))

with concurrent.futures.ThreadPoolExecutor() as executor:
    # why not! results were obtained 10x faster.
    executor.map(add_albums, range(1, max_page+1))

print(f"Scanning completed for {max_page} pages in {int(time.time() - start_ts)} seconds.")

with open(file_name, 'a') as file:
    for item in mustlistens:
        file.write(str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + '\n')

print(f"Added {len(mustlistens)} albums to {file_name}")


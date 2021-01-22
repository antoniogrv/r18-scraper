#!/usr/bin/env python

import requests
import cloudscraper
import io
import os
import sys

from pathlib import Path
from bs4 import BeautifulSoup
from table import parse_html

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_page(request):
    handler = BeautifulSoup(request.text, features = "html.parser")
    parent = handler.find("li", { "data-tracking_id" : "dmmref" })
    if parent == None:
        print(Colors.FAIL + "> Script failure. Can't retrieve the movie page." + Colors.ENDC)
        restart()
    return parent.findChildren("a")[0]["href"];

def create_folders(movie_id):
    Path("requests/").mkdir(exist_ok = True)
    Path('requests/' + movie_id).mkdir(exist_ok = True)      
    Path('requests/' + movie_id + "/assets/").mkdir(exist_ok = True)

def download_table(movie_id, content):
    print(Colors.WARNING + "> Downloading content in 'requests/" + movie_id + "/html.txt'" + Colors.ENDC)

    with io.open("requests/" + movie_id + "/html.txt", "w+", encoding = "utf-8") as f:
        f.write(content)

class Actress:
    def __init__(self, name, link):
        self.name = name
        self.link = link

def get_cast(handler):
    cast = []

    cast_raw_handler = handler.find("div", { "itemprop" : "actors" })

    if cast_raw_handler == None: 
        print(Colors.FAIL + "> Can't parse cast members." + Colors.ENDC)
        restart()

    cast_raw = cast_raw_handler.findChildren("a")

    for actress in cast_raw:
        cast.append(Actress(actress.text.strip(), actress["href"]))

    return cast

def get_content_id(handler):
    print(Colors.WARNING + "> Finding content_id..." + Colors.ENDC)

    content_id_handler = handler.find(string = "Content ID:")

    if content_id_handler == None:
        print(Colors.FAIL + "> Can't find content_id." + Colors.ENDC)
        restart()

    content_id = content_id_handler.find_next("dd")

    print(Colors.WARNING + "> Content_id found: " + content_id.text.strip() + Colors.ENDC)

    return content_id.text.strip()

def create_table(movie_id, movie_page, handler):
    title = handler.find("cite", { "itemprop" : "name" })
    release_date_handler = handler.find(string = "Release Date:")
    studio_handler = handler.find(string = "Studio:")
    cast = get_cast(get_handler(movie_page))

    if title == None or release_date_handler == None or studio_handler == None:
        print(Colors.FAIL + "> Can't parse the data." + Colors.ENDC)
        restart() 

    release_date = release_date_handler.find_next("dd")
    studio = studio_handler.find_next("a")

    return parse_html(title, release_date, studio, cast, movie_page, movie_id)

def download_assets(movie_id, content_id, cast):
    header_download_url = 'https://pics.r18.com/digital/video/' + content_id + '/' + content_id + 'pl.jpg'
    header_download_path = cloudscraper.create_scraper().get(header_download_url, allow_redirects = True)
    header_save_path = 'requests/' + movie_id + '/assets/' + movie_id + '-JAV'
            
    if len(cast) == 1:
        header_save_path += "-"
        header_save_path += cast[0].name.replace(" ", "-")

    header_save_path += '-Header.jpg'

    print(Colors.WARNING + '> Downloading header from: ' + header_download_url + Colors.ENDC)
    print(Colors.WARNING + '> Header saved to: ' + header_save_path + Colors.ENDC)

    open(header_save_path, 'wb').write(header_download_path.content)

    for i in range(1, 6, 1):
        image_download_url = 'https://pics.r18.com/digital/video/' + content_id + '/' + content_id + 'jp-' + str(i) +'.jpg'
        image_download_path = cloudscraper.create_scraper().get(image_download_url, allow_redirects = True)
        image_save_path = 'requests/' + movie_id + '/assets/' + movie_id + '-JAV'
            
        if len(cast) == 1:
            image_save_path += "-"
            image_save_path += cast[0].name.replace(" ", "-")

        image_save_path += '-0' + str(i) + '.jpg'

        print(Colors.WARNING + '> Downloading image ' +  str(i) + ' from: ' + image_download_url + Colors.ENDC)

        open(image_save_path, 'wb').write(image_download_path.content)

    print(Colors.WARNING + '> Images saved to: ' + image_save_path + Colors.ENDC)

def get_handler(movie_page):
    request = cloudscraper.create_scraper().get(movie_page)

    if request.ok:
        return BeautifulSoup(request.text, features = "html.parser")
    else:
        print(Colors.FAIL + "> Can't handle the workload." + Colors.ENDC)
        restart()

def restart():
    movie_id = sys.argv[1]
    print(Colors.FAIL + '> Something went wrong. ' + Colors.BOLD + 'Restarting until success...' + Colors.ENDC + Colors.ENDC)
    os.system('python app.py ' + movie_id)
    sys.exit()

os.system('')

if len(sys.argv) == 1:
    print(Colors.BOLD + "> ./app.py [MOVIE_ID]" + Colors.ENDC)
    exit()

movie_id = sys.argv[1]

url = "https://www.r18.com/common/search/floor=movies/searchword=" + movie_id + " /"
request = cloudscraper.create_scraper().get(url)

print(Colors.OKCYAN + "> Starting..." + Colors.ENDC)

if request.ok:
    if request.text.find('1 titles found') != -1:
        print(Colors.WARNING + '> Movie found! Finding its page...' + Colors.ENDC)

        movie_page = get_page(request)

        print(Colors.WARNING + '> Page found! Creating folders...' + Colors.ENDC)

        create_folders(movie_id)

        print(Colors.WARNING + '> Folders created. Downloading assets...' + Colors.ENDC)

        download_assets(movie_id, get_content_id(get_handler(movie_page)), get_cast(get_handler(movie_page)))

        print(Colors.WARNING + '> Assets downloaded. Generating content...' + Colors.ENDC)

        table = create_table(movie_id, movie_page, get_handler(movie_page))

        print(Colors.WARNING + '> Content generated. Downloading...' + Colors.ENDC)

        download_table(movie_id, table)

        print(Colors.OKGREEN + Colors.BOLD + '> Success!' + Colors.ENDC + Colors.ENDC)
    else:
        print(Colors.FAIL + "> Can't find the movie page. Exiting with id: " + movie_id + Colors.ENDC)
        restart()

else:
    print(Colors.FAIL + "> Can't request network access." + Colors.ENDC)
    restart()


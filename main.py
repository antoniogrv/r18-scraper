#!/usr/bin/env python

import PySimpleGUI as gui
import requests
import cloudscraper
import urllib.request
import io
import sys

from pathlib import Path
from bs4 import BeautifulSoup
from table import parse_html

def get_page(request):
    handler = BeautifulSoup(request.text, features = "html.parser")
    parent = handler.find("li", { "data-tracking_id" : "dmmref" })
    return parent.findChildren("a")[0]["href"];

def create_folders(movie_id):
    Path("requests/").mkdir(exist_ok = True)
    Path('requests/' + movie_id).mkdir(exist_ok = True)      
    Path('requests/' + movie_id + "/assets/").mkdir(exist_ok = True)

def download_table(movie_id, content):
    with io.open("requests/" + movie_id + "/html.txt", "w+", encoding = "utf-8") as f:
        f.write(content)

class Actress:
    def __init__(self, name, link):
        self.name = name
        self.link = link

def get_cast(handler):
    cast = []

    cast_raw = handler.find("div", { "itemprop" : "actors" }).findChildren("a")

    for actress in cast_raw:
        cast.append(Actress(actress.text.strip(), actress["href"]))

    return cast

def get_content_id(handler):
    print("> Finding content_id...")
    content_id = handler.find(string = "Content ID:").find_next("dd")
    print("> Content_id found: " + content_id.text.strip())
    return content_id.text.strip()

def create_table(movie_id, movie_page, handler):
    title = handler.find("cite", { "itemprop" : "name" })
    release_date = handler.find(string = "Release Date:").find_next("dd")
    studio = handler.find(string = "Studio:").find_next("a")
    cast = get_cast(get_handler(movie_page))

    return parse_html(title, release_date, studio, cast, movie_page, movie_id)

def download_assets(movie_id, content_id, cast):
    header_download_path = cloudscraper.create_scraper().get('https://pics.r18.com/digital/video/' + content_id + '/' + content_id + 'pl.jpg', allow_redirects = True)
    header_save_path = 'requests/' + movie_id + '/assets/' + movie_id + '-JAV'
            
    if len(cast) == 1:
        header_save_path += "-"
        header_save_path += cast[0].name.replace(" ", "-")

    header_save_path += '-Header.jpg'

    open(header_save_path, 'wb').write(header_download_path.content)

    for i in range(1, 6, 1):
        image_download_path = cloudscraper.create_scraper().get('https://pics.r18.com/digital/video/' + content_id + '/' + content_id + 'jp-' + str(i) +'.jpg', allow_redirects = True)
        image_save_path = 'requests/' + movie_id + '/assets/' + movie_id + '-JAV'
            
        if len(cast) == 1:
            image_save_path += "-"
            image_save_path += cast[0].name.replace(" ", "-")

        image_save_path += '-0' + str(i) + '.jpg'

        open(image_save_path, 'wb').write(image_download_path.content)

def get_handler(movie_page):
    request = cloudscraper.create_scraper().get(movie_page)

    if request.ok:
        return BeautifulSoup(request.text, features = "html.parser")
    else:
        print("> Can't handle the workload. Exiting.")
        exit()

movie_id = sys.argv[0]

url = "https://www.r18.com/common/search/floor=movies/searchword=" + movie_id + " /"
request = cloudscraper.create_scraper().get(url)

if request.ok:
    if request.text.find('1 titles found') != -1:
        print('> Movie found! Finding its page...')

        movie_page = get_page(request)

        print('> Page found! Creating folders...')

        create_folders(movie_id)

        print('> Generating HTML...')

        table = create_table(movie_id, movie_page, get_handler(movie_page))

        print('> Table generated. Downloading...')

        download_table(movie_id, table)

        print('> Success!')
    else:
        print("> Can't find the movie page. Exiting with id:" + movie_id)

else:
    print("> Can't request network access. Exiting.")


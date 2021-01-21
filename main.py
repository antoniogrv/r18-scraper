#!/usr/bin/env python
#main.py

import PySimpleGUI as gui
import requests
import cloudscraper
import urllib.request
import io

from pathlib import Path
from bs4 import BeautifulSoup

class Actress:
    def __init__(self, name, link):
        self.name = name
        self.link = link

def downloadContent(url, movieID):
    request = cloudscraper.create_scraper().get(url)
    handler = BeautifulSoup(request.text, features = "html.parser")

    # header

    content  = '<p style="text-align: center;"><strong><span style="font-size:22px;"><a href="MOVIE LINK" rel="nofollow">MOVIE ID</a></span><br />'
    content += '<span style="font-size:26px;"><a href="ACTRESS(es) LINK" rel="nofollow">ACTRESS</a>'
    content += '<span style="font-size:26px;"><a href="MOVIE LINK">&minus;<strong>TITLE&quot;</strong></span><br />'
    content += '<a href="MOVIE LINK"/><img alt="" src="IMAGE LINK" /></a></p>'

    # table

    content += '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width:400px"><tbody>'
    content += '<tr><td><strong>Movie</strong></td> <td><a href="MOVIE LINK" rel="nofollow">MOVIE ID</a></td></tr>'
    content += '<tr><td><strong>Studio</strong></td><td><a href="STUDIO LINK" rel="nofollow">STUDIO NAME</a></td></tr>'
    content += '<tr><td><strong>Cast</strong></td><td><a href="ACTRESS(es) LINK(s)" rel="nofollow">ACTRESS(es) NAME(s)</a></td></tr>'
    content += '<tr><td><strong>Release Date</strong></td><td>RELEASE DATE</td></tr></tbody>'

    # actresses

    actressData = []

    actressList = handler.find("div", { "itemprop" : "actors" }).findChildren("a")

    for actress in actressList:
        actressData.append(Actress(actress.text.strip(), actress["href"]))

    # content-id

    contentID = handler.find(string = "Content ID:").find_next("dd")

    # download header image

    headerDownload = cloudscraper.create_scraper().get('https://pics.r18.com/digital/video/' + contentID.text.strip() + '/' + contentID.text.strip() + 'pl.jpg', allow_redirects = True)
    open("requests/" + movieID + "/assets/" + movieID + '-JAV-Actresses-Header.jpg', 'wb').write(headerDownload.content)

    # download images

    for i in range(1, 6, 1):
        imageDownload = cloudscraper.create_scraper().get('https://pics.r18.com/digital/video/' + contentID.text.strip() + '/' + contentID.text.strip() + 'jp-' + str(i) +'.jpg', allow_redirects = True)
        print('https://pics.r18.com/digital/video/' + contentID.text.strip() + '/' + contentID.text.strip() + 'jp-' + str(i) +'.jpg')
        f = open("requests/" + movieID + "/assets/" + movieID + '-JAV-Actresses-0' + str(i) + '.jpg', 'wb')
        f.write(imageDownload.content)
        f.close()

    return content

def prepareContent(url, html, movieID):
    Path("requests/").mkdir(exist_ok = True)
    Path('requests/' + movieID).mkdir(exist_ok = True)      
    Path('requests/' + movieID + "/assets/").mkdir(exist_ok = True)

    handler = BeautifulSoup(html, features = "html.parser")
    parent = handler.find("li", { "data-price" : "500" })
    url = parent.findChildren("a")

    downloadResult = downloadContent(url[0]["href"], movieID)

    with io.open("requests/" + movieID + "/html.txt", "w+", encoding = "utf-8") as f:
        f.write("to-do")

layout = [
    [
        gui.Text("Movie ID: "),
        gui.In(size = (15, 1), enable_events = True, key = "-ID-"),
        gui.Button("Search", key = "-SEARCH-", bind_return_key = True)
    ],
    [
        gui.Text('_' * 75)
    ],
    [
        gui.Text("Waiting for an ID...", key = "-RESPONSE-", size = (50, 1))
    ]
]

title = "R18 Parser"
frame = gui.Window(title, layout)

while True:
    event, values = frame.read()
    if event == gui.WIN_CLOSED:
        break
    if event == "-SEARCH-":
        url = "https://www.r18.com/common/search/floor=movies/searchword=" + values["-ID-"] + " /"
        request = cloudscraper.create_scraper().get(url)

        if request.ok:

            if request.text.find("1 titles found") != -1:
                frame.Element("-RESPONSE-").Update("Movie found! Parsing...")
                prepareContent(url, request.text, values["-ID-"].upper())
                frame.Element("-RESPONSE-").Update("Request accepted. Files generated in requests/" + values["-ID-"].upper() + "/.")
            else:
                frame.Element("-RESPONSE-").Update("Movie not found.")
        else:
            print("Request failed (01).")
            break

frame.close()

#!/usr/bin/env python
#main.py

import PySimpleGUI as gui
import requests
import cloudscraper
import io
from pathlib import Path

def content_parser(str, movie_id):
    Path(movie_id).mkdir(exist_ok = True)      
    Path(movie_id + "/assets/").mkdir(exist_ok = True)

    with io.open(movie_id + "/html.txt", "w+", encoding="utf-8") as f:
        f.write(str)


layout = [
    [
        gui.Text("Movie ID: "),
        gui.In(size = (15, 1), enable_events = True, key = "-ID-"),
        gui.Button("Search", key = "-SEARCH-")
    ],
    [
        gui.Text('_' * 75)
    ],
    [
        gui.Text("Waiting for an ID...", key = "-RESPONSE-", size = (45, 1))
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

        if request.text.find("1 titles found") != -1:
            frame.Element("-RESPONSE-").Update("Movie found! Parsing...")
            content_parser(request.text, values["-ID-"].upper())
            frame.Element("-RESPONSE-").Update("Request accepted. Files generated in /" + values["-ID-"].upper() + "/.")
        else:
            frame.Element("-RESPONSE-").Update("Movie not found.")

frame.close()

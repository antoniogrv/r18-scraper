#!/usr/bin/env python
#main.py

import PySimpleGUI as gui
import requests
import cloudscraper
from pathlib import Path

def content_parser(str, movie_id):
    Path(movie_id).mkdir(exist_ok = True)      
    Path(movie_id + "/assets/").mkdir(exist_ok = True)
    open(movie_id + "/html.txt", "w+")

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
        gui.Text("Waiting for an ID...", key = "-RESPONSE-")
    ]
]

title = "R18 Parser"
frame = gui.Window(title, layout)

while True:
    event, values = frame.read()
    if event == gui.WIN_CLOSED:
        break
    if event == "-SEARCH-":
        frame.Element("-RESPONSE-").Update("Loading...")
        url = "https://www.r18.com/common/search/floor=movies/searchword=" + values["-ID-"] + " /"

        print("[Movie "+ values["-ID-"] + "] Loading data from " + url)

        request = cloudscraper.create_scraper().get(url)

        if "1 titles found" in request.text:
            frame.Element("-RESPONSE-").Update("Movie found! Parsing...")
            content_parser("Movie Page", values["-ID-"].upper())
        else:
            frame.Element("-RESPONSE-").Update("Movie not found.")

frame.close()

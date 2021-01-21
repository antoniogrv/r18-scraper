#!/usr/bin/env python
#main.py

import PySimpleGUI as gui
from bs4 import BeautifulSoup
import settings
import requests

layout = [
    [
        gui.Text("Movie ID: "),
        gui.In(size = (15, 1), enable_events = True, key = "-ID-")
    ],
    [
        gui.Text('_' * 75)
    ],
    [
        gui.Text("Waiting for an ID...", key = "-RESPONSE-")
    ]
]

title = "R18 Parser"
margins = (settings.FRAME_WIDTH, settings.FRAME_HEIGHT)

frame = gui.Window(title, layout, margins)

while True:
    event, values = frame.read()
    if event == gui.WIN_CLOSED:
        break
    if event == "-ID-":
        url = "https://www.r18.com/common/search/floor=movies/searchword=" + values["-ID-"] + "/service=video/"
        request = requests.get(url)

        print("[Movie "+ values["-ID-"] + "] Loading data from " + url)

        soup = BeautifulSoup(request.content, features = "html.parser")

        frame.Element("-RESPONSE-").Update("Loading...")


frame.close()


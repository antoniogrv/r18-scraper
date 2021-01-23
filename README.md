## r18-parser

Generates content about JAV movies listed on [R18](https://www.r18.com/) and formats them for [ZENRA's Blog](https://www.zenra.net/blog).  
Creates a folder with sample images, a table with informations about the movie, and a trailer, if possible.  


#### Instructions

Download the application by clicking [here](https://gitlab.com/v1enna/r18-parser/-/archive/master/r18-parser-master.zip) or clone it via `git clone https://gitlab.com/v1enna/r18-parser.git`.  
Unzip the files in a folder and open a terminal there with `cmd` or any other shell. Run `app.py <movie_id>` and let the program work.  
It will usually try to handle the request multiple times. If it's taking too long, `CTRL-C` will kill the process.


#### To-do

- [X] Add support for movies without actresses listed on R18
- [X] Download trailers if possible
- [X] Add multiple research feature
- [X] Improve trailer research

![Example](https://i.gyazo.com/562d0cda85900899f15bd9e1078d046e.png)

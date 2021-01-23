## r18-scraper

Generates content about JAV movies listed on [R18](https://www.r18.com/) and formats them for [ZENRA's Blog](https://www.zenra.net/blog).  
Creates a folder with sample images, a table with informations about the movie, and a trailer, if possible.  


#### Instructions

Download the application by clicking [here](https://gitlab.com/v1enna/r18-parser/-/archive/master/r18-parser-master.zip) or clone it via `git clone https://gitlab.com/v1enna/r18-parser.git`.  
Unzip the files in a folder and open a terminal there with `cmd` or any other shell. Run `app.py <movie_id/content_id> [other movies]` and let the program work. It will usually try to handle the request multiple times. If it's taking too long, `CTRL-C` will kill the process.

For istance, `app.py HITMA-60 HITMA-61 RBD-225` will download a trailer (if possible) and about 5 images for every movie, scraping data such as the movie ID, the content ID, the actresses with proper linking to their page on R18, the studio which produced the movie and so on, formatting everything in HTML and posting the results in `<source>/requests/result.txt`. Assets and HTML content for individual movies can be found in `<source>/requests/<movie_id>`.


#### To-do

- [X] Add support for movies without actresses listed on R18
- [X] Download trailers if possible
- [X] Add multiple movie research feature
- [X] Improve trailer research

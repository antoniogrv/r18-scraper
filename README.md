## r18-scraper

### R18 has closed. This scraper won't be maintained anymore.

#### Doesn't work properly anymore as of 10-26-2021.
Sadly, R18 recently updated its anti-scraping measures, making the already deprecated [request-html](https://requests.readthedocs.io/projects/requests-html/en/latest/)'s HTTPSessions even more useless. Right now, I don't feel like over-engineering how to scrape automatically (ie. using a headless browser) data from R18, so I'm probably going to implement a less-optimal software to achieve my needs. Still, options such as [Selenium](https://www.selenium.dev/) could be explored in the future.

Generates content about JAV movies listed on [R18](https://www.r18.com/).
Creates a folder with sample images, a table with informations about the movie, and a trailer, if possible.  

![Preview](https://i.ibb.co/f49g1HF/ea89ed9a77ca859dbd380859a5d7ba38.png)

#### Instructions

Download the application by clicking [here](https://gitlab.com/v1enna/r18-parser/-/archive/master/r18-parser-master.zip) or clone it via `git clone https://gitlab.com/v1enna/r18-parser.git`.  
Unzip the files, then run `app.py <movie_id/content_id> [other movies]` and let the program work. It will usually try to handle the request multiple times.

For instance, `app.py HITMA-60 HITMA-61 RBD-225` will download a trailer (if possible) and about 5 images for every movie (_HITMA-60, HITMA-61, RBD-225_), scraping data such as the movie ID, the content ID, the actresses with proper linking to their page on R18, the studio which produced the movie and so on, formatting everything in HTML and posting the results in `<source>/requests/result.txt`. Assets and HTML content for individual movies can be found in `<source>/requests/<movie_id>`.


#### To-do

- [X] Add support for movies without actresses listed on R18
- [X] Download trailers if possible
- [X] Add multiple movie research feature

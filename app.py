import io
import os
import pathlib
import requests

from bs4 import BeautifulSoup
from table import parse_html
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Scraper:
    def __init__(self, html):
        self.movie = None
        self.result = None
        self.html = html
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.request_id = self.parse_content_id()

        self.start()

    def start(self):
        self.movie = Movie(
            self.request_id,
            self.parse_movie_id(),
            self.parse_title(),
            self.parse_release_date(),
            self.parse_studio(),
            self.parse_url(),
            self.parse_cast(),
            self.parse_trailer_source()
        )
        self.create_folders()
        self.download_assets()

    def parse_url(self):
        search_url = "https://www.r18.com/common/search/floor=movies/searchword=" + self.request_id + "/"
        search_request = requests.get(search_url, headers = { 'User-Agent' : 'Mozilla/5.0'})

        print(Colors.WARNING + "> Request URL: " + search_url + Colors.ENDC)

        if search_request.ok and search_request.text.find('1 titles found') != -1:
            search_soup = BeautifulSoup(search_request.text, features = "html.parser")
            if (search_soup.find("li", { "data-tracking_id" : "dmmref" })) == None:
                print(Colors.FAIL + "> Script failure. Can't retrieve the movie page." + Colors.ENDC)
            return search_soup.find("li", { "data-tracking_id" : "dmmref" }).findChildren("a")[0]["href"]
        else:
            print(Colors.FAIL + "> Script failure. Can't retrieve the movie page." + Colors.ENDC)
            return None

    def parse_movie_id(self):
        return self.soup.find(string = "DVD ID").find_next("div").text.strip()

    def parse_title(self):
        return self.soup.find("meta", attrs = { "property" : "og:title" }).get("content").strip()

    def parse_release_date(self):
        return self.soup.find(string = "Release date").find_next("div").text.strip()

    def parse_studio(self):
        studio_name = self.soup.find(string = "Studio").find_next("a").text.strip()
        studio_url = self.soup.find(string = "Studio").find_next("a")["href"]
        return Studio(studio_name, studio_url)

    def parse_content_id(self):
        return self.soup.find(string = "Content ID").find_next("div").text.strip()

    def parse_trailer_source(self):
        if(self.soup.find("source") == None):
            print(Colors.FAIL + "> No trailers found." + Colors.ENDC)
            return None

        raw_trailer = self.soup.find("source")["src"].split("_")[0]

        suffixes = [
            "_mhb_w",
            "_dmb_w",
            "_dmb_s",
            "_mhb_s",
        ]

        sources = []

        for suffix in suffixes:
            sources.append(raw_trailer + suffix + ".mp4")

        return sources

    def parse_cast(self):
        cast = []

        cast_div = self.soup.find("h3", string = "Actresses").find_next("div")
        cast_span = cast_div.findChildren("a")

        for actress in cast_span:
            cast.append(Actress(actress.text.strip(), actress.get("href")))

        return cast

    def create_folders(self):
        print(Colors.WARNING + '> Creating folders...' +  Colors.ENDC)

        Path('requests/' + self.movie.get_movie_id()).mkdir(exist_ok = True)
        Path('requests/' + self.movie.get_movie_id() + "/assets/").mkdir(exist_ok = True)

    def download_assets(self):
        print(Colors.WARNING + '> Downloading assets...' +  Colors.ENDC)

        self.download_header()
        self.download_images()
        self.download_trailer()

    def download_header(self):
        header_download_url = 'https://pics.r18.com/digital/video/' + self.movie.get_content_id() + '/' + self.movie.get_content_id() + 'pl.jpg'
        header_download_path = requests.get(header_download_url, allow_redirects = True, headers = { 'User-Agent' : 'Mozilla/5.0' })

        print(Colors.WARNING + '> Downloading header from: ' + header_download_url + Colors.ENDC)

        header_save_path = 'requests/' + self.movie.get_movie_id() + '/assets/' + self.movie.get_movie_id() + '-JAV'

        if header_download_path.ok:
            if len(self.movie.get_cast()) == 1:
                header_save_path += "-"
                header_save_path += self.movie.get_cast()[0].name.replace(" ", "-")

            header_save_path += '-Header.jpg'

            print(Colors.OKCYAN + '> Header saved to: ' + header_save_path + Colors.ENDC)

            open(header_save_path, 'wb').write(header_download_path.content)
        else:
            print(Colors.FAIL + "> Can't download the header image." + Colors.ENDC)

    def download_images(self):
        failure = 0

        print(Colors.WARNING + '> Looking for images... ' + Colors.ENDC)

        for i in range(1, 6, 1):
            image_download_url = 'https://pics.r18.com/digital/video/' + self.movie.get_content_id()  + '/' + self.movie.get_content_id()  + 'jp-' + str(i) +'.jpg'
            image_download_path = requests.get(image_download_url, allow_redirects = False, headers = { 'User-Agent' : 'Mozilla/5.0' })  
            image_save_path = 'requests/' + self.movie.get_movie_id() + '/assets/' + self.movie.get_movie_id() + '-JAV'

            if image_download_path.ok or len(image_download_path.history) != 0:
                if len(self.movie.get_cast()) == 1:
                    image_save_path += "-"
                    image_save_path += self.movie.get_cast()[0].name.replace(" ", "-")

                image_save_path += '-0' + str(i) + '.jpg'

                open(image_save_path, 'wb').write(image_download_path.content)
            else:
                failure += 1

        if failure < 5:
            print(Colors.OKCYAN + '> Images saved to: requests/' + self.movie.get_content_id() + '/assets/' + Colors.ENDC)
        else:
            print(Colors.FAIL + "> Can't download any image. That's bad..." + Colors.ENDC)

    def download_trailer(self):
        print(Colors.WARNING + '> Parsing the trailer...' + Colors.ENDC)

        trailer_exists = False

        for source in self.parse_trailer_source():
            print(Colors.WARNING + '> Scanning trailer source: ' + source + Colors.ENDC)
           
            trailer_download_request = requests.get(source, allow_redirects = True, headers = { 'User-Agent' : 'Mozilla/5.0' })
            
            if trailer_download_request.ok:

                trailer_exists = True
                trailer_save_path = 'requests/' + self.movie.get_movie_id() + '/assets/'
                trailer_save_name = self.movie.get_movie_id() + '-JAV'

                if len(self.movie.get_cast()) == 1:
                    trailer_save_name += "-"
                    trailer_save_name += self.movie.get_cast()[0].name.replace(" ", "-")

                trailer_save_name += '.mp4'

                print(Colors.OKCYAN + '> Trailer saved to: ' + trailer_save_path + trailer_save_name + Colors.ENDC)

                self.movie.set_trailer(trailer_save_name)

                open(trailer_save_path + trailer_save_name, 'wb').write(trailer_download_request.content)

                break

        if trailer_exists == False:
            print(Colors.FAIL + "> Can't obtain any MP4 trailers for this movie." + Colors.ENDC)

    def get_movie(self):
        return self.movie

    def get_result(self):
        self.result = parse_html(self.movie)

        print(Colors.OKCYAN + "> Saving HTML table to: requests/" + self.movie.get_movie_id() + "/html.txt" + Colors.ENDC)

        with io.open("requests/" + self.movie.get_movie_id() + "/html.txt", "w+", encoding = "utf-8") as f:
            f.write(result)

        return self.result

class Actress:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

class Studio:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

class Movie:
    def __init__(self, content_id, movie_id, title, release_date, studio, url, cast, trailer):
        self.content_id = content_id
        self.movie_id = movie_id
        self.title = title
        self.release_date = release_date
        self.studio = studio
        self.url = url
        self.cast = cast
        self.trailer = trailer

    def get_content_id(self):
        return self.content_id

    def get_movie_id(self):
        return self.movie_id

    def get_title(self):
        return self.title

    def get_release_date(self):
        return self.release_date

    def get_studio(self):
        return self.studio

    def get_url(self):
        return self.url

    def get_cast(self):
        return self.cast

    def get_trailer(self):
        if(len(self.cast) == 1):
            actress = self.cast[0].get_name().split(" ")
            return self.movie_id + "-JAV-" + actress[0] + (("-" + actress[1]) if len(actress) > 1 else "") + ".mp4"
        else:
            return self.movie_id + "-JAV.mp4"

    def set_content_id(self, content_id):
        self.content_id = content_id

    def set_movie_id(self, movie_id):
        self.movie_id = movie_id

    def set_title(self, title):
        self.title = title

    def set_release_date(self, release_date):
        self.release_date = release_date

    def set_studio(self, studio):
        self.studio = studio

    def set_url(self, url):
        self.url = url

    def set_cast(self, cast):
        self.cast = cast

    def set_trailer(self, trailer):
        self.trailer = trailer

Path("requests/").mkdir(exist_ok = True)

print(Colors.BOLD + "# r18-scraper [manual] (last update: 11-15-2021; current per-request timeout: 0s)" + Colors.ENDC)

result = "" # result contains the requested html

for filename in os.listdir("source"):
    f = os.path.join("source", filename)
    if(os.path.isfile(f)):
        with open(f, encoding="utf8") as content:
            result += Scraper(content.read()).get_result()

print(Colors.OKGREEN + Colors.BOLD + "[!] Done. Results posted in '<root>/requests/'." + Colors.ENDC)  
with io.open("requests/result.txt", "w+", encoding = "utf-8") as f:
    f.write("<p>Introduction</p><p>&nbsp;</p>" + result + "Conclusions") 
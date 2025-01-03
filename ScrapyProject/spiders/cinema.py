import random
import re
from bs4 import BeautifulSoup as bs
import scrapy

from ScrapyProject.items import CinemaItem, ScreeningRoomItem, ScreeningItem



class CinemaSpider(scrapy.Spider):
    name = 'cinema'
    allowed_domains = ['maoyan.com']
    start_urls = ["https://www.maoyan.com/cinemas"]


    def __init__(self):
        super().__init__()
        self.processCinemaByName = set()

    def parse(self, response, **kwargs):
        soup = bs(response.text, 'html.parser')
        cinemas_links = soup.select('a.cinema-name')
        for link in cinemas_links:
            url = link.get('href')
            if url:
                yield response.follow(url, callback=self.parse_cinema_detail)

        next_page = soup.select_one("ul.list-pager li:last-child a")
        if next_page and next_page.get('href') != 'javascript:void(0);':
            yield response.follow(next_page['href'], callback=self.parse)

    def parse_cinema_detail(self, response):
        soup = bs(response.text, 'html.parser')
        name_elem = soup.select_one("h1")
        name = name_elem.text.strip() if name_elem else "Unknown Cinema"

        if name not in self.processCinemaByName:
            print(f"Processing Cinema: {name}")
            self.processCinemaByName.add(name)
            cinema_item = CinemaItem()
            cinema_item['name'] = name

            location_elem = soup.select_one("div.address.text-ellipsis")
            cinema_item['location'] = location_elem.text.strip() if location_elem else "Unknown Location"

            contact_elem = soup.select_one("div.telphone")
            contact_number = contact_elem.text.strip() if contact_elem else ""
            cinema_item['contact_number'] = re.sub(r'电话：', "", contact_number)

            # yield cinema_item

            # 播映信息
            yield from self.parse_screening(response, name)

    def save_screening_room(self, cinema_name, room_number, seat_count):
        screening_room_item = ScreeningRoomItem()
        screening_room_item['cinema_name'] = cinema_name
        screening_room_item['room_number'] = room_number
        screening_room_item['seat_count'] = seat_count
        yield screening_room_item

    def save_screening(self, movie_name, room_number, screening_time, price):
        screening_item = ScreeningItem()
        screening_item['movie_name'] = movie_name
        screening_item['screening_time'] = screening_time
        screening_item['room_number'] = room_number
        screening_item['price'] = price
        yield screening_item

    def parse_screening(self, response, cinema_name):
        soup = bs(response.text, 'html.parser')
        screening_room_set = set()

        movies_list = soup.select("div.show-list")
        for movie in movies_list:
            movie_name_elem = movie.select_one("h2.movie-name")
            movie_name = movie_name_elem.text.strip() if movie_name_elem else "Unknown Movie"

            movie_dates = movie.select("span.date-item")
            date_arranges = movie.select("div.plist-container")
            for i in range(min(len(movie_dates), len(date_arranges))):
                movie_date = movie_dates[i].text.strip() if movie_dates[i] else "Unknown Date"

                date_arrange = date_arranges[i]
                room_elem = date_arrange.select_one("span.hall")
                room_number = room_elem.text.strip() if room_elem else "Unknown Room"

                time_elem = date_arrange.select_one("span.begin-time")
                #$分割日期和具体时间
                screening_time = movie_date + "日 " +time_elem.text.strip() if time_elem else "Unknown Time"
                if screening_time != 'Unknown Time':
                    screening_time = screening_time[2:]

                #随机价格
                price = random.randint(20,50)

                if room_number not in screening_room_set:
                    screening_room_set.add(room_number)
                    # yield from self.save_screening_room(cinema_name, room_number, 40)

                yield from self.save_screening(movie_name, room_number, screening_time, price)


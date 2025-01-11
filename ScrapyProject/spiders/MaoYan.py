import re
import urllib

import requests
import scrapy
from bs4 import BeautifulSoup
from ScrapyProject.items import MovieItem, ActorItem, MovieActorItem
from ScrapyProject.methods import *



class MaoyanSpider(scrapy.Spider):
    name = "MaoYan"
    allowed_domains = ["maoyan.com"]
    start_urls = [
        "https://maoyan.com/films/?showType=1",
        "https://maoyan.com/films/?showType=2",
        "https://maoyan.com/films/?showType=3",
    ]

    def __init__(self):
        super().__init__()
        self.processMovieByTitle = set()
        self.precessActorByName = set()

    def parse(self, response, **kwargs):
        print(response.url)
        soup = BeautifulSoup(response.text, "html.parser")

        movies = soup.select("div.movie-item.film-channel")
        for movie in movies:
            url = movie.select_one("a")
            if url:
                detail_url = f"https://www.maoyan.com/ajax{url['href']}"
                cookies = getCookies()
                params = getParams() #params
                headers = getHeaders(detail_url, params)

                query_string = urllib.parse.urlencode(params)
                detail_url = f"{detail_url}?{query_string}"
                res = requests.get(detail_url, headers=headers, cookies=cookies,params=params)

                yield from self.parse_detail(res)
        next_page_url = soup.select_one("div.movies-pager ul li:last-child a")
        if next_page_url and next_page_url.get("href") != "javascript:void(0);":
            yield response.follow(next_page_url["href"], callback=self.parse)

    def parse_movie_detail(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select_one("h1")
        title_text = title.text.strip() if title else None
        print(title_text)
        if title_text and title_text not in self.processMovieByTitle:
            self.processMovieByTitle.add(title_text)
            movie_item = MovieItem()
            movie_item["title"] = title_text

            synopsis = soup.select_one("span.dra")
            movie_item["synopsis"] = re.sub(r"\s+", "", synopsis.text) if synopsis else ""

            release_date = soup.select_one("li.ellipsis:last-child")
            movie_item["release_date"] = (
                re.sub(r"[\u4e00-\u9fff]+", "", release_date.text)
                if release_date
                else ""
            )


            production_region = soup.find_all("li",class_="ellipsis")[1].get_text() or ""

            if '/' in production_region:
                production_region = production_region[:production_region.index('/')] or ""
            movie_item["production_region"] = production_region.strip()

            director = soup.select_one("div.name")
            movie_item["director"] = re.sub(r"\s+", "", director.text) if director else ""

            rating_style = soup.select_one("div.star-on")
            if rating_style and rating_style.get("style"):
                match = re.search(r"width:\s*(\d+(\.\d+)?)%", rating_style["style"])
                rating = float(match.group(1)) / 10 if match else 0
            else:
                rating = 0
            movie_item["rating"] = rating

            poster_url = soup.select_one("img.avatar")
            movie_item["poster_url"] = poster_url["src"] if poster_url else ""

            tags = soup.select("li.ellipsis a")
            tags_str = ",".join([tag.text.strip() for tag in tags]) if tags else ""
            movie_item["tags"] = tags_str

            movie_item["collection_count"] = 0
            yield movie_item
    def parse_actor_detail(self, response):

        soup = BeautifulSoup(response.text, "html.parser")
        movie_name = soup.select_one("h1")
        movie_name = movie_name.text.strip() if movie_name else "Unknown"

        actors_info = soup.select("ul.celebrity-list.clearfix li.celebrity.actor div.info")
        roleSet = set()
        for actor_info in actors_info:
            actor_name_elem = actor_info.select_one("div.name")
            actor_name = (
                re.sub(r"\s+", "", actor_name_elem.text).strip()
                if actor_name_elem
                else "Unknown"
            )

            if actor_name not in self.precessActorByName:
                self.precessActorByName.add(actor_name)
                actor_item = ActorItem()
                actor_item["actor_name"] = actor_name
                yield actor_item

            actor_role_elem = actor_info.select_one("span.role")
            actor_role = (
                re.sub(r"饰：", "", actor_role_elem.text).strip()
                if actor_role_elem
                else actor_name
            )

            if actor_role not in roleSet:
                roleSet.add(actor_role)
                movie_actor_item = MovieActorItem()
                movie_actor_item["movie_name"] = movie_name
                movie_actor_item["actor_name"] = actor_name
                movie_actor_item["role"] = actor_role
                yield movie_actor_item

    def parse_detail(self, response):
        # print("headers:", response.headers)
        # print("\n",response.text)
        yield from self.parse_movie_detail(response)
        yield from self.parse_actor_detail(response)








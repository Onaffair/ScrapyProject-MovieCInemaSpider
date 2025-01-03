# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CinemaItem(scrapy.Item):
    # Cinema table fields
    cinema_id = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    contact_number = scrapy.Field()

class ActorItem(scrapy.Item):
    # Actor table fields
    actor_id = scrapy.Field()
    actor_name = scrapy.Field()

class ScreeningRoomItem(scrapy.Item):
    # ScreeningRoom table fields
    room_id = scrapy.Field()
    cinema_name = scrapy.Field()
    room_number = scrapy.Field()
    seat_count = scrapy.Field()
class ScreeningItem(scrapy.Item):
    # Screening table fields
    screening_id = scrapy.Field()
    movie_name = scrapy.Field()
    room_number = scrapy.Field()
    screening_time = scrapy.Field()
    price = scrapy.Field()

class MovieActorItem(scrapy.Item):
    # MovieActor table fields
    movie_name = scrapy.Field()
    actor_name = scrapy.Field()
    role = scrapy.Field()

class MovieItem(scrapy.Item):
    # Movie table fields
    movie_id = scrapy.Field()
    title = scrapy.Field()
    synopsis = scrapy.Field()
    release_date = scrapy.Field()
    director = scrapy.Field()
    rating = scrapy.Field()
    poster_url = scrapy.Field()
    production_region = scrapy.Field()
    tags = scrapy.Field()
    collection_count = scrapy.Field()

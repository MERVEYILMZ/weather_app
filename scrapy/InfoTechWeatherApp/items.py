# items.py
import scrapy

class CityItem(scrapy.Item):
    country = scrapy.Field()
    city_municipality = scrapy.Field()
    state_province = scrapy.Field()
    population = scrapy.Field()

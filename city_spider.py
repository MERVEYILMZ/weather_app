# city_spider.py
import scrapy
from InfoTechWeatherApp.items import CityItem

class CitySpider(scrapy.Spider):
    name = 'city_spider'
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population',
        'https://en.wikipedia.org/wiki/Municipalities_of_the_Netherlands',
        'https://en.wikipedia.org/wiki/List_of_most_populous_municipalities_in_Belgium'
    ]

    def parse(self, response):
        if "United_States" in response.url:
            return self.parse_usa(response)
        elif "Netherlands" in response.url:
            return self.parse_netherlands(response)
        elif "Belgium" in response.url:
            return self.parse_belgium(response)

    def parse_usa(self, response):
        country = "United States"
        table_xpath = '//*[@id="mw-content-text"]/div[1]/table[5]'
        rows = response.xpath(f'{table_xpath}/tbody/tr')        
        
        for row in rows:
            yield CityItem(
                country=country,
                city_municipality=row.xpath('./td[1]/i/a/text()').get(),
                state_province=row.xpath('./td[2]/a/text()').get(),
                population=row.xpath('./td[3]/text()').get(),
            )

    def parse_netherlands(self, response):
        country = "Netherlands"
        table_xpath = '//*[@id="mw-content-text"]/div[1]/table[3]'
        rows = response.xpath(f'{table_xpath}/tbody/tr')        
        
        for row in rows:

            yield CityItem(
                country=country,
                city_municipality=row.xpath('./th/table/tbody/tr/td[2]/a/text()').get(),
                state_province=row.xpath('./td[2]/a/text()').get(),
                population=row.xpath('./td[3]/span/text()').get(),
            )

    def parse_belgium(self, response):
        country = "Belgium"
        table_xpath = '//*[@id="mw-content-text"]/div[1]/table'
        rows = response.xpath(f'{table_xpath}/tbody/tr')        
        
        for row in rows:
            yield CityItem(
                country=country,
                city_municipality=row.xpath('./td[2]/a/text()').get(),
                state_province=row.xpath('./td[9]/a/text()').get(),
                population=row.xpath('./td[7]/text()').get(),
            )

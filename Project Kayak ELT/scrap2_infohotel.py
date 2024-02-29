import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

urltoscrap = pd.read_csv("urltoscrap.csv", index_col=0, sep=",")


class YelpSpider(scrapy.Spider):

    name = "booking_geoloc"

    start_urls = [url for url in urltoscrap["url"]]

    def parse(self, response):
        return {
                    'name' : response.xpath('//*[@id="hp_hotel_name"]/div/h2/text()').get(),
                    'adresse' : response.xpath('//*[@id="showMap2"]/span[1]/text()').get(),
                    'url' : response.url,
                    'lat' : response.xpath('//*[@id="hotel_sidebar_static_map"]').attrib["data-atlas-latlng"].split(",")[0],
                    'lng' : response.xpath('//*[@id="hotel_sidebar_static_map"]').attrib["data-atlas-latlng"].split(",")[1],
                    'score' : response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div/text()').get(),
                    #'score' : response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div[1]/text()').get(),
                    'description' : response.xpath('//*[@id="property_description_content"]/div/p/text()').get(),
                }


# Name of the file where the results will be saved
filename = "info_hotels" + ".json"

# If file already exists, delete it before crawling (because Scrapy will
# concatenate the last and new results otherwise)
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log
## FEEDS => Where the file will be stored
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/116.0.0.0',
    'LOG_LEVEL': logging.INFO,
    'DOWNLOAD_DELAY': 5,
    "AUTOTHROTTLE_ENABLED": True,
    "COOKIES_ENABLED": False,
    "FEEDS": {
        'src/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(YelpSpider)
process.start()
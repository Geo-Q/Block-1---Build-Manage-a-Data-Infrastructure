import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

df_5city = pd.read_csv("city_weather_classement.csv", index_col=0, sep=",")
city_final_list = list(df_5city['Villes'])
cityid_final_list = list(df_5city['ID_city'])

class YelpSpider(scrapy.Spider):

    name = "booking"

    start_urls = [
        'https://www.booking.com/',
    ]

    def parse(self, response):
        for i in range(len(city_final_list)):
            city = city_final_list[i]
            city_id = cityid_final_list[i]
            city_rank = (i + 1)
            request = scrapy.FormRequest.from_response(
                response,
                formdata={'ss': city_final_list[i]},
                callback=self.after_search,
                cb_kwargs={'city' : city, 'city_id' : city_id, 'city_rank' : city_rank}
            )
            yield request

    def after_search(self, response, city, city_id, city_rank):#argid
        city = response.cb_kwargs.get('city')
        city_id = response.cb_kwargs.get('city_id')
        city_rank = response.cb_kwargs.get('city_rank')
        urls = response.xpath('/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a')

        for url in urls:
            yield {
                    'city_orgn' : city,
                    'city_id' : city_id,
                    'city_rank' : city_rank,
                    'url' : url.attrib["href"],
                }

# Name of the file where the results will be saved
filename = "url_hotels" + ".json"

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
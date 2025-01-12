# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Field


class EmallsShopItems(scrapy.Item):
    name = Field()
    products = Field()
    token = Field()
    url = Field()
    

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
    



class ProductItem(scrapy.Item):
    id = Field()
    title = Field()
    titlefa = Field()
    link = Field()
    image = Field()
    category = Field()
    rate = Field()
    offcount = Field()
    price = Field()
    pprice = Field()
    discountpercent = Field()
    maxprice = Field()
    lupdate = Field()
    buyTitle = Field()
    buyLink = Field()
    spec = Field()
    used = Field()

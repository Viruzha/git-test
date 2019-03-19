# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MtsbwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    serial_id=scrapy.Field()
    name=scrapy.Field()
    price=scrapy.Field()
    kind=scrapy.Field()
    disc_price=scrapy.Field()
    season=scrapy.Field()
    brand_name=scrapy.Field()
    gender=scrapy.Field()
    goods_url=scrapy.Field()
    sell_count=scrapy.Field()
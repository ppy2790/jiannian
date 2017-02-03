# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import  Item,Field


class ArticleItem(Item):

    author = Field()
    article = Field()
    url = Field()
    reads = Field()
    comments = Field()
    likes = Field()
    rewards = Field()
    author_url = Field()
    pub_day = Field()

    focus_num = Field()
    fan_num = Field()
    article_num = Field()
    word_num = Field()
    like_num = Field()


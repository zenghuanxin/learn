# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime


def date_convert(value):
    value = value.strip().replace("·","").strip()
    try:
        create_time = datetime.datetime.strptime(value,'%Y/%m/%d').date()
    except Exception as e:
        create_time = datetime.datetime.now().date()
    return create_time

def get_nums(value):
    search_re = re.search('.*?(\d+).*?', value)
    if search_re:
        nums = int(search_re.group(1))
    else:
        nums = 0
    return nums

def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return None
    else:
        return value

def return_icon(value):
    return value

class LagouJobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field()
    work_years = scrapy.Field()
    degree_need = scrapy.Field()
    job_type = scrapy.Field()
    pulish_time = scrapy.Field()
    tags = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field()
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()

class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class JobboleItem(scrapy.Item):
    source_url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    icon = scrapy.Field(
        output_processor = MapCompose(return_icon)
    )
    icon_path = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor = Join(",")
    )
    create_time = scrapy.Field(
        input_processor = MapCompose(date_convert)
    )


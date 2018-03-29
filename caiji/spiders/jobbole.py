# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from caiji.items import JobboleItem,ArticleItemLoader
from caiji.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        #1.获取文章列表页中的文章的url并交给scrapy下载后并进行解析
        #2.获取下一页的URL并交给scrapy进行下载，下载完成后交给parse进行解析
        '''

        #解析列表页中的所有文章URL，并交给scrapy下载后并进行解析

        post_nodes = response.xpath('//div[@id="archive"]/div[contains(@class,"floated-thumb")]/div[@class="post-thumb"]/a')
        for post_node in post_nodes:
            post_url = post_node.xpath('@href').extract_first()
            icon = post_node.xpath('img/@src').extract_first()
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.content_parse,meta={'icon':icon})
        next_url = response.xpath('//div[contains(@class,"navigation")]/a[contains(@class,"next")]/@href').extract_first("")
        if next_url:
            yield Request(url=next_url,callback=self.parse)

    def content_parse(self,response):
        # Jobbole_item = JobboleItem()
        # icon = response.meta.get("icon","")
        # source_url = response.url
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # praise_nums = int(response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first(0))
        # fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract_first("")
        # search_re = re.search('.*?(\d+).*?', fav_nums)
        # if search_re:
        #     fav_nums = int(search_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first("")
        # search_re = re.search('.*?(\d+).*?', comment_nums)
        # if search_re:
        #     comment_nums = int(search_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.xpath('//div[@class="entry"]').extract_first("")
        # tags_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tags_list = [tag for tag in tags_list if not tag.strip().endswith("评论")]
        # tags = ','.join(tags_list)
        # create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first("").strip().replace("·","").strip()
        #
        # Jobbole_item['title'] = title
        # Jobbole_item['source_url'] = source_url
        # Jobbole_item['url_object_id'] = get_md5(source_url)
        # Jobbole_item['praise_nums'] = praise_nums
        # Jobbole_item['comment_nums'] = comment_nums
        # Jobbole_item['fav_nums'] = fav_nums
        # Jobbole_item['icon'] = [icon]  #图片下载必须传递数组list
        # Jobbole_item['content'] = content
        # Jobbole_item['tags'] = tags
        # try:
        #     create_time = datetime.datetime.strptime(create_time,'%Y/%m/%d')
        # except Exception as e:
        #     create_time = datetime.datetime.now().date()
        # Jobbole_item['create_time'] = create_time


        #通过itemLoad加载item
        item_loader = ArticleItemLoader(item=JobboleItem(),response=response)
        icon = response.meta.get("icon", "")
        item_loader.add_xpath("title",'//div[@class="entry-header"]/h1/text()')
        item_loader.add_value("source_url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_value("icon",icon)
        item_loader.add_xpath("comment_nums", '//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath("praise_nums", '//span[contains(@class,"vote-post-up")]/h10/text()')
        item_loader.add_xpath("fav_nums", '//span[contains(@class,"bookmark-btn")]/text()')
        item_loader.add_xpath("tags", '//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_xpath("content", '//div[@class="entry"]')
        item_loader.add_xpath("create_time", '//p[@class="entry-meta-hide-on-mobile"]/text()')

        Jobbole_item = item_loader.load_item()

        yield Jobbole_item
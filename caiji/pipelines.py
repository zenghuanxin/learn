# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class JobbolePipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()

class JsonExporterPipeline(object):
    #调用scrapy提供的json export 到处json文件
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii='utf-8')
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost','root','root','jobbole',charset='utf8',use_unicode =True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = '''
            insert into article(title,url,url_object_id,icon,icon_path,comment_nums,fav_nums,praise_nums,tags,content,create_time)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        self.cursor.execute(insert_sql,(item['title'],item['source_url'],item['url_object_id'],item['icon'],item['icon_path'],item['comment_nums'],item['fav_nums'],item['praise_nums'],item['tags'],item['content'],item['create_time']))
        self.conn.commit()
        return item

class MysqlTwistedPipeline(object):#mysql 异步插入, 防止数据太大，使得数据库插入太慢.

    def __init__(self,dppool):
        self.dbpool = dppool

    @classmethod  #初始化一个类，并实例化返回连接池
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)#处理异常
        return item

    def handle_error(self,failure):
        #处理异步插入的异常
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = '''
            insert into article(title,url,url_object_id,icon,icon_path,comment_nums,fav_nums,praise_nums,tags,content,create_time)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cursor.execute(insert_sql, (item['title'], item['source_url'], item['url_object_id'], item['icon'], item['icon_path'], item['comment_nums'],item['fav_nums'], item['praise_nums'], item['tags'], item['content'], item['create_time']))


class JobboleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "icon" in item:
            for ok,value in results:
                icon_file_path = value['path']
            item['icon_path'] = icon_file_path
        return item

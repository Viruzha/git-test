# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class MtsbwPipeline(object):
    CONN=MySQLdb.connect(host='localhost',port=12000,user='root',passwd='1234',db='data',charset='utf8')
    conn=CONN.cursor()
    def process_item(self, item, spider):
        self.conn.execute(f'''
        INSERT INTO mtsbw 
        VALUES('{item['serial_id']}',
        '{item['name']}',
        '{item['price']}',
        '{item['kind']}',
        '{item['disc_price']}',
        '{item['season']}',
        '{item['brand_name']}',
        '{item['gender']}',
        '{item['goods_url']}',
        '{item['sell_count']}');
        commit;
        ''')
        
        
        
        
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# 写入mongodb
# 对抓取的数据进行后续处理，比如入库，去重等
# 如果改动pipline，要在settings中设置启动
class JobbolePipeline(object):
	# 下面连接数据库代码也可以写在process_item方法中，但是写在__init__中只需要连接一次
	def __init__(self):
		self.client = pymongo.MongoClient('60.205.211.210',27017)
		self.db = self.client['test']
		self.collection = self.db['bole_online']

	# 这个形参item是接收scrapy脚本传过来的items，这个方法会将items自动拆分为键值对来进行写入数据库等后续操作
	def process_item(self, item, spider):
		print(item)
		# 注意写入mongo时，要dict()强转一下，否则会报TypeError
		self.collection.insert(dict(item))
		return item # 是为了写多条数据时将实体传给下一个

# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import  Request
from Jobbole.items import JobboleItem

class BoleSpider(scrapy.Spider):
	name = 'bole'
	allowed_domains = ['jobbole.com']
	start_urls = ['http://python.jobbole.com/all-posts/']

	def parse(self, response):
		# 出现xe/ decode解码一下
		# print(response.body.decode('utf-8'))
		items = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
		# print(len(items)) 20
		for item in items:
			# 文章链接 extract()返回的是list extract_first()返回的是一个值 str类型
			art_url = item.xpath('./@href').extract_first()
			# 文章标题
			art_title = item.xpath('./@title').extract_first()
			# 文章图片链接
			art_img_url = item.xpath('./img/@src').extract_first()
			# print(art_list,art_title,art_img_url)

			# 请求文章链接
			yield Request(url=art_url,callback=self.parse_content,meta={'art_url':art_url,'art_title':art_title,'art_img_url':art_img_url})

		# 实现翻页 在解析页面的函数中写代码  点击下一页
		# 获得下一页的链接
		next_page = response.xpath('//div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract_first()
		print(next_page)
		print('正在翻页----第%s页----' % (next_page[-2:-1]))
		if not next_page:
			print('翻页完毕！！！')
		yield Request(url=next_page, callback=self.parse)

	def parse_content(self,response):
		# 实例化items  给items字段赋值
		items = JobboleItem()
		# 文章创建时间 -- 这个函数会传到上面的for循环中 所以这里都是取第一个
		create_time = response.xpath('//div[@class="entry-meta"]/p/text()').extract_first().strip()
		create_time = create_time.replace(' ·','').replace('/','-')
		items['create_time'] = create_time
		# 内容 -- 只抓取了p标签内容
		art_content = response.xpath('//div[@class="entry"]/p/text()').extract()
		items['art_content'] = art_content
		# 接收传下来的数据
		art_url = response.meta['art_url']
		items['art_url'] = art_url
		art_title = response.meta['art_title']
		items['art_title'] = art_title
		art_img_url = response.meta['art_img_url']
		items['art_img_url'] = art_img_url
		# 拼接数据
		art_list = {
			'art_url' : art_url,
			'art_title':art_title,
			'art_img_url':art_img_url,
			'create_time':create_time,
			'art_content':art_content
		}
		# 将数据返回给piplines.py
		return items
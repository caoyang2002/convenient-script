# -*- coding: utf-8 -*-
import scrapy
from PhotoSpider.items import PhotospiderItem
import re


class GetphotospiderSpider(scrapy.Spider):
    name = 'getPhotoSpider'
    allowed_domains = ['mn52.com']
    start_urls = ['https://www.mn52.com/txj/']  # 这里填写头像集的url，当然，可以将txj改成你想要的分类

    # 添加__init__函数用于存放页数
    def __init__(self):
        self.page_index = 1

    def parse(self, response):
        # 填空题开始了！！从这里xpath在start_urls上获取的消息，过滤出url
        for photo in response.xpath('//div[@class="content"]/div[2]/div'):
            url = photo.xpath('./div/a/@href').extract_first()
            # 这里要给url加上https，否则会。。无法访问
            url_new = 'https:' + url
            # 将新的url甩给下面的函数，也就是爬取下级页面信息~
            yield scrapy.Request(url_new, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        # 过滤从上面丢下来的信息，得到photo_url，也就是真实的图片下载链接
        for photos in response.xpath('//div[@id="originalpic"]/img'):
            # 这个是正则表达式，用来筛选出//image.mn52.com/img/allimg/190906/8-1ZZ6094322-53.jpg中的8-1ZZ6094322-53
            # pattern = '\w*?\-\w+'
            pattern = r'\w*?\-\w+'  # 使用原始字符串
            # 这个 PhotospiderItem 是用来存放的，在items.py里面
            item = PhotospiderItem()
            item['photo_url'] = photos.xpath('./@src').extract_first()
            item['photo_id'] = re.search(pattern, item['photo_url']).group()
            yield item
        # 这是用来执行下一页的
        self.page_index += 1
        # 下面的12代表第十二个分类（头像集），修改分类的时候需要同时将这个12一起修改（比如爬取美食图片要将12改成10）
        next_link = 'https://www.mn52.com/mstp/list_12_' + \
            str(self.page_index) + '.html'
        yield scrapy.Request(next_link, callback=self.parse)

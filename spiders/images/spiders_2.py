# -*- coding: utf-8 -*-
# [url=home.php?mod=space&uid=238618]@Time[/url]    : 2021/1/19 16:35
# [url=home.php?mod=space&uid=686208]@AuThor[/url]  : Purple soul-吾爱
# @FileName: 爬虫成品.py

import requests
import re
import os
import sys
import time
from urllib.request import urlopen
from tqdm import tqdm

'''创建一个类'''


class Color:
    def __init__(self):
        self.dit1 = {}
        self.downsize = 0
        self.file_address = 0
        '''添加请求头'''
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        self.port = 'https://xxxxx.xyz'
        '''子网站地址'''
        self.port_1 = '/h/dalu/'
        self.port_2 = '/h/rihan/'
        self.port_3 = '/h/oumei/'
        self.port_4 = '/h/sanji/'
        self.port_5 = '/h/dongman/'
        self.port_6 = '/h/tupian/'
        self.port_8 = '/h/duanpian/'

    '''视频下载'''

    def download_from_url(self, url, moive_name, moive_num):
        """
        @param: url to download file
        @param: moive_name place to put the file
        :return: bool
        """

        # 获取文件长度
        try:
            file_size = int(urlopen(url).info().get('Content-Length', -1))
        except Exception as e:
            print(e)
            print("错误，访问url: %s 异常" % url)
            return False
        # 判断本地文件夹是否存在

        if not os.path.exists(self.dir_name[0]):
            os.makedirs(self.dir_name[0])
        # 判断本地文件存在时
        if os.path.exists(self.dir_name[0] + '/' + moive_name + self.file_geshi):
            # 获取文件大小
            first_byte = os.path.getsize(
                self.dir_name[0] + '/' + moive_name + self.file_geshi)
        else:
            # 初始大小为0
            first_byte = 0

        # 判断大小一致，表示本地文件存在
        if first_byte >= file_size:
            print("文件已经存在,无需下载")
            return file_size

        header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
        pbar = tqdm(
            total=file_size, initial=first_byte,
            unit='B', unit_scale=True, desc=url.split('/')[-1])
        # 访问url进行下载
        time.sleep(1)
        req = requests.get(url, headers=header, stream=True)
        try:
            with (open(self.dir_name[0] + '/' + moive_name + self.file_geshi, 'wb')) as f:
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(1024)
        except Exception as e:
            print(e)
            return False
        pbar.close()
        return True

    '''请求视频网页链接'''

    def request_video_link(self):
        self.title = re.findall(
            '<p><a href="(.*?)">(.*?)</a></p>', self.html)  # 获取当前页视频链接和标题
        self.dir_name = re.findall(
            "<a href='/'>.*?</a> > <a href='.*?'>(.*?)</a> > </div>", self.html)  # 获取分类文件夹名称
        # 将列表转换为字典
        dit1 = dict(self.title)
        for d in dit1.keys():
            if re.match('^/h\/\w+\/', d):
                movie_name = dit1[d]
                print("{:.10s}\t\t{:.60s}".format(
                    d, dit1[d]))  # 打印获取到的子链接及视频名称
                file_address = requests.get(
                    self.port + d, headers=self.headers)
                file_address_html = file_address.text
                # print(file_address_html)
                self.file_obtain_geshi = re.findall(
                    'id=".*?">(.*?)</span><span style=".*?"', file_address_html)  # 获取文件格式字符串
                file_address = re.findall(
                    'id=".*?">(.*?)</span><span style=".*?"', file_address_html)  # 得到视频下载地址
                self.file_obtain_geshi = ''.join(
                    self.file_obtain_geshi).split(".")[-1:]  # 对得到的地址格式进行切片
                self.file_geshi = '.' + \
                    str(self.file_obtain_geshi[0])  # 在文件格式前加'.'
                '''视频下载地址是单独的，所以需要获取解析地址来和视频地址拼接'''
                file_address = self.file_down_address + \
                    file_address[0]  # 将解析地址和获取到的视频地址拼接
                # print(file_address)
                self.download_from_url(file_address, movie_name, d)

    '''获取下一页'''

    def next_request_video_link(self):
        self.request_video_link()
        for url in self.urls:
            self.port_page = self.port_request + url
            print()
            print('当前网页链接为：'+self.port_page)
            self.response = requests.get(
                self.port_request + url, headers=self.headers)
            self.html = self.response.text
            self.request_video_link()

    def dowm_type_choice(self):
        dit = {1: '大陆', 2: '日韩', 3: '欧美', 4: '三级', 5: '动漫', 6: '图片', 7: '短片'}
        print(dit)
        choice_type = eval(input('请选择下载类型（输入数字1-7）:'))
        while not (choice_type in dit.keys()):
            choice_type = eval(input('输入错误请重新输入（输入数字1-7）:'))
        if choice_type == 2:
            self.port_request = self.port + self.port_2
            self.file_down_address = 'https://xxxx.com/mp4/'
        elif choice_type == 3:
            self.port_request = self.port + self.port_3
            self.file_down_address = 'https://xxxx.com/mp4/'
        elif choice_type == 4:
            self.port_request = self.port + self.port_4
            self.file_down_address = 'https://xxxx.com/mp4/'
        elif choice_type == 5:
            self.port_request = self.port + self.port_5
            self.file_down_address = 'https://xxxx.com/mp4/'
        elif choice_type == 6:
            self.port_request = self.port + self.port_6
            self.file_down_address = 'https://xxxxx.com/mp4/'
        elif choice_type == 7:
            self.port_request = self.port + self.port_8
            self.file_down_address = 'https://xxxxx.com/mp4/'
        else:
            self.port_request = self.port + self.port_1
            self.file_down_address = 'https://xxxxx.com/mp4/'
        self.response = requests.get(self.port_request, headers=self.headers)
        self.html = self.response.text
        self.urls = re.findall(
            "<option value='(.*?)'>.*?</option>", self.html)  # 获取当前类型所有子网页链接
        print('当前类型为：%d :' % (choice_type), end='')
        print(dit.get(choice_type))
        print(self.port_request)
        print('****************************开始下载****************************')
        rx_seckill.next_request_video_link()


if __name__ == '__main__':
    a = """                                                                                                                                        
        oooooooooo.  o888o      o888o              d88b'        'P88b    oo
        `888'   `Y8b  888        888                Y8bo.      .ob8Y    ,"8 
         888     d88' 888        888    .od88bo.    `Y888o.  .o888Y'   oooo 
         888ooo888Y   888        888   d8'    `8b      `"Y8888Y"'      `888 
         888 888.     888        888   888    888    .o888Y  Y888o.     888
         888  `88b.   `Y8b      d88'  `Y8b    d88'  .ob8Y       Y8bo.   888 
        o888o  o888o     Y8bod8P'       `88od8P'    o888o       o888o  o888o
    功能列表：                                                                                
    1.选择下载类型
    吾爱破解论坛 http://www.52pojie.cn
        """
    print(a)
    rx_seckill = Color()
    choice_function = input('请选择:')
    if choice_function == '1':
        rx_seckill.dowm_type_choice()
    else:
        print('没有此功能')
        sys.exit(1)

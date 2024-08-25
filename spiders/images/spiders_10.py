# coding=utf-8
import os
import re
import urllib
from time import sleep

import requests
from lxml import etree


host = "http://www.mzitu.com"

category = ['xinggan']

start_page = 124973
end_page = start_page + 1


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def save_img(img, dir_path, file_name):
    headers = {"Referer": "http://www.mzitu.com",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    file_content = requests.get(img, headers=headers)
    if file_content.status_code != 200:
        print(img, "下载失败")
    else:
        # urllib.request.urlretrieve(img, dir_path + file_name)
        with open(dir_path + file_name, "wb") as f:
            f.write(file_content.content)
        print("保存图片" + dir_path + file_name + "成功")


def get_html(url, page):
    sleep(5)
    new_url = url+"/"+str(page)
    headers = {"Referer": "http://www.mzitu.com",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    response = requests.get(new_url, headers=headers)
    print(response.headers)
    html = etree.HTML(response.content)
    title = html.xpath("/html/body/div[2]/div[1]/h2/text()")
    img_url = html.xpath("/html/body/div[2]/div[1]/div[3]/p/a/img/@src")
    if len(title) > 0 and len(img_url) > 0:
        title = validateTitle(title[0])
        surfix = os.path.splitext(img_url[0])[1]
        title = title + surfix

        dir_path = "/www/spider/images/"
        print(dir_path+title)
        print(img_url)
        save_img(img_url[0], dir_path, title)


try:
    for i in range(start_page, int(end_page)):
        url = host + '/' + str(i)
        headers = {"Referer": "http://www.mzitu.com",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
        response = requests.get(url, headers=headers)
        print(url)
        print(response.headers)
        if response.status_code == 200:
            html = etree.HTML(response.content)
            total_page = html.xpath(
                "/html/body/div[2]/div[1]/div[4]/a[5]/span/text()")
            if len(total_page) > 0:
                for i in range(1, int(total_page[0]) + 1):
                    get_html(url, i)
        # 获取总页数

except Exception as e:
    print(str(e))

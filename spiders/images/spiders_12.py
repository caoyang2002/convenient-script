# encoding: utf-8
import sys
import requests
import re
import time
import os
from bs4 import BeautifulSoup
count = 4
urlHead = 'http://www.bjmingding.com/post/'
urlFoot = '.html'


def SaveMovie(link, image_name):  # 获取网址
    try:
        time1 = time.time()
        # 没有这行，打印的结果中文是乱码
        # link = 'http://puliting.dgzcad.com/puliting/1553829923537.mp4'
        dest_resp = requests.get(link)
        # 视频是二进制数据流，content就是为了获取二进制数据的方法
        data = dest_resp.content
        # 保存数据的路径及文件名
        root = '/Users/caoyang/Desktop/SCRIPT/vedio'
        path = root + image_name+str(count)+'.mp4'
        if not os.path.exists(root):
            os.mkdir(root)
        f = open(path, 'wb')
        f.write(data)
        f.close()
        time2 = time.time()
        print('ok,下载完成!')
        print('总共耗时：' + str(time2 - time1) + 's')
    except:
        return ""


def getHtmlurl(url):  # 获取网址
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getMovieLink(html):
    soup = BeautifulSoup(html)
    aaa = soup.find('ul', class_='row')
    All_MovieLinks = soup.select('body script')
    i = 1
    lll = ' '
    for MovieLink in All_MovieLinks:
        str = MovieLink.get_text()
        print(MovieLink)
        if i == 2:
            s = str.find('url: ')
            t = str.find('pic')
            lll = str[s+6:t].split('\'')[0]
            print(lll)
            break
        i += 1
    # r'<a\sclass=".*?"\starget=".*?"\shref=".*?">(.*)</a>'  # 正则表达式
    reg = r'<h1 class="f-22 txt-ov">(.*)</h1>'
    reg_ques = re.compile(reg)  # 编译一下正则表达式，运行的更快
    image_name_arr = reg_ques.findall(html)  # 匹配正则表达式
    image_name = image_name_arr[0]
    SaveMovie(lll, image_name)


def main(url):
    # url='http://www.ivsky.com/bizhi/yourname_v39947/'
    html = (getHtmlurl(url))
    # print(html)
    return getMovieLink(html)


if __name__ == '__main__':
    for i in range(1, 100):
        count += 1
        url = urlHead+str(6765+count)+urlFoot
        try:
            main(url)
        except:
            pass

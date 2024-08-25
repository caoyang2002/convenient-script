import wget
from requests_html import HTMLSession
import urllib
import urllib3
import os
import random
urllib3.disable_warnings()


BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.70"
                   ]

header = {"Content-Type": "application/json", }

header['User-Agent'] = random.choice(user_agent_list)


def downloadPic(url, kw, pic_num, out_path, pic_type='jpg'):
    '''
    @url: 待下载的url
    @kw：图片关键词
    @pic_num：计划下载的数量
    @out_path：图片下载的相对路径
    @pic_type：图片类型
    '''
    img_name = r'{}-{}.{}'.format(kw, pic_num, pic_type)
    img_full_name = r'{}\{}\{}'.format(BASE_DIR, out_path, img_name)

    res = wget.download(url=url, out=img_full_name)
    if res:
        print('img:{} has downloaded!'.format(img_name))


def getPicUrl(req_url):
    session = HTMLSession()
    res = session.get(url=req_url, headers=header, verify=False)
    img_box = res.html.links

    for i in img_box:
        if 'jpg' in i or 'png' in i or 'jpeg' in i:
            return i


def main(kw='美女', num=10, img_path='img'):
    '''
    @kw: 关键词
    @num: 计划下载的数量
    '''
    # 将中文关键词编码
    kwd = urllib.parse.quote(kw)

    # 生成页面url
    for i in range(num):
        index = i+1
        base_url = 'https://pic.sogou.com/d?query={}&forbidqc=&entityid=&preQuery=&rawQuery=&queryList=&st=&did={}'.format(
            kwd, index)

        # 根据页面url，获取图片url
        url = getPicUrl(base_url)

        # 执行下载
        downloadPic(url=url, kw=kw, pic_num=index, out_path=img_path)


if __name__ == "__main__":
    main(kw='美女', num=10)

import urllib.request
from lxml import etree
import os


def creat_request(page):
    if (page == 1):
        url = 'https://pic.netbian.com/index.html'
    else:
        url = 'https://pic.netbian.com/index_'+str(page)+'.html'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

    # 创建请求对象
    request = urllib.request.Request(url=url, headers=headers)
    return request


def get_page(request):
    # 发送请求并获取响应
    response = urllib.request.urlopen(request)
    # 读取响应内容
    content = response.read().decode('gbk')
    return content


def dow_load(content):
    if not os.path.exists('美图'):
        os.makedirs('美图')

    tree = etree.HTML(content)
    # 提取图片地址和名称
    src_list = tree.xpath('//ul/li/a//img/@src')
    name_list = tree.xpath(('//ul/li/a//img/@alt'))

    # 下载图片
    for i in range(len(src_list)):
        src = src_list[i]
        name = name_list[i]
        url = 'https://pic.netbian.com'+src
        filename = '美图/'+name + str(i+1) + '.jpg'
        urllib.request.urlretrieve(url=url, filename=filename)
        print(name+'.jpg 下载完成')


if __name__ == '__main__':
    start_page = int(input('请输入下载的起始页：'))
    end_page = int(input('请输入下载的结束页：'))

    for page in range(start_page, end_page+1):
        # 创建请求对象
        request = creat_request(page)
        # 获取源码
        content = get_page(request)
        # 下载文件
        dow_load(content)

import urllib.request
from lxml import etree  # type: ignore
import re
import os
import datetime

# 下载图片（获取原图链接并下载）


def downloadImage(url, pathway):
    response = urllib.request.urlopen(url)
    content = response.read().decode(encoding='utf-8')
    dom = etree.HTML(content)
    src = dom.xpath('//div/ul[@id="pictureurls"]/li/div/a/img/@src')
    # 获取图片链接和名称并下载图片
    # pattern = '\w+\-\w+'
    pattern = '\w+\-\w+'
    firstsrc = src[0]
    filetype = firstsrc[-4:]

    headers = [('Host', 'www.mn52.com'), ('Connection', 'keep-alive'),  ('Cache-Control', 'max-age=0'),
               ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'),
               ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'),
               ('Accept-Encoding', 'gzip, deflate, br'),
               ('Accept-Language', 'zh-CN,zh;q=0.9'),
               ('If-None-Match', '5d652a1c-3d43'),
               ('Referer', 'https://www.mn52.com/xingganmeinv/'),
               ('If-Modified-Since', 'Tue, 27 Aug 2019 10:09:54 GMT')]
    opener = urllib.request.build_opener()
    opener.addheaders = headers
    for img in src:
        name = re.search(pattern, img).group()
        if str(img[1:4]) == "img":
            imgUrl = "https://image.mn52.com" + img
        else:
            imgUrl = "https:" + img

        data = opener.open(imgUrl)
        # 储存路径
        path = pathway + "/" + str(name) + str(filetype)
        f = open(path, "wb")
        f.write(data.read())
        f.close()
        print("图片下载成功："+imgUrl)

# 构造分类的 url
# typeNum 性感美女-->1  清纯美女-->2  韩国美女-->3  欧美图片-->4  美女明星-->5


def getUrl(typeNum):
    type = ""
    if typeNum == 1:
        type = "xingganmeinv"
    elif typeNum == 2:
        type = "meihuoxiezhen"
    elif typeNum == 3:
        type = "rihanmeinv"
    elif typeNum == 4:
        type = "jingyannenmo"
    elif typeNum == 5:
        type = "meinvmingxing"
    url1 = "https://www.mn52.com/"
    url2 = "/list_"
    url = url1 + type + url2 + str(typeNum) + "_"
    return url


# 提示信息
print("################################################################################")
print("#                                                                              #")
print("#            (1)作者：ShibaInu  mn52图库：https://www.mn52.com                 #")
print("#                                                                              #")
print("#            (2)==> 需要输入：文件储存路径,例如 D:/image                       #")
print("#                   下载的图片都会保存在这个文件夹                             #")
print("#                                                                              #")
print("#            (3)==> 需要输入：图片类别 Number                                  #")
print(
    "#                   性感美女 ==>[ 1 ]                                          #")
print(
    "#                   清纯美女 ==>[ 2 ]                                          #")
print(
    "#                   韩国美女 ==>[ 3 ]                                          #")
print(
    "#                   欧美图片 ==>[ 4 ]                                          #")
print(
    "#                   美女明星 ==>[ 5 ]                                          #")
print("#                                                                              #")
print("#            (4)==> 需要输入：下载的起始页和末尾页的页码数                     #")
print(
    "#                   起始页[ startPage ]                                        #")
print(
    "#                   末尾页[ endPage(不包含末尾页)]                             #")
print("#                                                                              #")
print("################################################################################")
print("")

pathway = input("  ①请输入文件存储路径(例如 D:/image)：")
print("")

typeNum = input("  ②请输入下载的类别：")
urlList = getUrl(int(typeNum))
print("")

startPage = input("  ③请输入起始页 startPage：")
print("")

endPage = input("  ④请输入末尾页 endPage：")
print("")

print("   == 即将开始精彩资源的下载 == ")
print("")

startNum = int(startPage)
endNum = int(endPage)

startTime = datetime.datetime.now()
for n in range(startNum, endNum):
    realurl = urlList + str(n) + '.html'
    response = urllib.request.urlopen(realurl)
    content = response.read().decode(encoding='utf-8')
    dom = etree.HTML(content)
    src = dom.xpath('//div[@id="waterfall"]/ul/li/div/a/@href')

    for img in src:
        path = 'https://www.mn52.com' + img
        indexImg = src.index(img)
        # 异常处理：遇到异常信息跳过
        try:
            print("开始下载该组图：" + path)
            starttime = datetime.datetime.now()
            downloadImage(path, pathway)
            endtime = datetime.datetime.now()
            print("  下载成功，耗时：" + str(endtime - starttime))
            print("  =========> 第" + str(indexImg+1) + "组图片下载完成 <=========")
            print("")
        except Exception as e:
            print("  =========> 第" + str(indexImg+1) + "组图片下载完成 <=========")
            pass
        continue

    print("===========================> 第" + str(n) +
          "个图片列表下载完成 <===========================")

endTime = datetime.datetime.now()

print("下载成功，耗时：：" + str(endTime - startTime))

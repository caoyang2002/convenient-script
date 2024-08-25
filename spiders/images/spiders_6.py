import requests as rq
from bs4 import BeautifulSoup
import sys
import time
import os


class images():
    def __init__(self, dicts, head, imghead):
        self.dicts = dicts
        self.head = head
        self.imghead = imghead

    def getreques(self, url, head):
        return rq.get(url, headers=head)

    def getimgtable(self, data):
        print(BeautifulSoup(data, 'html.parser').find_all('img'))
        return BeautifulSoup(data, 'html.parser').find_all('img')

    def createdir(self):
        dir = sys.path[0]+'\\src\\'
        for path in self.dicts.values():
            if os.path.exists(dir+path) == False:
                os.mkdir(dir+path)
        return dir

    def writeimg(self, dir, name, img, page, i):
        f = open(dir+name+'\\'+page+'--'+i+'.jpg', 'wb')
        f.write(self.getreques(img.get('data-original'), self.imghead).content)

    def run(self):
        dir = self.createdir()
        for pages, name in self.dicts.items():
            for page in range(1, pages):
                i = 0
                print('https://www.mzitu.com/'+name+'/page/'+str(page))
                for img in self.getimgtable(self.getreques('https://www.mzitu.com/'+name+'/page/'+str(page)+'/', self.head).text):
                    print(img)
                    if 'data-original' in str(img):
                        i += 1
                        self.writeimg(dir, name, img, str(page), str(i))


def run_main():
    dicts = {
        193: 'xinggan',
        30: 'japan',
        35: 'mm',
    }
    head1 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'Hm_lvt_cb7f29be3c304cd3bb0c65a4faa96c30=1636799900,1636806558; Hm_lpvt_cb7f29be3c304cd3bb0c65a4faa96c30=1636806558',
        'if-modified-since': 'Wed, 10 Nov 2021 13:09:33 GMT',
        'sec-ch-ua': '"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'
    }
    head = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; MIX 2 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.9',
        'cookie': 'Hm_lvt_450e019eee95b5c453f724272dbc091d='+str(int(time.time())),
        'cookie': 'Hm_lpvt_450e019eee95b5c453f724272dbc091d='+str(int(time.time())),
        'x-requested-with': 'com.i8b073894b8d0cf7a'
    }
    imghead = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; MIX 2 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'referer': 'https://m.mzitu.com/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.9',
        'x-requested-with': 'com.i8b073894b8d0cf7a'
    }
    images(dicts, head, imghead).run()


run_main()

from bs4 import BeautifulSoup
import requests
import time

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
}

time.sleep(4)
num = 1
page = 1
for page in range(1, 6):
    if page == 1:
        new_url = 'http://www.ypppt.com/moban/lunwen/'
    else:
        new_url = [
            'http://www.ypppt.com/moban/lunwen/list-{}.html'.format(page)]
        # 列表（被称为打了激素的数组）：可以存储任意数据类型的集合（一个变量中可以存储多个信息）,相当于数组
        new_url = new_url[0]
    #   new_url = 'http://www.ypppt.com/moban/lunwen/list-{}.html'.format(page)
    print("正在爬取" + new_url)
    response = requests.get(new_url, headers=headers)
    response.encoding = 'utf-8'
    jx = BeautifulSoup(response.content, 'lxml')
    mains = jx.find('ul', {'class': 'posts clear'})
    main_ppts = mains.find_all('li')
    for i in main_ppts:
        a = i.a.attrs['href']
        print('http://www.ypppt.com' + a)
        b = requests.get('http://www.ypppt.com' + a)
        b.encoding = b.apparent_encoding

        c = BeautifulSoup(b.content, 'lxml')
        down = c.find('div', {'class': 'button'})
        down1 = down.a.attrs['href']
        down_1 = requests.get('http://www.ypppt.com' + down1)
        down_1.encoding = down_1.apparent_encoding

        down_2 = BeautifulSoup(down_1.content, 'lxml')
        e = down_2.find('ul', {'class': 'down clear'})
        f = e.find('li')
        downlaod_url = f.a.attrs['href']
        download = requests.get(url=downlaod_url, headers=headers).content

        with open(str(num) + '.zip', 'wb') as f:
            f.write(download)
        print(str(num) + '下载成功')
        num += 1

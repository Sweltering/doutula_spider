# 爬取斗图啦网站最新表情包（多线程）

import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading


# 生产者生产每一页图片的url和图片名称
class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
        'Referer': 'http://www.doutula.com/photo/list/?page=2'
    }

    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():  # 如果队列中没有数据就退出
                break
            url = self.page_queue.get()  # 从队列中取出页面的url
            self.parse_page(url)

    # 数据提取，提取图片的url和图片名称
    def parse_page(self, url):
        response = requests.get(url, headers=self.headers)
        html = response.text

        # 解析图片
        ehtml = etree.HTML(html)  # 返回一个<Element html at 0x2c3f84f2c8>对象
        imgs = ehtml.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')  # 爬取所有图片的img标签
        for img in imgs:
            img_url = img.get('data-original')  # 通过get获取所有图片的url
            alt = img.get('alt')  # 通过get获取所有图片的名字
            alt = re.sub(r'[\?？\.，。！! \*]', '', alt)  # 将获取到的图片的名字中出现的非法字符替换为空
            suffix = os.path.splitext(img_url)[1]  # 获取图片url后面的扩展名
            filename = alt + suffix  # 图片名称
            self.img_queue.put((img_url, filename))


# 消费者下载图片保存本地
class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():  # 如果两个队列中没有数据就退出
                break
            img_url, filename = self.img_queue.get()  # 在队列中取出图片的url和文件名
            request.urlretrieve(img_url, 'images/'+filename)  # urlretrieve将图片下载保存在本地
            print(filename+'    下载完成!')


# 前100页的url
def main():
    page_queue = Queue(100)  # 页面url队列
    img_queue = Queue(1000)  # 图片队列
    for x in range(1, 100):
        url = 'http://www.doutula.com/photo/list/?page={}'.format(x)
        page_queue.put(url)

    # 5个生产者
    for x in range(5):
        t = Producer(page_queue, img_queue)
        t.start()

    # 5个消费者
    for x in range(5):
        t = Consumer(page_queue, img_queue)
        t.start()


if __name__ == '__main__':
    main()

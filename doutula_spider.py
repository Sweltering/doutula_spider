# 爬取斗图啦网站最新表情包（单线程）

import requests
from lxml import etree
from urllib import request
import os
import re


# 数据提取
def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
        'Referer': 'http://www.doutula.com/photo/list/?page=2'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # 解析图片
    ehtml = etree.HTML(html)  # 返回一个<Element html at 0x2c3f84f2c8>对象
    imgs = ehtml.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')  # 爬取所有图片的img标签
    for img in imgs:
        img_url = img.get('data-original')  # 通过get获取所有图片的url
        alt = img.get('alt')  # 通过get获取所有图片的名字
        alt = re.sub(r'[\?？\.，。！! ]', '', alt)  # 将获取到的图片的名字中出现的非法字符替换为空
        suffix = os.path.splitext(img_url)[1]  # 获取图片url后面的扩展名
        filename = alt + suffix  # 图片名称
        request.urlretrieve(img_url, 'images/'+filename)  # urlretrieve函数:将图片保存在本地


# 前100页的url
def main():
    for x in range(1, 100):
        url = 'http://www.doutula.com/photo/list/?page={}'.format(x)
        parse_page(url)


if __name__ == '__main__':
    main()

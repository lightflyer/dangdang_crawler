# coding: utf-8
from bs4 import BeautifulSoup
import csv
import codecs
import time
import requests
import re


def run():
    start_url = "http://search.dangdang.com/?key=python&act=input&show=big&page_index={}"

    headers = {
        'Host': 'search.dangdang.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.121 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',

    }

    index = 1

    while index <= 21:
        url = start_url.format(index)
        print(url)
        # request = urllib.request.Request(url=url, headers=headers)
        # response = urllib.request.urlopen(request)
        response = requests.get(url=url, headers=headers)
        index = index + 1

        parse_content(response)

        time.sleep(1)


def parse_content(response):
    # print(response.text)
    # with open('dang_test.html', 'wb+') as f:
    #     f.write(response.content)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup.text)
    # pattern_str = '<a title="(.*)"  ddclick='
    # names = re.findall(pattern_str, response.text)
    # print(names)
    temps = soup.find_all('a', class_='pic')
    # print(temps)
    global books
    books = books + temps
    print(f'get books size = {str(len(books))}')


def show_result():
    file_name = 'python_book.csv'

    with codecs.open(file_name, 'w', 'utf-8') as file:
        filed_names = ['书名', '页面地址', '图片地址']
        writer = csv.DictWriter(file, fieldnames=filed_names)

        writer.writeheader()
        for book in books:
            # print(book)
            if len(list(book.children)[0].attrs) == 3:
                img = list(book.children)[0].attrs['data-original']
            else:
                img = list(book.children)[0].attrs['src']

            try:
                writer.writerow({'书名': book.attrs['title'], '页面地址': book.attrs['href'], '图片地址': img})
            except UnicodeEncodeError:
                print('encode error,')

    print(f'write data into {file_name} successfully')


if __name__ == '__main__':
    books = []
    run()
    show_result()

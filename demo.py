#!/usr/bin/env python
# encoding-utf-8

#爬取豆瓣电影TOP250 - 完整示例代码

from bs4 import BeautifulSoup
import requests

DOWNLOAD_URL= 'http://movie.douban.com/top250'

def download_page(url):
    data = requests.get(url).content
    print("the data is downloaded"+ data.decode('utf-8'))
    return data

def main():
    print(download_page(DOWNLOAD_URL))
    print("-----------------------------")
    print("it's over")


def parse_html(html):
    soup = BeautifulSoup(html)
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})

    movie_name_list = []

    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()

        movie_name_list.append(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None

def buy():
    pass

if __name__ == '__main__':
    main()



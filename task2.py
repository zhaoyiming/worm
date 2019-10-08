import requests
from urllib import request
from bs4 import BeautifulSoup
from xml import etree
import time
import csv
import re
index = 0
rownum = 1
with open("豆瓣Top250电影数据爬取.csv","w",newline="",encoding="utf_8_sig") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["排名","电影名称","评分","评价人数","简介","封面图片超链接"])

    while True:
        time.sleep(0.1)

        response = requests.get("https://movie.douban.com/top250?start="+str(index)+"&filter=")
        response.encoding = "utf-8"
        if index == 250:
            print("===========爬取完毕==========")
            break
        else:
            index += 25
            html = BeautifulSoup(response.text,features="html.parser")
            movie_list_soup = html.find('ol', attrs={'class': 'grid_view'})

            m_list = movie_list_soup.find_all('li')

            for movie_li in m_list:
                movie_name = movie_li.find('span', attrs={'class': 'title'})

                if not movie_name:
                    titlestr = "没有电影名称"
                else:
                    titlestr = movie_name.text

                detail2 = movie_li.find('div', attrs={'class': 'star'})
                movie_score = detail2.find('span', attrs={'class': 'rating_num'})
                if not movie_score:
                    srcstr = "没有电影分数"
                else:
                    srcstr = movie_score.text
                appraise_num_span = detail2.findAll('span')
                appraise_num = appraise_num_span[3]

                if not appraise_num:
                    appraise_num_str = "没有评价数"
                else:
                    appraise_num_str=re.findall(r"\d+\.?\d*", appraise_num.text)[0]


                detail3 = movie_li.find('div', attrs={'class': 'bd'})
                movie_intro = detail3.find('span', attrs={'class': 'inq'})
                if not movie_intro:
                    introstr = "没有电影简介"
                else:
                    introstr = movie_intro.text
                pic=movie_li.find("div",attrs={"class":"pic"})
                if pic:
                    pics=pic.find("img").attrs["src"]

                print([rownum, titlestr, srcstr, appraise_num_str, introstr,pics])
                csv_writer.writerow([rownum, titlestr, srcstr, appraise_num_str, introstr,pics])
                rownum += 1






# ming
#encoding="utf-8"
from bs4 import BeautifulSoup
import requests
import csv
import os
import re
import time

with open("百思不得姐爬虫数据.csv", "w",newline="",encoding="utf_8_sig") as f:
    colnum=1
    csv_w = csv.writer(f)
    csv_w.writerow(["编号", "昵称", "头像","时间","描述","主图","点赞数","差评数","分享数","评论数"])
    index = 1
    while True:
        if index==1:
            response = requests.get("http://www.budejie.com/")
        else:
            response = requests.get("http://www.budejie.com/" + str(index))
        # if response.status_code==404:
        #     break
        # with open("text.html", "wb") as f:
        #     f.write(response.content)
        response.encoding="utf-8"
        html = BeautifulSoup(response.text, features="html.parser")
        print("开始爬取page ",index)

        content = html.find("div", attrs={"class": "j-r-list"})

        divs=content.find_all("li")


        if divs:
            for div in divs:
                name=div.find("div",attrs={"class","u-txt"})
                if name is None:
                    continue
                else:
                    names = name.find("a").text
                    atimes = name.find("span").text

                img=div.find("div",attrs={"class","u-img"})
                if img is None:
                    continue
                else:
                    imgs = img.find("img").attrs["data-original"]

                maintext=div.find("div",attrs={"class","j-r-list-c-desc"})

                if maintext is None:
                    continue
                else:
                    maintexts = maintext.find("a").text

                mainpic = div.find("div", attrs={"class", "j-r-list-c-img"})
                if mainpic is None:
                    continue
                else:
                    mainpics = mainpic.find("img").attrs["src"]

                dianzannum = div.find("li", attrs={"class", "j-r-list-tool-l-up"})
                if dianzannum is None:
                    continue
                else:
                    dianzannums = dianzannum.find("span").text

                commentnum = div.find("div", attrs={"li", "j-r-list-tool-r j-r-list-tool-cc"})
                if commentnum is None:
                    continue
                else:
                    commentnums = commentnum.find("span").text

                cainum = div.find("li", attrs={"class", "j-r-list-tool-l-down"})
                if cainum is None:
                    continue
                else:
                    cainums = cainum.find("span").text

                sharenum = div.find("div", attrs={"class", "j-r-list-tool-ct-share-c"})
                if sharenum is None:
                    continue
                else:
                    sharenums = sharenum.find("span").text
                    sharenums=re.findall(r"\d+\.?\d*",sharenums)[0]
                print([colnum,names,imgs,atimes,maintexts,mainpics,dianzannums,cainums,sharenums,commentnums])
                csv_w.writerow([colnum,names,imgs,atimes,maintexts,mainpics,dianzannums,cainums,sharenums,commentnums])
                colnum+=1
            print("this is page "+str(index))
        index=index+1
        if index==10:
            break

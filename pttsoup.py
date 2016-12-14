import requests
from bs4 import BeautifulSoup
import time
import re
import sys

#to_day = time.strftime("%y%m%d-%H%M%S",time.localtime())
page = ""
count =50
group = ["Gossiping" , "Sex", "Movie"]
#看板list
url = ("https://www.ptt.cc")
# encode_re= ".encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)"
payload = {
"from":"/bbs/" + group[0] +"/index.html",
"yes":"yes"
}
#八卦版18禁post內容
rs = requests.session()
#設定session
res = rs.post("https://www.ptt.cc/ask/over18", data=payload)
#回傳payload post讓八卦版同意
res = (rs.get(url +"/bbs/" + group[0] + "/index" + page + ".html").text).encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
#爬八卦版標題,轉碼需先從requests轉
#res = res.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
soup = BeautifulSoup(res,"html.parser")
#爬蟲解析八卦版html
article_number = re.search(r'href="/bbs/(.+)/index(\d+).html">&lsaquo;', res).group(1,2)

def  article_print(soup):
    to_day = time.strftime("%y%m%d",time.localtime())
    ptt = []
    for write_html in soup.select(".r-ent"):
        date = write_html.select(".date")[0].text
        title = write_html.select(".title")[0].text.strip()
        # 去除title前後的\n .strip()
        nrec =write_html.select(".nrec")[0].text
        author = write_html.select(".author")[0].text
        link = write_html.find_all("a", href = True)
        if link != []:
            link = link[0]["href"]
        else:
            link = "無"
        ptt.append([date,nrec,title,author,link])
        #將八卦版的文章的日期標題作者連結存成list
    for a in ptt[::-1]:
        write_text = "時間:{0}\n[{1}]標題:{2}\n作者:{3}\n連結:{4}\n-----\n".format(a[0],a[1],a[2],a[3],a[4])
        with open(to_day  + ".txt","a") as file:
            file.write(write_text)
    #排序倒轉並寫入檔案

if   count != 0 :
        page = article_number[1]
        for a in range(int(count)):
            print(a)
            article_print(soup)
            print(page)
            res = (rs.get(url +"/bbs/" + group[0] + "/index" + str(page) + ".html").text).encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
            soup = BeautifulSoup(res,"html.parser")
            article_print(soup)
            print("write ok")
            page = int(page)  - 1



test1 = re.search(r'href="/bbs/(.+)/index(\d+).html">&lsaquo;', res).group(1,2)
#抓取上一頁的版名跟頁號
test2 = int(test1[1])
print(test1[0],test1[1])

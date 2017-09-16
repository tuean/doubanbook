# encoding: utf-8

import request
import urllib3
import time
import random
import bs4
import lxml
import pymysql
import db

# 数据库链接
connection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='tuean330',
    port=3306,
    charset='utf8',
    db='tuean'
)

cursor = connection.cursor()
print("数据库连接成功")


def insert(name, author, publish, press, ISBN, grade, tags, comments, bookId):
    sql = f'insert into douban_books values(0, \'{name}\' , \'{author}\' , \'{publish}\' , \'{press}\' , \'{ISBN}\' , \'{grade}\' , \'{tags}\' , \'{comments}\', \'{bookId}\')'
    print("新增sql" + str(sql))
    try:

        # data = (name, author, publish, press, ISBN, grade, tags, comments)
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("插入失败 回滚")
        print(e)
    else:
        print('成功插入', cursor.rowcount, '条数据')


headerPool = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
    {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

]


def increaseHeaderPool(header, url):
    header["Referer"] = url
    return header


def download(url, retrys=2, delayFlag=True):
    if delayFlag:
        sleepSec = random.randint(0, 10) * 0.5
        time.sleep(sleepSec)
        print("延时" + str(sleepSec) + "s")
    else:
        time.sleep(0.1)
        print("延时 0.1s")
    http = urllib3.PoolManager()
    try:
        # header = increaseHeaderPool(random.choice(headerPool), url)
        header = random.choice(headerPool)
        r = http.request('GET', url, headers=header)
        if 200 == r.status:
            html = str(r.data, encoding="utf-8")
        else:
            print(r.status)
            if retrys > 0 and r.status != 404:
                return download(url, retrys - 1, False)
            elif r.status == 403:
                html = "ip"
            else:
                html = None
    except Exception as e:
        print(e.reason)
    return html


def makeURL(bookId):
    return 'https://book.douban.com/subject/' + str(bookId) + '/?icn=index-editionrecommend'


def start(bookId):
    # url = 'https://book.douban.com/subject/' + str(bookId) + '/'
    toBeContinue = True
    count = 0
    finishCount = 0
    finishFlag = 100
    while toBeContinue:
        if count < 10:
            url = makeURL(bookId)
            result = download(url, 3, True)
            count += 1

            show = "成功!" if (result is not None) else "失败!";
            print("bookId: " + str(bookId) + " 返回结果:" + str(show))
            if result is None:
                bookId += 1
                finishCount += 1
                if finishCount > finishFlag:
                    print("爬取结束")
                    print("最后一个有效的bookId:" + str(bookId - 100))
                continue
            elif result == 'ip':
                print("bookId:" + str(bookId))
                return
            else:
                print("开始解析：\n" + url)
                toBeContinue = transfer(result, bookId)
                bookId += 1
        else:
            time.sleep(5)
            print("延时10s")
            count = 0
            continue


def transfer(result, bookId):
    soup = bs4.BeautifulSoup(result, 'lxml')

    name = str(soup.h1.text).replace("\n", "").replace("\r", "")
    print("书籍名称：" + str(name))

    author = str(soup.find(id='info').span.text).replace("\n", "").replace("\r", "").replace("作者:", "").replace(" ", "")
    print("作者：" + author)

    pls = soup.find_all(class_='pl')
    press = ''
    publish_year = ''
    page_number = ''
    price = ''
    ISBN = ''
    for pl in pls:
        if str(pl.text).__contains__("出版社"):
            press = str(pl.nextSibling).replace(" ", "")
            print("出版社：" + press)
        if str(pl.text).__contains__("出版年"):
            publish_year = str(pl.nextSibling).replace(" ", "")
            print("出版年：" + publish_year)
        if str(pl.text).__contains__("页数"):
            page_number = str(pl.nextSibling).replace(" ", "")
            print("页数：" + page_number)
        if str(pl.text).__contains__("价格"):
            price = str(pl.nextSibling).replace(" ", "")
            print("价格：" + price)
        if str(pl.text).__contains__("ISBN"):
            ISBN = str(pl.nextSibling).replace(" ", "")
            print("ISBN：" + ISBN)

    db_grade = str(soup.find("strong", class_="ll").text)
    print("豆瓣评分：" + db_grade)

    taglist = soup.find_all(class_="tag")
    tags = ""
    for tag in taglist:
        if tags != "":
            tags += "、"
        tags += str(tag.text)
    print("标签：" + tags)

    commentlist = soup.find_all(class_="comment-content")
    comments = ""
    for comment in commentlist:
        if comments != "":
            comments += "<>"
        comments += str(comment.text)
    print("评论：" + comments)

    if name is not None and str(name) != '':
        if author is None:
            author = ''
        if publish_year is None:
            publish_year = ''
        if press is None:
            press = ''
        if ISBN is None:
            ISBN = ''
        if db_grade is None:
            db_grade = ''
        if tags is None:
            tags = ''
        if comments is None:
            comments = ''
        author.replace("'", "\\'")
        press.replace("'", "\\'")
        insert(name, author, publish_year, press, ISBN, db_grade, tags, comments, bookId)

    return True


bookId = 10004102

start(bookId)
# print(soup.prettify())
# print(download(url), end='\r\n')
# print('111\n111')

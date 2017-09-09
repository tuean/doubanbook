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
    charset='utf8'
)

cursor = connection.cursor()
print("数据库连接成功")


def insert(name, author, publish, press, ISBN, grade, tags, comments):
    # sql = f"insert into douban_books (name, author, publish, press, ISBN, grade, tags, comments) values ({name} , {author} , {publish} , {press} , {ISBN} , {grade} , {tags} , {comments})"
    sql = f'insert into douban_books values(0, {name} , {author} , {publish} , {press} , {ISBN} , {grade} , {tags} , {comments})'
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
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]


def download(url, retrys=2):
    sleepSec = random.randint(0, 10) * 0.2
    time.sleep(sleepSec)
    print("延时" + str(sleepSec) + "s")
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', url, headers=random.choice(headerPool))
        if 200 == r.status:
            html = str(r.data, encoding="utf-8")
        else:
            print(r.status)
            if retrys > 0 and r.status != 404:
                return download(url, retrys - 1)
            else:
                html = None
    except Exception as e:
        print(e.reason)
    return html


def makeURL(bookId):
    return 'https://book.douban.com/subject/' + str(bookId) + '/'


def start(bookId):
    # url = 'https://book.douban.com/subject/' + str(bookId) + '/'
    url = makeURL(bookId)
    toBeContinue = True
    while toBeContinue:
        result = download(url)
        if result is None:
            bookId = bookId + 1
            continue
        else:
            print("开始解析：\n" + url)
            toBeContinue = transfer(result, bookId)
            bookId += 1
            url = makeURL(bookId)


def transfer(result, bookId):
    soup = bs4.BeautifulSoup(result, 'lxml')

    name = str(soup.h1.text).replace("\n", "").replace("\r", "")
    print("书籍名称：" + str(name))

    author = str(soup.find(id='info').span.text).replace("\n", "").replace("\r", "").replace("作者:", "").replace(" ", "")
    print("作者：" + author)

    pls = soup.find_all(class_='pl')
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

    insert(name, author, publish_year, press, ISBN, db_grade, tags, comments)

    return True


bookId = 1734833

start(bookId)
# print(soup.prettify())
# print(download(url), end='\r\n')
# print('111\n111')


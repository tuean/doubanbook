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


def insert(name, author, publish, press, ISBN, grade, tags, comments):
    # sql = f"insert into douban_books (name, author, publish, press, ISBN, grade, tags, comments) values ({name} , {author} , {publish} , {press} , {ISBN} , {grade} , {tags} , {comments})"
    sql = f'insert into douban_books values(0, \'{name}\' , \'{author}\' , \'{publish}\' , \'{press}\' , \'{ISBN}\' , \'{grade}\' , \'{tags}\' , \'{comments}\')'
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
    # {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    # {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    # {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    # {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    # {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    # {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
    {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
     # 'cookie':"bid=XmzY4p7iGuQ; ll=\"108296\"; gr_user_id=04df80b9-dce3-4e9b-9c61-10a32ad9d602; ct=y; viewed=\"12345678_27071333_1734833_1212131_1734846_1734844_1734840_1734837_27045311_26704405\"; "
     #          "ps=y; gr_cs1_189a509b-a11c-4613-8672-5990a18d7d45=user_id%3A0; dbcl2=\"127533512:iZMDiwOo614\"; ck=yIQE; __utmt=1; __utmt_douban=1; ap=1; push_noty_num=0; push_doumail_num=0; gr_session_"
     #          "id_22c937bbd8ebd703f2d8e9445f7dfd03=1a50d233-0568-481b-80ae-4897904608b5; gr_cs1_1a50d233-0568-481b-80ae-4897904608b5=user_id%3A1; __utma=30149280.727552494.1504699968.1505217669.1505305962"
     #          ".5; __utmb=30149280.32.10.1505305962; __utmc=30149280; __utmz=30149280.1504699968.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.12753; _vwo_uuid_v2=26C691A1DD1651E10BC90"
     #          "95866120870|3da6e84f1ab2f3f0f41b894d111969aa",
     # 'Host': 'erebor.douban.com'
     }

]

def increaseHeaderPool(header, url):
    header["Referer"] = url
    return header



def download(url, retrys=2, delayFlag=True):
    if delayFlag:
        sleepSec = random.randint(0, 5) * 1
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
            else:
                html = None
    except Exception as e:
        print(e.reason)
    return html


def makeURL(bookId):
    return 'https://book.douban.com/subject/' + str(bookId) + '/?icn=index-editionrecommend'


def start(bookId):
    # url = 'https://book.douban.com/subject/' + str(bookId) + '/'
    url = makeURL(bookId)
    toBeContinue = True
    count = 0
    while toBeContinue:
        if count < 6:
            result = download(url, 3, True)
            count += 1
        else:
            time.sleep(10)
            print("延时10s")
        show = "成功!" if (result is not None) else "失败!";
        print("bookId" + str(bookId) + " 返回结果:" + str(show))
        if result is None:
            bookId += 1
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


bookId = 10002000

start(bookId)
# print(soup.prettify())
# print(download(url), end='\r\n')
# print('111\n111')


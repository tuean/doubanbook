
import bs4
import db


def transfer(result, bookId):
    try:
        soup = bs4.BeautifulSoup(result, 'lxml')

        name = ''
        name = str(soup.h1.text).replace("\n", "").replace("\r", "")
        print("书籍名称：" + str(name))

        author = str(soup.find(id='info').span.text).replace("\n", "").replace("\r", "").replace("作者:", "").replace(" ",
                                                                                                                    "")
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
            db.insertBooksInfo(name, author, publish_year, press, ISBN, db_grade, tags, comments, bookId)
    except Exception as e:
        print(e)
        return False
    return True


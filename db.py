import pymysql

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


def getBookId():
    sql = f'select book_id from douban_id'
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        for id in result:
            book_id = id
        if book_id is None:
            return '10094411'
        else:
            return book_id
    except Exception as e:
        connection.rollback()
        print(e)
    else:
        print('查询成功')


def updateBookId(newBookId):
    sql = 'update douban_id set book_id = ' + str(newBookId)
    try:
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(e)
    else:
        print('成功更新', cursor.rowcount, '条数据')


def insertBooksInfo(name, author, publish, press, ISBN, grade, tags, comments, bookId):
    sql = f'insert into douban_books(name,author,publish,press,ISBN,grade,tags,comments,bookId) values( \'{name}\' , \'{author}\' , \'{publish}\' , \'{press}\' , \'{ISBN}\' , \'{grade}\' , \'{tags}\' , \'{comments}\', \'{bookId}\')'
    sql.strip('\00').encode()
    # print("新增sql" + str(sql))
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


import parser
import time

import db
import download
import util


def start(bookId):
    toBeContinue = True
    count = 0
    while toBeContinue:
        if count < 10:
            url = util.makeURL(bookId)
            bookId += 1
            db.updateBookId(bookId)
            count += 1
            result = download.download(url, 3, True)
            show = "成功!" if (result is not None) else "失败!"
            print("bookId: " + str(bookId) + " 返回结果:" + str(show))
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            if result is None:
                continue
            elif result == 'ip':
                print("bookId:" + str(bookId))
                toBeContinue = False
            else:
                print("开始解析：\n" + url)
                parser.transfer(result, bookId)
        else:
            print("延时5s")
            count = 0
            time.sleep(5)


bookId = db.getBookId()
print("任务开始，起始位置为：" + str(bookId))
start(bookId)

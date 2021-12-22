import poplib
import parser

emailaddress = 'zhongxiaotian'
# 注意使用开通POP，SMTP等的授权码
password = 'Tuean_330@11'
pop3_server = 'pop.gjzq.com.cn'

# 连接到POP3服务器:
server = poplib.POP3(host=pop3_server, port=110)
# 可以打开或关闭调试信息:
# server.set_debuglevel(1)
# POP3服务器的欢迎文字:
print(server.getwelcome())
# 身份认证:
server.user(emailaddress)
server.pass_(password)
# stat()返回邮件数量和占用空间:
messagesCount, messagesSize = server.stat()
print('messagesCount:', messagesCount)
print('messagesSize:', messagesSize)
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
print('------ resp ------')
print(resp)  # +OK 46 964346 响应的状态 邮件数量 邮件占用的空间大小
print('------ mails ------')
# print mails  # 所有邮件的编号及大小的编号list，['1 2211', '2 29908', ...]
print('------ octets ------')
print(octets)

# 获取最新一封邮件, 注意索引号从1开始:
length = len(mails)
print('mailLength:' + str(length))
for i in range(length):
    resp, lines, octets = server.retr(i + 1)
    msg_bytes = b'\n'.join(lines)
    # msg = parser.tuple2st(str(msg_bytes, encoding='utf-8'))
    msg = ""
    # print('第' + str(i) + '封邮件内容为：')
    print(str(msg))
    # 解析收件人
    try:
        headers = msg._headers
        for x in headers:
            if str(x).__contains__('From') and str(x).__contains__('yangzhanhong'):
                # 执行删除操作
                print(str(i))
    except Exception as e:
        print(str(e))

# 关闭连接:
server.quit()
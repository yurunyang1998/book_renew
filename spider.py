#coding=utf-8
import requests
import datetime
import smtplib
from email.mime.text import MIMEText



year =datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day

print(year,month,day)

user = '05166115'
pwd = '166115'


def getsession(user,pwd):
    url_get_session = 'https://api.xiyoumobile.com/xiyoulibv2/user/login/?username='+user+'&password='+pwd+'&callback=jsonp5'
    #data = {'user_name':user,'user_pwd':pwd}
    r  = requests.get(url_get_session)
    true =1
    false =0
    null =0
    r = r.text
    #print(r)
    r = r.split('(')[1].split(')')[0]

    #print(r)
    session_dic = dict(eval(r))

    #print(session_dic['Detail'])
    session = session_dic['Detail'].split()[0]

    return session    #获取到了session



def getbookinfo(session):
    true = 1
    false = 0
    null = 0
    url_get_book_information = 'https://api.xiyoumobile.com/xiyoulibv2/user/rent/?session='+session+'%20Path=/opac_two'
    r = requests.get(url_get_book_information)
    r = dict(eval(r.text))

    bookinfos =[]

    for i in r['Detail']:
        try:
            #print(i.keys())
            bookinfo={'Title':i['Title'],
                      'state':i['State'],
                      'Date':i['Date'],
                      'Library_id':i['Library_id'],
                      'canrenew':i['CanRenew'],
                      'department_id':i['Department_id'],
                      'department':i['Department']}
            #print(bookinfo)
            bookinfos.append(bookinfo)

        except Exception as e:
            print(e)
            #exit(0)

    return  bookinfos


def calculatetime(time):
    pass


def send_email(msg_address,sub,cont):

    """
    这是一个发送邮件的函数
    :param msg_address: 表示目的地址
    :param sub: 表示主题，如图书过期提醒，图书已续订
    :param cont: 表示内容，哪本书啥时候过期，是否续订
    :return:
    """

    msg_from='674860268@qq.com'                                 #发送方邮箱
    passwd='fiupxsfhxbxkbfdc'                                   #填入发送方邮箱的授权码
    msg_to=msg_address                                  #收件人邮箱

    subject="图书过期提醒"                                     #主题
    content="这是我使用python smtplib及email模块发送的邮件"      #正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)          #邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except Exception as e:
        print("发送失败")
    finally:
        s.quit()


def renewal(bookinfos):
    if(bookinfos is not None):
     for i in bookinfos:
        print(i)
        if(i['state']=='超过期限'):
            send_email()

        elif(calculatetime(i['Date'])): #如果快过期了
            if(i['canrenew']==0):  #如果不能续借了
                send_email()
            else:                 #自动续借
                pass


if __name__ == '__main__':
    # session = getsession(user,pwd)
    # bookinfos = getbookinfo(session)
    # renewal(bookinfos)
    send_email()
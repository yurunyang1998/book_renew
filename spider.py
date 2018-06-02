#coding=utf-8
import requests
import datetime
import smtplib
from email.mime.text import MIMEText








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
                      'department':i['Department'],
                      'barcode':i['Barcode']}
            #print(bookinfo)
            bookinfos.append(bookinfo)

        except Exception as e:
            print(e)
            #exit(0)

    return  bookinfos


def calculatetime(time):
    '''
    计算是不是快过期了
    :param time:
    :return:
    '''
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    now_day = datetime.datetime.now().day

    year=int(time[:4])
    month = int(time[4:6])
    day = int(time[6:8])

    if(year-now_year>=1):
        return False
    if(month-now_month>=1):
        return False
    if(day-now_day<=3):      #距离过期还有多久
        return True
    else:return False


def send_email(msg_address,send_info):

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
    content=send_info['has_renew']      #正文


    hasrenew = '这几本书已经续借:  '+'\n'
    for i in send_info['has_renew']:
        hasrenew = hasrenew+"           "+i+'\n'

    #if(send_info['overtime'] is not None):
    overtime = '这几本书已经过期：'+'\n'
    for i in send_info['overtime']:
        overtime=overtime+i+"           "+'\n'

    cannotrenew="这几本书已无法续借并将于一下日期过期 :"+'\n'
    for j,date in enumerate(send_info['overtime_date']) :
        cannotrenew = cannotrenew + "           "+send_info['cannotrenew'][j] +" : "+date[:4]+'-'+date[4:6]+'-'+date[6:8] +'\n'


    content ='======================\n'+hasrenew+"\n======================\n"+overtime+'\n======================\n'+cannotrenew +'\n======================\n'
    print(content)

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


def renewal(bookinfos,session):
    """
    这是自动续借的
    :param bookinfos:
    :param session:
    :return:
    """
    if(bookinfos is not None):
     send_info ={'overtime':[],'cannotrenew':[],'overtime_date':[],'has_renew':[]}
     for i in bookinfos:
        #print(i)
        if(i['state']=='超过期限'):
            send_info['overtime'].append(i['Title'])   #加入过期列表

        elif(calculatetime(i['Date'])): #如果快过期了
            if(i['canrenew']==0):  #如果不能续借了
                send_info['cannotrenew'].append(i['Title'])
                send_info['overtime_date'].append(i['Date'])
            else:                 #自动续借
                renewal_url = 'https://api.xiyoumobile.com/xiyoulibv2/user/renew?session='+session+'%20Path=/opac_two&barcode='+str(i['barcode'])+'&department_id='+str(i['department_id'])+'&library_id='+str(i['Library_id'])
                send_info['has_renew'].append(i['Title'])
                #print(renewal_url)



    #print(send_info)

    return send_info

if __name__ == '__main__':
    user = '05166115'
    pwd = '166115'
    email = "674860268@qq.com"
    session = getsession(user,pwd)
    bookinfos = getbookinfo(session)
    send_info=renewal(bookinfos,session)
    print(send_info)

    if(len(send_info['overtime_date'])>0 or (len(send_info['has_renew'])>0)  or len(send_info['cannotrenew'])>0):
         send_email(email,send_info)


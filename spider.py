import requests
import  json
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


    for i in r['Detail']:
        try:
            print(i.keys())
            bookinfo={'Title':i['Title'],
                      'state':i['State'],
                      'Date':i['Date'],
                      'Library_id':i['Library_id'],
                      'canrenew':i['CanRenew'],
                      'department_id':i['Department_id'],
                      'department':i['Department']}
            print(bookinfo)
            
        except Exception as e:
            print(e)
            #exit(0)

if __name__ == '__main__':
    session = getsession(user,pwd)
    getbookinfo(session)

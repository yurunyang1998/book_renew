import requests
import  json
user = '05166115'
pwd = '166115'
url_get_session = 'https://api.xiyoumobile.com/xiyoulibv2/user/login/?username='+user+'&password='+pwd+'&callback=jsonp5'
#data = {'user_name':user,'user_pwd':pwd}
r  = requests.get(url_get_session)
true =1
r = r.text
#print(r)
r = r.split('(')[1].split(')')[0]

#print(r)
session_dic = dict(eval(r))

#print(session_dic['Detail'])
session = session_dic['Detail'].split(";")[0]

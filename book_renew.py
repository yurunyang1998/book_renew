from flask import Flask,render_template
from flask import  request,redirect,url_for

from  spider import getsession
from   link_databs import  insert,delet_user
app = Flask(__name__,static_url_path='')


@app.route('/',methods=['GET'])
def index():
     return app.send_static_file(filename='yuRunYang/html/sign.html')



@app.route('/subscribe',methods=['POST'])
def get_message():
    user = request.form['name']
    pwd = request.form['password']
    email = request.form['email']

    session = getsession(user,pwd)
    if(session=='ACCOUNT_ERROR'):
        return "</p> 账号或密码错误"   # 账号或密码错误

    result = insert(user,pwd,email)
    if(result==1):
        return "</p>订阅成功"
    else:
        return '</p>该用户已经存在'

@app.route('/login',methods=['GET'])
def login():
    #return  "srtasdf"
    return app.send_static_file(filename='yuRunYang/html/login.html')



@app.route('/login',methods=['POST'])
def delete_user():
    user = request.form['user']
    pwd = request.form['pwd']
    result = delet_user(user,pwd)
    return result

@app.route('/sign.html',methods=['GET'])
def index2():
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)


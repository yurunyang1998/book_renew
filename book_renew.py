from flask import Flask
from flask import  request
app = Flask(__name__,static_url_path='')


@app.route('/',methods=['GET'])
def index():
    return app.send_static_file(filename='yuRunYang/html/sign.html')

@app.route('/book_renew',methods=['GET','POST'])
def get_message():
    user = request.form(['name'])
    pwd = request.form(['password'])
    email = request.form(['email'])

    print(user)
    return user

if __name__ == '__main__':
    app.run()

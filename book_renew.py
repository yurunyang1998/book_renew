from flask import Flask

app = Flask(__name__,static_url_path='')


@app.route('/',methods=['GET','POST'])
def hello_world():
    return app.send_static_file(filename='html/sign.html')


if __name__ == '__main__':
    app.run()

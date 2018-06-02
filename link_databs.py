import pymysql as MySQLdb

def insert(user,pwd,email):
    """
    这个是用来添加用户数据的，表的名字叫 subscribers
    :param user:
    :param pwd:
    :param email:
    :return:
    """
    try:
        conn = MySQLdb.connect('localhost','root','admin','book_renew')
        cursor = conn.cursor()
        whther_exist_sql = "select * from subscribers where user=%s "%(user)
        cursor.execute(whther_exist_sql)
        if(cursor.fetchone()):
            print("这个用户已经存在")

        else:

            inser_sql = " insert into subscribers(user,pwd,email) VALUE ('%s','%s','%s')" %(user,pwd,email)
            cursor.execute(inser_sql)
            conn.commit()
    except:
        conn.rollback()

    finally:
        conn.close()




def select(id):

    db = MySQLdb.connect('localhost','root','admin','book_renew')
    cursor = db.cursor()
    select_sql="select * FROM subscribers where id=%s" %id
    cursor.execute(select_sql)
    data =cursor.fetchall()
    print(data)
    return data




def delet_user(user,pwd):

    try:
        conn = MySQLdb.connect('localhost','root','admin','book_renew')
        cursor = conn.cursor()
        delete_sql = "delete  from subscribers where user=%s and pwd=%s"%(user,pwd)
        cursor.execute(delete_sql)
        conn.commit()
        print("你的账号已经成功删除")
    except:
        print("删除失败")
        conn.rollback()

    finally:
        conn.close()
def get_count():
    """
    这个是获取数据库中所有的条数的
    :return:
    """
    db = MySQLdb.connect('localhost','root','admin','book_renew')
    cursor = db.cursor()
    count_sql = "select count(*) from subscribers"
    cursor.execute(count_sql)
    count = cursor.fetchone()
    #print(count[0])
    return  count[0]




if __name__ == '__main__':

    # for i in range(10):
    #     insert(i,'166115','674860268@qq.com')
    # i = get_count()
    # for  a in range(i):
    #     select(a)
    delet_user('1','166115')
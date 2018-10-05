import pymysql.cursors
import hashlib

#This is a temporary script to create a default user.  

def mon_con():
    connection = pymysql.connect(host = 'localhost',
                                 user = 'test',
                                 password = 'test',
                                 db = 'monitoring',
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)
    return connection

"""def authenticate(password):
    encrypt_password=hashlib.sha224(password.encode()).hexdigest()"""


def create_user(username, password):
    encrypt_password=hashlib.sha224(password.encode()).hexdigest()
    print(username)
    print(encrypt_password)
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = r"INSERT INTO users (username, password, admin) SELECT '" + username + "', '" + encrypt_password + "', 1 FROM DUAL WHERE NOT EXISTS (SELECT * from users WHERE username='" + username + "') LIMIT 1"
            print(sql)
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()




create_user("admin", "test")



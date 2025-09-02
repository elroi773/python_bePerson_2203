import pymysql

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",   
        password="Mysql4344!",   
        database="bePerson",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

#coding=utf-8
import MySQLdb

def open_db(dbname, username, password):
    conn = MySQLdb.connect(
        host = 'localhost',
        port = 3306,
        user = username,
        passwd = password,
        db = dbname,
        )
    return conn

def close_db(connect):
    connect.commit()
    connect.close()

def write_data(connect, table, fields, values):
    cur = connect.cursor()
    sqlstring = "insert into " + table + " (" + fields + ") values (" + values + ")"
    print(sqlstring)
    cur.execute(sqlstring)

    
    



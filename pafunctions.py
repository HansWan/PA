#coding=utf-8
import MySQLdb
import os, shutil

#define functions used by all modules, e.g., open database, write data into tables, etc.

def open_db(dbname, username, password):
    connect = MySQLdb.connect(
        host = 'localhost',
        port = 3306,
        user = username,
        passwd = password,
        db = dbname,
        )
    return connect

def close_db(connect):
    connect.commit()
    connect.close()

def write_data_to_dbtable(connect, table, fields, values, returnlastid=False):
    cur = connect.cursor()
    sqlstring = "insert into " + table + " " + fields + " values " + values
#    print(sqlstring)
#    try:
    cur.execute(sqlstring)
#    except:
#    pass
    if returnlastid:
        sqlstring = "select last_insert_id()"
        cur.execute(sqlstring)
        last_insert_id = cur.fetchone()[0]
        return last_insert_id
    cur.close()
    
def load_data_from_file(connect, table, fields, sourcefilepath, sourcefilename):
    f = open(sourcefilepath+sourcefilename, 'r')

    for line in f.readlines():
        s = line.rstrip('\n').split(':')
        if len(s) == 2:
            values = str(tuple(s))
            write_data_to_dbtable(connect, table, fields, values, False)
    
def list_files_to_dbtable(connect, rootfolder, parent_table, child_table):
#list all files in a designated folder (including sub folders) and load them into a table
    for root, dirs, files in os.walk(rootfolder):
        for file in files:
            table = parent_table
            fields = '(path, filename)'
            values = "('" + MySQLdb.escape_string(root) + "', " + "'" + file + "')"
            last_insert_id = write_data_to_dbtable(connect, table, fields, values, True)

            #load into table filestatus
            table = child_table
            status = ''
            fields = '(idrawpasswordfiles, status)'
            values = "(" + str(last_insert_id) + ", " + "'" + status + "')"
            write_data_to_dbtable(connect, table, fields, values, False)

def check_if_record_exists(connect, table, fields, values)
    cur = connect.cursor()
    sqlstring = "select * from " + table + " " + fields + " values " + values
#    print(sqlstring)
#    try:
    cur.execute(sqlstring)

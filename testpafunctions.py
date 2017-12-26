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

    sqlstring = "insert into " + table + " (" + fields2string(fields) + ") values (" + fields2percents(fields) + ")"
    try:
        cur.execute(sqlstring, values)
    except:
        pass
    if returnlastid:
        sqlstring = "select last_insert_id()"
        cur.execute(sqlstring)
        last_insert_id = cur.fetchone()[0]
        return last_insert_id
    cur.close()
    
def load_data_from_file(connect, table, fields, sourcefilepath, sourcefilename):
    f = open(sourcefilepath+sourcefilename, 'r')
    returnlastid = False   #no need to return last_insert_id
    for line in f.readlines():
        values = line.rstrip('\n').split(':')
        if len(values) == 2:
            write_data_to_dbtable(connect, table, fields, values, returnlastid)
    
def list_files_to_dbtable(connect, rootfolder, parent_table, child_table):
    #list all files in a designated folder (including sub folders) and load them into a table
    for root, dirs, files in os.walk(rootfolder):
        for file in files:
            table = parent_table
            fields = ['path', 'filename']
            #some roots not include "\", need to add one
            if root[len(root)-1] <> '\\':
                root = root + "\\"
            values = [root, file]
            if not check_if_record_exists(connect, table, fields, values): #if no record exists then add a new one
                returnlastid = True   #need to return last_insert_id in order to add records in child table
                last_insert_id = write_data_to_dbtable(connect, table, fields, values, returnlastid)

                #load into table filestatus
                table = child_table
                status = ''
                fields = ['idrawpasswordfiles', 'status']
                values = [last_insert_id, status]
                if not check_if_record_exists(connect, table, fields, values):
                    returnlastid = False #no need to return last_insert_id
                    write_data_to_dbtable(connect, table, fields, values, returnlastid)

def fields2string(fields):
    fields2string = ''
    for field in fields:
        fields2string = fields2string + field + ','
    fields2string = fields2string[:-1]
    return fields2string

def fields2percents(fields):
    #construct %s, %s string according to fields quantity
    fields2percents = ''
    for field in fields:
        fields2percents = fields2percents + '%s,'
    fields2percents = fields2percents[:-1]
    return fields2percents

def fields2paras(fields):
    #construct 'parameter1=%s, parameter2=%s' string according to fields quantity
    fields2paras = ''
    for field in fields:
        fields2paras = fields2paras + field + '=%s and '
    fields2paras = fields2paras[:-5]
    return fields2paras

def check_if_record_exists(connect, table, fields, values):
    cur = connect.cursor()
    sqlstring = "select * from " + table + " where " + fields2paras(fields)
#    try:
    return cur.execute(sqlstring, values)

def get_id(connect, table, fields, values):
    cur = connect.cursor()
    sqlstring = "select id from " + table + " where " + fields2paras(fields)
    print(sqlstring)
    cur.execute(sqlstring, values)
#    try:
    id = cur.fetchone()[0]
    return id

def update_a_record(connect, table, parafields, paravalues, updatedfields, updatedvalues):
    if not check_if_record_exists(connect, table, parafields, paravalues):    #no record exists then add one
        fields = parafields + updatedfields
        values = paravalues + updatedvalues
        returnlastid = False
        write_data_to_dbtable(connect, table, fields, values, returnlastid)
    else:
        cur = connect.cursor()
        sqlstring = "update " + table + " set " + fields2paras(updatedfields) + " where " + fields2paras(parafields)
        cur.execute(sqlstring, updatedvalues + paravalues)

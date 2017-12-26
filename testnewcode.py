#coding=utf-8
import MySQLdb
import os, shutil
import copy
from pafunctions import open_db, write_data_to_dbtable, close_db, fields2string, fields2percents, fields2paras, load_data_from_file, list_files_to_dbtable, check_if_record_exists, get_id, update_a_record

connect = open_db('PA', 'root', 'nopassword')
cur = connect.cursor()

#truncate table
sqlstring = "truncate table rawpasswordfiles"
cur.execute(sqlstring)
connect.commit()
sqlstring = "truncate table filestatus"
cur.execute(sqlstring)
connect.commit()
sqlstring = "truncate table passwords"
cur.execute(sqlstring)
connect.commit()

os._exit()


#scan folder and load files into a table
#rootfolder = 'C:\\Users\\admin\\Documents\\Files\\ITL\\Python\\python_work\\PA\\data\\'
rootfolder = 'C:\\temp\\s\\'
parent_table = 'rawpasswordfiles'
child_table = 'filestatus'
list_files_to_dbtable(connect, rootfolder, parent_table, child_table)

#scan table rawpasswordfiles and load data into table passwords
#get data from a table
parent_table = 'rawpasswordfiles'
child_table = 'filestatus'

sqlstring = "select id, path, filename from " + parent_table + " where id in (select idrawpasswordfiles from " + child_table + " where status <> 'loaded')"
cur.execute(sqlstring)
filelist = cur.fetchall()

#load data into table passwords
for id, sourcefilepath, sourcefilename in filelist:
    #check if this file is already uploaded
    table = 'filestatus'
    fields = ['idrawpasswordfiles', 'status']
    values = [id, 'loaded']
    if not check_if_record_exists(connect, table, fields, values):    #not uploaded
        table = 'passwords'
        fields = ['account', 'password']
        print("uploading " + sourcefilepath + sourcefilename + "...")
        load_data_from_file(connect, table, fields, sourcefilepath, sourcefilename)
        #update table filestatus
        table = 'filestatus'
        parafields = ['idrawpasswordfiles']
        paravalues = [id]
        updatedfields = ['status']
        updatedvalues = ['loaded']
        update_a_record(connect, table, parafields, paravalues, updatedfields, updatedvalues)

close_db(connect)

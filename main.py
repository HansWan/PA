#coding=utf-8
import MySQLdb
import os, shutil
import copy

from pafunctions import open_db, write_data_to_dbtable, close_db, load_data_from_file, list_files_to_dbtable


connect = open_db('PA', 'root', 'nopassword')


#scan folder and load files into a table
rootfolder = 'C:\\Users\\admin\\Documents\\Files\\ITL\\Python\\python_work\\PA\\data\\'
parent_table = 'rawpasswordfiles'
child_table = 'filestatus'
list_files_to_dbtable(connect, rootfolder, parent_table, child_table)

#load data into table passwords
table = 'passwords'
fields = ['account', 'password']
sourcefilepath = "C:\\Users\\admin\\Documents\\Files\\ITL\\Python\\python_work\\PA\\data\\"
sourcefilename = "o"
#load_data_from_file(connect, table, fields, sourcefilepath, sourcefilename)


connect.commit()

os._exit()


#mark a file as "loaded"
table = 'filestatus'
status = 'loaded'
parafields = ['idrawpasswordfiles', 'status']
paravalues = [1, 'loaded']
updatedfields = ['status']
updatedvalues = ['loaded']
#values = "(" + str(last_insert_id) + ", " + "'" + status + "')"
get_data_from_dbtable(connect, table, fields, values)



close_db(connect)

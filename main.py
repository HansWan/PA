from pafunctions import open_db, write_data, close_db

conn = open_db('PA', 'root', 'nopassword')

table = 'filestatus'
fields = 'id, idrawpasswordfile, status'
status = 'analyzed'
for i in range(31, 40):
#    values = str(i) + ',' + str(i) + ", 'analyzed'"
    values = str(i) + ', ' + str(i) + ', ' + "'" + status + "'"
    write_data(conn, table, fields, values)

#cur.close()
close_db(conn)

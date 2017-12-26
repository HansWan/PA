#used only for codes backup

if False:
    table = 'filestatus'
    fields = 'id, idrawpasswordfile, status'
    status = 'analyzed'
    for i in range(41, 50):
    #    values = str(i) + ',' + str(i) + ", 'analyzed'"
        values = str(i) + ', ' + str(i) + ', ' + "'" + status + "'"
        write_data_to_dbtable(conn, table, fields, values)

        #if i>1000:
            #break
        #i += 1

            #print values

values = "('" + MySQLdb.escape_string(sourcefilepath) + "', " + "'" + sourcefilename + "')"
last_insert_id = write_data_to_dbtable(connect, table, fields, values, True)

#        print(os.path.join(root, file))


def write_data_to_dbtable(connect, table, fields, values, returnlastid=False):
    cur = connect.cursor()
    
    v1 = 'abc@de.com'
    v2 = 'abcde'
    fields2string(fields)
    sqlstring = "insert into filestatus (idrawpasswordfiles, status) values (2, '')"
#    sqlstring = "insert into passwords (account, password) values ('abc@de.com', 'abcde')"
#    sqlstring = "insert into password (account, password) values (%s, %s) "%(v1, v2)
#    sqlstring = "insert into " + table + " (" + fields2string(fields) + ") values (%s, %s) " + "('abc@de.com', 'abcde')"
#    sqlstring = "insert into " + table + " (" + fields2string(fields) + ") values " + values
#    sqlstring = "insert into " + table + " " + fields + " values " + values
    print(sqlstring)
    print(values)
#    try:
    cur.execute(sqlstring)
    connect.commit
    print('done')
#    cur.execute(sqlstring, values)
#    except:
#    pass
    if returnlastid:
        sqlstring = "select last_insert_id()"
        cur.execute(sqlstring)
        last_insert_id = cur.fetchone()[0]
        return last_insert_id
    cur.close()


truncate table 

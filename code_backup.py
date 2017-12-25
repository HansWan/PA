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

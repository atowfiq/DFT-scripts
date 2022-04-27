
db='fedbfull'
#cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database=db)#
cnx = mysql.connector.connect(user='root', password='inshALLAH%6',host='127.0.0.1',database=db)#

cursor = cnx.cursor()


def getdbidCompoundIdPair():
    query = "SELECT _database_code_ICSD,id from compound where source='icsd'"
    cursor.execute(query)
    l = cursor.fetchall()
    dbids, compoundids = [item[0] for item in l], [item[1] for item in l]
    result = {}
    for i in range(0, len(dbids)):
        if dbids[i] == None:
            print dbids[i]
        result[int(dbids[i])] = compoundids[i]
    return result

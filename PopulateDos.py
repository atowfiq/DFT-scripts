import glob
import os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists
import copy
import matplotlib.pyplot as plt
import mysql.connector
from random import shuffle
import numpy as np
import json
import sys

db = 'fedbfull'
#cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database=db)
cnx = mysql.connector.connect(user='root', password='inshALLAH%6',host='127.0.0.1',database='fedbfull')
cursor = cnx.cursor()



def column(matrix, i):
    return [row[i] for row in matrix]

def getListToSting(list):

    return "'" +  ', '.join(str(x) for x in list) + "'"




def readDos(file):

    dosTotalVal =[]
    headers =[]
    content = ''
    with open(file) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i = 0

    while (i < len(content)):
        dosVal = []

        data = content[i].split('  ')


        if i>=2:
            for d in data:
                if(len(d.strip())==0):
                    continue
                if i==2:
                    if d !="#":
                        headers.append(d)
                else:
                    dosVal.append(d)
            if(i>2):
                temp=dosVal[:]
                dosTotalVal.append(temp)

        i = i + 1
    return dosTotalVal,[x.strip() for x in headers if x.strip()]
        #band.append(content[i].split())

        #bands.append(band)
    #return bands


def insertTotalDataDos(compoundDos,dbid):
  #  compoundDosJson="'"+json.dumps(compoundDos)+"'"
    energyList = column(compoundDos, 0)
    energy =  "'" +getListToSting(energyList)+"'"
    totaldosList = column(compoundDos, 1)
    totaldos = "'" +getListToSting(totaldosList)+"'"

 #  s = "0,"+energy+"," + totaldos + "," +compoundDosJson+ ",'" + ','.join(dosColHeaders) + "'," +  str(id) + ",'icsd'"
   # for i in range(0,len(dosColHeaders)):
     #   print dosColHeaders[i]

    q= energy+ ","+ min(energyList)+ ","+ max(energyList)+ ","+energyList[0] + ","+energyList[len(energyList)-1]+","+totaldos+","
    q=q + min(totaldosList)+ ","+ max(totaldosList)+ ","+totaldosList[0] + ","+totaldosList[len(totaldosList)-1]
    query = "INSERT INTO dostotaldata(`compoundid`,`energy`,`energymin`,`energymax`,`energyfirst`,`energylast`,`totaldos`,`totaldosmin`,`totaldosmax`,`totaldosfirst`,`totaldoslast`)  values(%s,%s)" % (str(dbid),q)
    cursor.execute(query)


def createCols(colName,tableName):
    cols=''
    colsCommaSeparated =''
    try:
        query ="ALTER TABLE "+tableName+" ADD `"+colName+"` mediumtext;"
        cursor.execute(query)
        cols=cols+"`"+colName+"`"
        colsCommaSeparated = colsCommaSeparated+colName
    except Exception,e:
        print e
    try:
        query = "ALTER TABLE "+tableName+" ADD `" + colName + "min` double;"
        cursor.execute(query)
        cols = cols +",`"+colName+"min`"
        colsCommaSeparated = colsCommaSeparated+","+colName+"min"
    except Exception, e:
        print e
    try:
        query = "ALTER TABLE "+tableName+" ADD `" + colName + "max` double;"
        cursor.execute(query)
        cols = cols +",`"+ colName + "max`"
        colsCommaSeparated = colsCommaSeparated + "," + colName + "max"
    except Exception, e:
        print e
    try:
        query = "ALTER TABLE "+tableName+" ADD `" + colName + "first` double;"
        cursor.execute(query)
        cols = cols + ",`"+colName + "first`"
        colsCommaSeparated = colsCommaSeparated + "," + colName + "first"
    except Exception, e:
        print e
    try:
        query = "ALTER TABLE " + tableName + " ADD `" + colName + "last` double;"
        cursor.execute(query)
        cols = cols + ",`"+colName + "last`"
        colsCommaSeparated = colsCommaSeparated + "," + colName + "last"
    except Exception, e:
        print e
    return cols,colsCommaSeparated

def getColspartialdosData(orb):
    cols=''
    orbcols =''
    if orb not in partialdosdatatCols:
        orbcols,commaseparatedCols=createCols(orb,tbl)
        cols= cols+orbcols
        partialdosdatatCols.extend(commaseparatedCols.split(','))
    return "`"+orb+"`,"+"`"+orb+"min`,"+"`"+orb+"max`,"+"`"+orb+"first`,"+"`"+orb+"last`"




def column(matrix, i):
    return [row[i] for row in matrix]
def getListToSting(list):
    return ', '.join(str(x) for x in list)


def getValspartialdosData(compoundDos,j):
    v = column(compoundDos, j)
    return "'" + getListToSting(v) + "'," + str(min(v)) + "," + str(max(v)) + "," + str(v[0]) + "," + str(v[len(v) - 1])

def insertPartialDos(compoundDos,dosColHeaders,id,structureElem):
    for i in range(0,len(structureElem)):
        print structureElem[i]
        queryCols = ''
        queryVals = ''
        orbital = ''

        for j in range(2,len(dosColHeaders)):
            elemOrb = dosColHeaders[j].split(':')
            if(elemOrb[0]==str(i+1)):
                orb =elemOrb[1].strip()
                if(len(orbital)>0):
                    orbital =orbital + ','
                orbital = orbital+orb
                if(len(queryCols)>0):
                    queryCols =queryCols+','
                queryCols = queryCols + getColspartialdosData(orb)
                if (len(queryVals) > 0):
                    queryVals = queryVals+ ','
                queryVals = queryVals+ getValspartialdosData(compoundDos,j)

        query = "insert into partialdosdata(compoundid, elementindex,element, orbitals,%s) values(%s,%s,'%s','%s',%s)" %(queryCols,id,i+1,structureElem[i],orbital,queryVals)
        cursor.execute(query)

def readStructure(structureFile):
    content = ''
    with open(structureFile) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i = 0
    elements={}
    index=0
    while (i < len(content)):
        if 'Z:' in content[i]:

            e=content[i].split()[0]
            elements[index]=e
            index = index + 1
        i = i + 1
    return elements




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


def getDosColNames(dbName,tableName):
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + dbName + "' AND TABLE_NAME = '" + tableName + "'"
    cursor.execute(query)
    l = list(cursor.fetchall())

    return ([item[0] for item in l])


def getAllGeneratedIds(tableName):
    query = "SELECT distinct compoundid from %s"% tableName
    cursor.execute(query)
    return [item[0] for item in cursor.fetchall()]

def deleteDataForCompound(id):
    print "delete compound data if exists"
    query = "delete from dostotaldata where compoundid=%s" % id

    cursor.execute(query)
    query = "delete from partialdosdata where compoundid=%s" % id
    cursor.execute(query)
    print 'deleted'



#elements = ["Ac","Am","Ce","Np","Pa","Pu","Th","U","La"]
#dosDirectory ="C:\Users\AdnanIbne\PycharmProjects\DFTDataGenerator\DFTDataGenerator\Data\dos"
#dosDirectory = "/home/khair/Research/Wien2k/Data/dos/"
dosDirectory= "/home/hafiz/Research/IMS_Database/success_done"
elements =[f for f in os.listdir(dosDirectory)]#["U"]

tbl = 'partialdosdata'
alreadyGenerated = getAllGeneratedIds('dostotaldata')
dbidCompoundIdPair = getdbidCompoundIdPair()
partialdosdatatCols=getDosColNames(db,tbl)



for e in elements:
    path  =join(dosDirectory,e)# #join(join(dosDirectory ,e),"2")#
    files =[f for f in os.listdir(path)]

    count = 0

    for idx, f in enumerate(files):
        try:

            if dbidCompoundIdPair[int(f)] in alreadyGenerated:
                print f + ' Generated'
                continue

            print f
            if count%100==0:
                print count
            count = count+1
            destinationDir = join(path, f)
            os.chdir(destinationDir)

            dosColHeaders=[]
            compoundDos = []

            structureElem= readStructure(f+".struct")
            print structureElem
            dFiles = glob.glob(f+".dos*ev")
            #dFiles.sort()

            for dosIndex in range(len(dFiles)):
                dosfile =f+".dos"+str(dosIndex+1)+"ev"

            #bsfile = join(destinationDir,f+".spaghetti_ene")
            #bsfile ="/media/adnan/ExtraDrive1/Repository/DFTDataGenerator/DFTDataGenerator/Data/bs/9310.spaghetti_ene"
                dosTotalVal,header = readDos(dosfile)
                index=0
                for d in dosTotalVal:
                    if len(compoundDos)==len(dosTotalVal):
                        compoundDos[index]=compoundDos[index]+d[1:]
                    else:
                        compoundDos.append(d)
                    index = index+1

                if len(dosColHeaders)==0:
                    dosColHeaders= header
                else:

                    dosColHeaders = dosColHeaders + header[1:]

            fid =str(dbidCompoundIdPair[int(f)])
            deleteDataForCompound(fid)
            insertTotalDataDos(compoundDos,fid)

            insertPartialDos(compoundDos,dosColHeaders,fid,structureElem)
         #   print getData()
            cnx.commit()
        except Exception, e:
            cnx.rollback()
            print 'Error ' + f
            print  e
            print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
print "Completed"
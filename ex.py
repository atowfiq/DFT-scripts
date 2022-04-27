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


cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='fedbfull')#
cursor = cnx.cursor()


def getAllGeneratedIds():
    query = "SELECT _database_code_ICSD,id from compound where source='icsd'"
    cursor.execute(query)
    l =cursor.fetchall()
    dbids,compoundids= [item[0] for item in l],[item[1] for item in l]
    result={}
    for i in range(0,len(dbids)):
        if dbids[i]==None:
            print dbids[i]
        result[int(dbids[i])]=compoundids[i]
    return result

#print 29086 in getAllGeneratedIds()


def addCols(tableName,colName):
    try:
        query ="ALTER TABLE "+tableName+" ADD `"+colName+"` mediumtext;"
        cursor.execute(query)
    except Exception,e:
        print e
    try:
        query = "ALTER TABLE "+tableName+" ADD `" + colName + "min` double;"
        cursor.execute(query)
    except Exception, e:
        print e
    try:
        query = "ALTER TABLE "+tableName+" ADD `" + colName + "max` double;"
        cursor.execute(query)
    except Exception, e:
        print e
    try:
        query = "ALTER TABLE "+tableName+" ADD `" + colName + "first` double;"
        cursor.execute(query)
    except Exception, e:
        print e
    try:
        query = "ALTER TABLE "+tableName+" ADD " + colName + "last double;"
        cursor.execute(query)
    except Exception, e:
        print e




def getBandstructureColNames(dbName,tableName):
    query="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '"+dbName+"' AND TABLE_NAME = '"+tableName+"'"
    cursor.execute(query)
    l= list(cursor.fetchall())

    return ([item[0] for item in l])



cols= getBandstructureColNames('fedbfull','partialbandstructure')

cnames= 'tot,s,p,px,py,pz,d,dz2,d(x2-y2),dxy,dxz,dyz,f,A2,x(T1),y(T1),z(T1),ksi(T2),eta(T2),zeta(T2),0,1'
for cn in cnames.split(','):
    if cn not in cols:
        addCols('partialbandstructure',cn)

print




import os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists
from shutil import copyfile, move, copytree


def updateQtlFile(f):
    move(f + '.inq', f + '.inq_backup')

    content = ''
    with open(f + '.inq_backup') as fileToRead:
        content = fileToRead.readlines()

    with open(f + ".inq", "a") as intFile:
        index = 0
        while index < len(content):
            if 'qsplit' in content[index]:
                contentSplitted = content[index].split()
                contentSplitted[1]='2'
                content[index]="   " + "  ".join(contentSplitted[:len(contentSplitted) - 1]) + "       " + contentSplitted[len(contentSplitted) - 1]
                content[index]=content[index]+"\n"
            intFile.write(content[index])
            print content[index]
            index = index + 1

            #updateQtlFile("C:\\Users\\AdnanIbne\\PycharmProjects\\DFTDataGenerator\\DFTDataGenerator\\Data\\bandstructure\\U\\2\\29086\\29086")
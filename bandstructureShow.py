
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
                              database='feicsddb')
#cnx = mysql.connector.connect(user='root', password='inshALLAH%6',
 #                             host='127.0.0.1',
  #                            database='fedbfull')
cursor = cnx.cursor()



def column(matrix, i):
    return [row[i] for row in matrix]

def getListToSting(list):
    return ', '.join(str(x) for x in list)

def getData():
    query = "select * from bandstructure_k"
    cursor.execute(query)
    return list(cursor)

def insertDataBandstructure_k(band,id):
        kx ="'"+getListToSting(column(band,0))+"'"
        ky ="'"+getListToSting(column(band,1))+"'"
        kz ="'"+getListToSting(column(band,2))+"'"
        X ="'"+getListToSting(column(band,3))+"'"
        s ="0,"+kx+","+ky+","+kz+","+X+","+str(id)+",'icsd'"
        query ="INSERT INTO bandstructure_k(compoundid,kx,ky,kz,X,database_id,source) VALUES (%s);" % s

        cursor.execute(query)


def insertDataBandstructure_all(band, id,index):
    energy= "'" + getListToSting(column(band, 4)) + "'"

    s = "0," + str(index) + "," + energy+ "," + str(id) + ",'icsd'"

    query = "INSERT INTO bandstructure_all(compoundid,`index`,energy,database_id,source) VALUES (%s);" % s
    cursor.execute(query)

def readBandstructure(file):

    bands = []
    band=[]
    content = ''
    with open(file) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i = 0

    while (i < len(content)):
        if 'bandindex' in content[i] :

            bands.append(copy.copy(band))
            band =[]
            i = i + 1;

        band.append(content[i].split())
        i = i + 1;
    bands.append(band)
    return bands

elements = ["Ac","Am","Ce","Np","Pa","Pu","Th","U","La"]
bsDirectory = "/home/khair/Research/Wien2k/Data/bandstructure/"

for e in elements:
    path  = join(join(bsDirectory,e),"2")

    files = []#[f for f in os.listdir(path)]

    count = 0

    for idx, f in enumerate(files):
        try:
            if count==1:
                print count
            count = count+1
            destinationDir = join(path, f)
          #  bsfile = join(destinationDir,f+".spaghetti_ene")
            bsfile ="/media/adnan/ExtraDrive1/Repository/DFTDataGenerator/DFTDataGenerator/Data/bs/9310.spaghetti_ene"
            bands = readBandstructure(bsfile)
            X= column(bands[len(bands)-1],3)
            #for band in bands[1:]:
             #   Y= column(band ,4)
            #   plt.plot(X, Y)
            insertDataBandstructure_k(bands[1],f)

            for i in range(1,len(bands)):
                insertDataBandstructure_all(bands[i],f,i)

            print getData()
            cnx.commit()
        except Exception, e:
            print f
            print  e
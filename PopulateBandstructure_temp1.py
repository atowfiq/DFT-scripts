
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


#1. Case.inq open- iatom value make qsplit -2 to 2
#2. x lapw1 -band
#3. x qtl -band

#JATOM  1  MULT= 1  ISPLIT= 2  tot,s,p,px,py,pz,d,dz2,d(x2-y2),dxy,dxz,dyz,f,A2,x(T1),y(T1),z(T1),ksi(T2),eta(T2),zeta(T2),
# JATOM  2  MULT= 2  ISPLIT= 2  tot,s,p,px,py,pz,


cnx = mysql.connector.connect(user='root', password='inshALLAH%6',
                              host='127.0.0.1',
                              database='fedbfull')#
cursor = cnx.cursor()


def getAllGeneratedIds():
    query = "SELECT distinct database_id from bandstructure_temp1 where source='icsd'"
    cursor.execute(query)
    return [item[0] for item in cursor.fetchall()]


def insertDataBandstructure(band, index,id):
    energy = "'" + getListToSting(band) + "'"

    s = "id,"+ str(index)+ ","  +   energy+ "," + str(id) + ",'icsd'"
    query = "INSERT INTO bandstructure_temp1(compoundid,`index`,energy,database_id,`source`) select %s from compound_temp1 where _database_code_ICSD=%s and source ='icsd';" % (s,id)
    cursor.execute(query)


def insertDataPartialBandstructure(partialBand,index,id,orbitals,structureElements):
    for i in range(len(partialBand)):
        p = partialBand[i]
        values=''
        if(i<len(partialBand)):
            orbital=''
            if(i==len(partialBand)-1):
                orbital='tot'
            else:
                orbital = orbitals[i]
            splittedOrbitals = orbital.split(',')
            cols =''
            for orb in splittedOrbitals:
                 if len(orb)>0:
                     cols=cols+'`'+orb+'`,'
            for j in range(len(p[0])):
                values = values+"'"+getListToSting(column(p,j))+"',"
            #splittedOrbital = orbital.split(',')
        values= "id,"+ str(index)+ ","  + str(i)+ ",'"+structureElements[i]+"'," +values+ id + ",'icsd'"
        query = "INSERT INTO partialbandstructure_temp1(compoundid,`index`,elementindex,element,"+cols+"database_id,`source`) select %s from compound_temp1 where _database_code_ICSD=%s and source ='icsd';" % (values,id)
        cursor.execute(query)



def column(matrix, i):
    return [row[i] for row in matrix]
def getListToSting(list):
    return ', '.join(str(x) for x in list)



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

def readKFile(kfile):
    content = ''
    with open(kfile) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i = 0
    kpoints = {}
    while (i < len(content)):
        p = content[i].split()[0]
        if p.replace(".","").replace("-","").isdigit()==False:
            kpoints[i+1]=p
        i = i + 1
    return kpoints

def updateFermiEnergy(fe,id):
    query = "Update compound_temp1 set fermienergy= %s where _database_code_ICSD=%s and source='icsd'" % (str(fe),id)
    cursor.execute(query)

def deleteDataForCompound(id):
    print "delete compound data if exists"
    query = "delete from bandstructure_temp1 where compoundid=%s and source='icsd'" % id

    cursor.execute(query)
    query = "delete from partialbandstructure_temp1 where compoundid=%s and source='icsd'" % id
    cursor.execute(query)
    print 'deleted'


def readqtlFile(qtlFile,id,structureElements,compoundId):
    deleteDataForCompound(compoundId)
    fermyEnergy = 0
    structureElements[len(structureElements)]="IS"
    content = ''
    orbitals=[]
    isplits =[]
    with open(qtlFile) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i = 0

    index=0
    kpoints = {}
    bands =[]
    band=[]
    isStart = False

    partialBand=[]
    pb=[]
    while (i < len(content)):
        splitted = content[i].split()
        if 'FERMI ENERGY' in content[i]:
            fermyEnergy=float(splitted[len(splitted)-1])
            updateFermiEnergy(fermyEnergy*13.6,id);
        elif 'ISPLIT' in content[i]:
            orbitals.append(splitted[len(splitted)-1])
        elif 'BAND' in content[i]:
            if len(band)>0:
                index=index+1

                insertDataBandstructure(band,index,id)
                insertDataPartialBandstructure(partialBand,index,id,orbitals,structureElements)

                #  bands.append(copy.copy(band))
                partialBand=[]
                band=[]
            isStart=True
        elif isStart:

            j=0
            splittedBandValue = content[i].split()
            energyInEv = (float(splittedBandValue[0]) - fermyEnergy) * 13.6

            band.append(energyInEv)

            while j< len(orbitals)+1:
                if  j<len(partialBand):
                    pb = partialBand[j]
                else:
                    pb=[]
                    partialBand.append(pb)
                pb.append(content[i].split()[2:])
                j = j + 1
                i = i + 1
            i=i-1
        i = i + 1
    print "Inserted " + id
#    print partialBand[2]
#    print orbitals[0]
def getdbidCompoundIdPair():
    query = "SELECT _database_code_ICSD,id from compound_temp1 where source='icsd'"
    cursor.execute(query)
    l = cursor.fetchall()
    dbids, compoundids = [item[0] for item in l], [item[1] for item in l]
    result = {}
    for i in range(0, len(dbids)):
        if dbids[i] == None:
            print dbids[i]
        result[int(dbids[i])] = compoundids[i]
    return result


elements =["Pu"]
#elements = ["Ac","Am","Ce","Np","Pa","Pu","Th","U","La"]
bsDirectory = "/home/khair/Research/Wien2k/Data/bandstructure/"
#bsDirectory = "C:\\Users\\AdnanIbne\\PycharmProjects\\DFTDataGenerator\\DFTDataGenerator\\Data\\bandstructure"
alreadyGenerated = getAllGeneratedIds()
dbidCompoundIdPair = getdbidCompoundIdPair()
for e in elements:
    path  = join(join(bsDirectory,e),"2")

    files = [f for f in os.listdir(path)]

    count = 0

    for idx, f in enumerate(files):
        try:
            if count==1:
                print count
            count = count+1
            destinationDir = join(path, f)

            if int(f) in alreadyGenerated:
                print f + ' Generated'
                continue

            if not exists(join(destinationDir, f + ".spaghetti_ps")):
                print f + " bandstructure not exists"
                continue

            #bsfile = join(destinationDir,f+".spaghetti_ene")
            # bsfile = join(destinationDir,f+".spaghetti_ene")
            structureFile= join(destinationDir,f+".struct")
            # bsfile ="/media/adnan/ExtraDrive1/Repository/DFTDataGenerator/DFTDataGenerator/Data/bs/9310.spaghetti_ene"
       #     print structureFile
            structureElements = readStructure(structureFile)
    #        kpointFile = join(destinationDir,f+".klist_band")
     #       kPointsIndexes= readKFile(kpointFile)

            qtlFile= join(destinationDir, f + ".qtl")
            bandstructure = readqtlFile(qtlFile,f,structureElements,str(dbidCompoundIdPair[int(f)]))
         #   print structureElements
          #  print kPointsIndexes
            #X= column(bands[len(bands)-1],3)
            #for band in bands[1:]:
             #   Y= column(band ,4)
            #   plt.plot(X, Y)

            cnx.commit()
        except Exception, e:
            print "Error " + f
            print  e
print "Completed"
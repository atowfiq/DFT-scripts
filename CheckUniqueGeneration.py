import os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists
from os import listdir, makedirs

def getChemicalFormulaName(cifFile):
    content = ''
    with open(cifFile) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i = 0
    formulaName = ''
    while (i < len(content)):
        if '_chemical_formula_sum' in content[i]:
            formulaName = content[i].replace('_chemical_formula_sum','')
            formulaName = formulaName.strip()
            break;
            # print content[i]
        i = i + 1;
    if len(formulaName) == 0:
        formulaName = ""
    return formulaName
dict = {}
elements = ["Ac","Am","Ce","Np","Pa","Pu","Th","U","La"]
successDirectory = "/home/khair/Research/Wien2k/Data/success/"


count = 0
for e in elements:
    path  = join(join(successDirectory,e),"2")
    print path

    files = [f for f in os.listdir(path)]

    totalDone = 0
    for idx, f in enumerate(files):
        try:
            sourceDir = join(path, f)
            filePath = join(sourceDir, f + ".cif")
            formulaName = getChemicalFormulaName(filePath)
            if 	dict.has_key(formulaName):
                dict[formulaName]= dict[formulaName]+1
            else:
                dict[formulaName]=1
        except Exception, e:
            print e

with open("generatedFile.txt", "a") as logFile:
    sum = 0
    for k in dict.keys():
        sum = sum + dict[k]
        print k + " " + str(dict[k])

        logFile.write("%s\n" % (k + " " + str(dict[k])))
print sum
print len(dict)

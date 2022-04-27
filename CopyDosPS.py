import os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists
from os import listdir, makedirs
def MakeDir(dir):
    if not exists(dir):
        os.makedirs(dir)
        return True
    else:
        return False


elements = ["Ac","Am","Ce","Np","Pa","Pu","Th","U","La"]
bsDirectory = "/home/khair/Research/Wien2k/Data/dos/"

source = "icsd"
outputDirectory = "/home/khair/Research/Wien2k/Data/View/dos"
outputDirectory  = join(outputDirectory,source)

MakeDir(outputDirectory)

count = 0
for e in elements:
    path  = join(join(bsDirectory,e),"2")
    print path

    files = [f for f in os.listdir(path)]


    totalDone = 0
    for idx, f in enumerate(files):
        try:
            sourceDir = join(path, f)
            os.chdir(sourceDir)
            filePath =join(sourceDir, f + "1.ps")
            print filePath
            if exists(filePath):
                pasteDir = join(outputDirectory, f + "1.ps")
                print pasteDir
                copyfile(filePath,pasteDir)
                count = count + 1
                continue
            else:
                print "Not Exists" + join(sourceDir, f + ".spaghetti_ps")
        except Exception, e:
            with open("pnglog.txt", "a") as logFile:
                logFile.write("Error: File: %s Message: %s\n" % (f, e))
print count
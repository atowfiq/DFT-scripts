
import os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists


elements = ["Ac","Am","Ce","Np","Pa","Pu","Th","U","La"]
count = 0

for e in elements:
    print "element: " + e
    dosOutPutDirectory ="/home/khair/Research/Wien2k/Data/dos/"+e+"/2"#"/home/khair/Research/Wien2k/Data/dos/test"#"/home/khair/Research/Wien2k/Data/dos/U/2"# "C:/Users/AdnanIbne/Desktop/Python"#

    pbsDostoPsScript = "/home/khair/Research/Wien2k/pbs/pbsdostops/pbs"

    files = [f for f in os.listdir(dosOutPutDirectory )]

    totalDone =0
    for idx, f in enumerate(files):
        try:

            destinationDir = join(dosOutPutDirectory, f)
            os.chdir(destinationDir)
            print destinationDir
            count =count+1
            if(count%1==0):
                break;



            #copy the pbs script for dos -- generating dos command is twritten in pbs.csh
            copyfile(pbsDostoPsScript+str(idx%7)+".csh", join(destinationDir, "pbsdostops.csh"))
            k = subprocess.Popen(["qsub", "pbsdostops.csh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = k.communicate()
            print "dos  generated"

        except Exception, e:
            with open("dospslog.txt", "a") as logFile:
                logFile.write("Error: File: %s Message: %s\n" % (f, e.message))
print count
# *****Requirements to generated dos*****
# copy of successful generated scf
#
# Fermi Energy from scf File
# *****Steps***
#  1. Generate the case.qtl file->
#                                   x lapw1 -p
#                                   x lapw2 -qtl -p
# 2. Generate case.int file-> e.g Number of Atoms in the struct file =2 then
#                             -> configure_int_lapw  -b  total  1  tot s,p,d,f  2  tot,s,p,d,f end
# Grep the Fermi Energy from case.scf file
# Update case.int file with Fermi Energy Emin =FermiEnergy-1, Emax =FermiEnergy+.5
#Run 'x tetra' to generate dos
#This code is run 2 times to generate dos -> Fist run to generate case.qtl ->2nd run to generate dos
#
#
#
# 0.3786179695

#
#




import os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists
from shutil import copyfile, move, copytree
from os import makedirs



def getFermiEnergy():
    k = subprocess.Popen(['grep', '-nr', ':FER', '.', '--exclude=*.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = k.communicate()
    splitted = out.split('\n')
    newSplit = splitted[len(splitted) - 2].split()
    return float(newSplit[len(newSplit) - 1])



def getSpaceGroup(cifFile):
    symmetry = ''
    content = ''
    with open(cifFile) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i = 0
    spaceGroup = ''
    while (i < len(content)):
        if '_symmetry_Int_Tables_number' in content[i]:
            spaceGroup = content[i].split()[1].strip().lower()
            break;
            # print content[i]
        i = i + 1;
    if len(spaceGroup) == 0:
        spaceGroup = "0"
    return int(spaceGroup)

def updateQtlFile(f):
    move(f + '.inq', f + '.inq_backup')

    content = ''
    with open(f + '.inq_backup') as fileToRead:
        content = fileToRead.readlines()

    with open(f + ".inq", "a") as inqFile:
        index = 0
        while index < len(content):
            if 'qsplit' in content[index]:
                contentSplitted = content[index].split()
                contentSplitted[1]='2'
                content[index]="   " + "  ".join(contentSplitted[:len(contentSplitted) - 1]) + "       " + contentSplitted[len(contentSplitted) - 1]
                content[index]=content[index]+"\n"
            inqFile.write(content[index])
            index = index + 1

def MakeDir(dir):
    if not exists(dir):
        makedirs(dir)
        return True
    else:
        return False


#elements = ["Ac","Am","Ce","Np","Pa","Pu","Th","U","La"]
successDirectory= "/home/khair/Research/Wien2k/Data/success"
bsDirectory = "/home/khair/Research/Wien2k/Data/bandstructure/"
elements = ["Ce"]#[f for f in os.listdir(bsDirectory)]
pbsBSScript = "/home/khair/Research/Wien2k/pbs/pbsbs/pbsdis/pbs"
kpathDirectory = "/home/khair/Research/Wien2k/Data/K_path/kpath_by_spacegroup"
sources= "/home/khair/Research/Wien2k/Data/sources"
for e in elements:
    successFileElementPath = join(join(successDirectory,e),"2")
    successFiles = [f for f in os.listdir(successFileElementPath)]
    path = join(join(bsDirectory, e), "2")

    for sidx, sf in enumerate(successFiles):
        if not os.path.exists(os.path.join(path,sf)):
            copytree(os.path.join(successFileElementPath, sf),os.path.join(path,sf))

    files = [f for f in os.listdir(path)]

    count = 1
    totalDone = 0
    for idx, f in enumerate(files):
        try:
            if count%200==0:
                print count
                break;
            destinationDir = join(path, f)
            print destinationDir
            os.chdir(destinationDir)
            if exists(join(destinationDir, f + ".spaghetti_ps")):
                print f + " bandstructure exists"
                continue
            # copy the pbs script for bandstructure -- generating dos command is written in pbs.csh
            count = count + 1
            copyfile(pbsBSScript + str(idx % 8) + ".csh", join(destinationDir, "pbs.csh"))
            #make case.insp with Fermi Energy

            with open(join(sources, 'case.insp')) as fileToRead:
                content = fileToRead.readlines()
            fermiEnergy = getFermiEnergy()
            with open(f+".insp", "a") as inspFile:
                index= 0
                while index<len(content):
                    if '# Fermi switch,  Fermi-level (in Ry units)' in content[index]:
                        content[index] = content[index].replace("0.xxxx",str(fermiEnergy))
                    inspFile.write(content[index])
                    index = index +1
            print "New insp file generated"

            spaceGroup =getSpaceGroup(join(destinationDir,f+".cif"))
            print "spaceGroup "+str(spaceGroup)
            updateQtlFile(f)
            copyfile(join(kpathDirectory,str(spaceGroup)+".klist_band"), join(destinationDir, f+".klist_band"))
            k = subprocess.Popen(["qsub", "pbs.csh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = k.communicate()
            print "bandstructure  generated"
            count = count+1

        except Exception, e:
            with open("bslog.txt", "a") as logFile:
                logFile.write("Error: File: %s Message: %s\n" % (f, e))
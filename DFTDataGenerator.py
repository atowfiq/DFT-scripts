import os
from os.path import isfile, join, basename, exists
from os import listdir, makedirs
from shutil import copyfile, move
import subprocess
import traceback

def MakeDir(dir):
    if not exists(dir):
        makedirs(dir)
        return True
    else:
        return False



sourcePath = "/home/khair/fesd/icsdcif/ICSDCifs/U/2/"  # "/home/khair/fesd/rsptinp"

cifFiles = [f for f in os.listdir(sourcePath) if f.endswith('.cif')]
outPutDirectory = "/home/khair/Research/Wien2k/Data/output/U/2"
pbsScript = "/home/khair/Research/Wien2k/pbs/pbs/pbs"
MakeDir(outPutDirectory)
count = 0
folderName = ""
print len(cifFiles)
for idx,f in enumerate(cifFiles):
    try:
        folderName = basename(f).replace(".cif", "").replace("EntryWithCollCode", "")
        destinationDir = join(outPutDirectory, folderName)


        if exists(destinationDir):
            print "exists"
            continue
        if count == 200:
            count = 0
            break;
        count = count + 1

        MakeDir(destinationDir)
        #  sourceRspt  = join(sourcePath,f.replace(basename(f) ,"rspt"))
        #  sourceRspt  = join(sourcePath,f.replace(basename(f) ,"rspt"))

        filePath = join(sourcePath, f)
        newFileName = folderName + ".cif"
        print newFileName
        if not exists(join(destinationDir, newFileName)):
            copyfile(filePath, join(destinationDir, newFileName))

        copyfile(pbsScript+str(idx%5)+".csh", join(destinationDir, "pbs.csh"))

        os.chdir(destinationDir)
        # print destinationDir
        # mpiRunCmd = "'mpirun -machinefile ~/torque/"+proc+" -np 16 ~/bin/rspt_bin/rspt'"
        # print mpiRunCmd
        k = subprocess.Popen(["cif2struct", newFileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()

        k = subprocess.Popen(["init_lapw", "-b"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()

        copyfile(join(destinationDir, folderName + ".struct"), join(destinationDir, folderName + "_backup.struct"))
        if exists(join(destinationDir, folderName + ".struct_sgroup")):
            copyfile(join(destinationDir, folderName + ".struct_sgroup"), join(destinationDir, folderName + ".struct"))

        k = subprocess.Popen(["init_lapw", "-b"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()

        k = subprocess.Popen(['grep', '-nr', 'ERROR', '.', '--exclude=*.py'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = k.communicate()
        if len(out.split('\n')) > 1:
            k = subprocess.Popen(["reduce_rmt_lapw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = k.communicate()

            k = subprocess.Popen(["init_lapw", "-b"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = k.communicate()

            k = subprocess.Popen(['grep', '-nr', 'ERROR', '.', '--exclude=*.py'], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = k.communicate()

            with open("log.txt", "w") as text_file:
                text_file.write("Error: File: %s Grep error List: %s" % (f, out))

        k = subprocess.Popen(["qsub", "pbs.csh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()

        print f
        print out
        print err
    except Exception,e:
        with open("log.txt", "w") as text_file:
            text_file.write("Error: File: %s Message: %s" % (f, e.message,))
        traceback.print_exc()

print "Completed"
import os
from os.path import isfile, join, basename, exists
from shutil import copy, move
from os import listdir, makedirs



elements= set(["Na", "K", "Rb", "Cs", "Mg", "Ca", "Sr", "Ba","Sc", "Y", "Ti", "Zr", "Hf", "V", "Nb" ,"Ta"])
destinationDir = "D:\COD"
path="E:\cod-cifs-mysql\cif"
for root, subdirs, files in os.walk(path):

    for filename in files:
        if (filename.endswith('cif')):
            filepath= os.path.join(root, filename)
            with open(filepath,'r') as fileToRead:
                content = fileToRead.readlines()

            content = [x.strip() for x in content]
            for i in range(0,len(content)):
                if("_chemical_formula_sum" in content[i]):
                        splitted =content[i].split("'")
                        if(len(splitted)>1):
                            formula= splitted[1]
                            splittedFormula =splitted[1].split()
                            numberOfElements= len(splittedFormula)
                            for el in splittedFormula:
                                for n in range(10):
                                    el =  el.replace(str(n),'')
                                if(el in elements):
                                    dir=join(destinationDir,join(el,str(numberOfElements)))
                                    if not exists(dir):
                                        makedirs(dir)
                                    copy(filepath,dir)


print "Completed"
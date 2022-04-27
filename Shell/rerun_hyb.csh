#!/bin/csh -f

set whichatom = "Th"

set homedir = "$PWD"
set targetpath = "/home/hafiz/Research/Hybrid/element"
set incompath = "/home/hafiz/Research/Hybrid/incomplete"

ls $incompath/$whichatom > out.txt
set file='out.txt'

foreach case ("`cat $file`")

	mv $incompath/$whichatom/$case  $targetpath/$whichatom/$case
	cd $targetpath/$whichatom/$case

	qsub -v case=$case,whichatom=$whichatom pbs_dm.csh

	cd $homedir
end	
rm out.txt


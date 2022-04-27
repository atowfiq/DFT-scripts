#!/bin/csh -f

set cifpath = "/home/hafiz/hh_research/icsdcif/ICSDCifs"
set targetpath = "/home/hafiz/hh_research/ternaries/sgroup_success"
set failpath = "/home/hafiz/hh_research/ternaries/fail"
set homedir = "$PWD"

ls $cifpath > atomslist.txt

foreach atom ("`cat atomslist.txt`")
	ls $cifpath/$atom/3/ > $atom.txt
	mkdir $targetpath/$atom
	mkdir $failpath/$atom

	foreach case ("`cat $atom.txt`")
		set name = `echo "$case" | sed -e 's/EntryWithCollCode\(\d*\)/\1/'`
       		set casename = `echo $name | sed 's/.cif/ /g'`
        	echo $casename
		mkdir $targetpath/$atom/$casename
		cp $cifpath/$atom/3/$case $targetpath/$atom/$casename
		cd $targetpath/$atom/$casename
		cp $case $name
		cif2struct $name
		x sgroup 
		if ( -s $casename.struct_sgroup ) then
			cp $casename.struct $casename.struct.old
			mv $casename.struct_sgroup $casename.struct
		else
			mv $targetpath/$atom/$casename  $failpath/$atom
		endif		
	end
	cd $homedir
	rm $atom.txt
end
rm atomslist.txt


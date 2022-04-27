#!/bin/csh -f

set filepath = "/home/hafiz/hh_research/ternaries/sgroup_success"
set homedir = "$PWD"

ls $filepath > atoms.txt

#foreach whichatom ("`cat atoms.txt`")
set whichatom = "U"
	
	ls $filepath/$whichatom > out.txt
	set file='out.txt'
	foreach case ("`cat $file`")
	##set case = 416243

	##################### Read case.struct ####################################################################
	
	set structfile = $filepath/$whichatom/$case/$case.struct
	set ucell=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $1}')`
	set natom=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $3}')`
	set spaceG=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $4}')`
	set spaceGname=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $5}')`
	set atoms=`( grep 'Z:' $structfile | awk '{print $1}')`
	set zvar1=`( grep 'Z:' $structfile | awk '{print $8}')`
	set zvar2=`( grep 'Z:' $structfile | awk '{print $9}')`		
	set mval=`( grep 'MULT' $structfile | awk '{print $2}')`
	set isplit=`( grep 'MULT' $structfile | awk '{print $4}')`
	set var=`( grep 'MULT' $structfile | awk '{print $1}')`

	set ii=1
	set lattice=0;
	foreach line ("`cat $structfile`")
		if ($ii == 4) then
			set argv = ( $line )
			set ai = $1
			set bi = $2
			set ci = $3
			set alpha = $4
			set beta = $5
			set gamma = $6
		endif
		@ ii++
	end

	set i=1
	set totatom=0
	set mult = ' '
	while ($i<$#mval + 1)
        	if ($mval[$i] !~ [0-9] ) then
                	set mval0 = `echo "$var[$i]" | sed -e 's/MULT=\(\d*\)/\1/'`
                	@ totatom += $mval0
                	set mult = ($mult $mval0)
        	else
                	@ totatom += $mval[$i]
                	set mult = ($mult $mval[$i])
        	endif
        	@ i++
	end
	
	if ($#zvar1 == $natom) then
        	set i=1
		set j=1
        	set zval = ' '
        	while ($i<$natom + 1)
                	if ($zvar1[$i] == Z:) then
                        	set zval = ($zval $zvar2[$j])
				@ j = $j + 1
                	else
				set zval = ($zval $zvar1[$i])
                	endif
               		@ i++
        	end
	
#	endif

##echo $natom $zvar1 $zvar2

	set atomicnum = ' '
	set elemem = ' '
	set multiplicity = ' '
	set ato1 = ' '
	set ato2 = ' '	
	set ato3 = ' '
	set ele1 = ' '
	set ele2 = ' '
	set ele3 = ' '
	set ml1 = ' '
	set ml2 = ' '	
	set ml3 = ' '

	set i=1
        while ($i<$natom + 1)

                        set ii=1
                        @ a = 0
                        while ($ii < 100)
                                if ($ii"." =~ $zval[$i]) then
                                        @ a = $ii
                                endif
                                @ ii++
                        end

			if (($a > 56 && $a < 72) || $a > 88) then
                                set ato1 = ($ato1 $a)
				set ele1 = ($ele1 $atoms[$i])
				set ml1 = ($ml1 $mult[$i])
                        else if (($a > 20 && $a < 31) || ($a > 38 && $a < 49) || ($a > 71 && $a < 81) || ($a > 103 && $a < 113) ) then
				set ato2 = ($ato2 $a)
                                set ele2 = ($ele2 $atoms[$i])
				set ml2 = ($ml2 $mult[$i])
			else
				set ato3 = ($ato3 $a)
                                set ele3 = ($ele3 $atoms[$i])
				set ml3 = ($ml3 $mult[$i])
			endif
                @ i++
        end
		set atomicnum = ($atomicnum $ato1 $ato2 $ato3)
		set elemem = ($elemem $ele1 $ele2 $ele3)
		set multiplicity = ($ml1 $ml2 $ml3)
 
##		echo "Z= [$atomicnum] Atoms= [$elemem]"
		echo $alpha
##		echo $case
#		if ($spaceG == 139 && $totatom == 5) then	
#			echo "$whichatom  ICSD#$case  $ucell  $spaceGname($spaceG)  lattice= [$ai $bi $ci] angles= [$alpha $beta $gamma] #atoms= $natom  Total_atoms= $totatom Z= [$atomicnum] Atoms= [$elemem] Multi= [$multiplicity]"
#			echo "$whichatom $case $ai $bi $ci $atomicnum $elemem $multiplicity" >> data2.txt
#			echo "$whichatom $ucell $case $natom $totatom $ai $bi $ci $alpha $beta $gamma $atomicnum $elemem $multiplicity" >> data_ternaries.txt
#		endif	
	endif
	end
#end

#########################################################################################################################
#########################################################################################################################


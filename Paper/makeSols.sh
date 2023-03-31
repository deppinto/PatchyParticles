#!/bin/bash

START=1
END=136
SPECIES=2
COLORS=3
TOT=$(( COLORS * ( COLORS + 1 ) / 2 + COLORS * SPECIES * 5 ))
TOTS=$(( COLORS * ( COLORS + 1 ) / 2 + COLORS * SPECIES * 5 / 2 ))
TOTA=$(( COLORS * SPECIES * 5 / 2 ))
TOTC=$(( COLORS * ( COLORS + 1 ) / 2 ))

echo "$TOT" "$TOTS" "$TOTA" "$TOTC"

python3 generate_cls_file.snubcube.py snubdode "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 0 > dump

for ((i=$START; i<=$END; i++))
do
	minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubdode.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_dode' > dump
	INI=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_dode | sed -n 1','1'p' | awk '{print $1}'`
	if [ $INI = "UNSAT" ];then
		echo "No solution for snub dodecahedron!"
		exit 0
	fi
	

	rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
	python3 generate_cls_file.snubcube.py snubcube "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 0 > dump
	sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >> '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
	line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
	stringarray=($line)
	save=${stringarray[3]}
	result=$((save + TOT))
	var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
	sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
	minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube' > dump
	RES=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube | sed -n 1','1'p' | awk '{print $1}'`

	rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.icosahedron.py icosahedron "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 0 > dump
        sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >> '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_ico' > dump
        RESS=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_ico | sed -n 1','1'p' | awk '{print $1}'`

        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.snubcube.py snubcube1 "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 0 > dump
        sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >> '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube1' > dump
        RETS=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube1 | sed -n 1','1'p' | awk '{print $1}'`

        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.snubcube.py snubcube2 "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 0 > dump
        sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >> '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube2' > dump
        RETTS=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube2 | sed -n 1','1'p' | awk '{print $1}'`



        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.snubcube.py snubcube "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 1 > dump
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^'$TOTC'//;t;s/'$TOTC'/\n'$TOTC'/;D' | sed 's/ //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
        #line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^[^'$TOTC']*'$TOTC' //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
        arr=($line)
        save=${arr[0]}
        result0=$((save + TOTA ))
        save=${arr[1]}
        result1=$((save + TOTA ))
        save=${arr[2]}
        result2=$((save + TOTA ))
        save=${arr[3]}
        result3=$((save + TOTA ))
        save=${arr[4]}
        result4=$((save + TOTA ))
        line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        line2=$(sed -n '2p' files/solution_dode | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/')
        var="${line2} ${line}"
        echo $var | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >>  '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube' > dump
        RESSS=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube | sed -n 1','1'p' | awk '{print $1}'`

        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.snubcube.py snubcube "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 1 > dump
        line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
	arr=($line)
        save=${arr[0]}
        result0=$((save - TOTA ))
        save=${arr[1]}
        result1=$((save - TOTA ))
        save=${arr[2]}
        result2=$((save - TOTA ))
        save=${arr[3]}
        result3=$((save - TOTA ))
        save=${arr[4]}
        result4=$((save - TOTA ))
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^'$TOTC'//;t;s/'$TOTC'/\n'$TOTC'/;D' | sed 's/ //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        #line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^[^'$TOTC']*'$TOTC' //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        line2=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //')
	line3=$(sed -n '2p' files/solution_dode | sed 's/'$TOTC'.*//' | sed 's/$/'$TOTC'/')
        var="${line3} ${line} ${line2}"
        echo $var | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >>  '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube' > dump
        RESSSS=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube | sed -n 1','1'p' | awk '{print $1}'`


        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.snubcube.py snubcube1 "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 1 > dump
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^'$TOTC'//;t;s/'$TOTC'/\n'$TOTC'/;D' | sed 's/ //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
	#line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^[^'$TOTC']*'$TOTC' //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
        arr=($line)
        save=${arr[0]}
        result0=$((save + TOTA))
        save=${arr[1]}
        result1=$((save + TOTA))
        save=${arr[2]}
        result2=$((save + TOTA))
        save=${arr[3]}
        result3=$((save + TOTA))
        save=${arr[4]}
        result4=$((save + TOTA))
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        line2=$(sed -n '2p' files/solution_dode | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/')
        var="${line2} ${line}"
        echo $var | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >>  '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube1' > dump
        RRES=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube1 | sed -n 1','1'p' | awk '{print $1}'`

        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.snubcube.py snubcube1 "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 1 > dump
        line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
        arr=($line)
        save=${arr[0]}
        result0=$((save - TOTA))
        save=${arr[1]}
        result1=$((save - TOTA))
        save=${arr[2]}
        result2=$((save - TOTA))
        save=${arr[3]}
        result3=$((save - TOTA))
        save=${arr[4]}
        result4=$((save - TOTA))
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^'$TOTC'//;t;s/'$TOTC'/\n'$TOTC'/;D' | sed 's/ //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
	#line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^[^'$TOTC']*'$TOTC' //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        line2=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //')
	line3=$(sed -n '2p' files/solution_dode | sed 's/'$TOTC'.*//' | sed 's/$/'$TOTC'/')
        var="${line3} ${line} ${line2}"
        echo $var | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >>  '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube1.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube1' > dump
        RRRES=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube1 | sed -n 1','1'p' | awk '{print $1}'`


        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.snubcube.py snubcube2 "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 1 > dump
	#line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^[^'$TOTC']*'$TOTC' //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^'$TOTC'//;t;s/'$TOTC'/\n'$TOTC'/;D' | sed 's/ //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
        arr=($line)
        save=${arr[0]}
        result0=$((save + TOTA))
        save=${arr[1]}
        result1=$((save + TOTA))
        save=${arr[2]}
        result2=$((save + TOTA))
        save=${arr[3]}
        result3=$((save + TOTA))
        save=${arr[4]}
        result4=$((save + TOTA))
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        line2=$(sed -n '2p' files/solution_dode | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/')
        var="${line2} ${line}"
        echo $var | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >>  '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube2' > dump
        REES=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube2 | sed -n 1','1'p' | awk '{print $1}'`

        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.snubcube.py snubcube2 "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 1 > dump
        line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
        arr=($line)
        save=${arr[0]}
        result0=$((save - TOTA))
        save=${arr[1]}
        result1=$((save - TOTA))
        save=${arr[2]}
        result2=$((save - TOTA))
        save=${arr[3]}
        result3=$((save - TOTA))
        save=${arr[4]}
        result4=$((save - TOTA))
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^'$TOTC'//;t;s/'$TOTC'/\n'$TOTC'/;D' | sed 's/ //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
	#line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^[^'$TOTC']*'$TOTC' //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        line2=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //')
	line3=$(sed -n '2p' files/solution_dode | sed 's/'$TOTC'.*//' | sed 's/$/'$TOTC'/')
        var="${line3} ${line} ${line2}"
        echo $var | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >>  '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubcube2.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube2' > dump
        REEES=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_cube2 | sed -n 1','1'p' | awk '{print $1}'`


        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.icosahedron.py icosahedron "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 1 > dump
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^'$TOTC'//;t;s/'$TOTC'/\n'$TOTC'/;D' | sed 's/ //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
	#line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^[^'$TOTC']*'$TOTC' //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
        arr=($line)
        save=${arr[0]}
        result0=$((save + TOTA))
        save=${arr[1]}
        result1=$((save + TOTA))
        save=${arr[2]}
        result2=$((save + TOTA))
        save=${arr[3]}
        result3=$((save + TOTA))
        save=${arr[4]}
        result4=$((save + TOTA))
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        line2=$(sed -n '2p' files/solution_dode | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/')
        var="${line2} ${line}"
        echo $var | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >>  '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_ico' > dump
        RREESS=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_ico | sed -n 1','1'p' | awk '{print $1}'`


        rm -f '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        python3 generate_cls_file.icosahedron.py icosahedron "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test' 1 > dump
        line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //' | sed 's/^/ /g' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^ *//g' | grep -Eo '[-][0-9]+([.][0-9]+)?' | tr '\n' ' ' | sed 's/$/\n/g' | sed 's/-//g')
        arr=($line)
        save=${arr[0]}
        result0=$((save - TOTA))
        save=${arr[1]}
        result1=$((save - TOTA))
        save=${arr[2]}
        result2=$((save - TOTA))
        save=${arr[3]}
        result3=$((save - TOTA))
        save=${arr[4]}
        result4=$((save - TOTA))
	line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^'$TOTC'//;t;s/'$TOTC'/\n'$TOTC'/;D' | sed 's/ //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
	#line=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/^[^'$TOTC']*'$TOTC' //' | sed 's/'$TOTS'.*//' | sed 's/$/'$TOTS'/' | sed 's/^ */ /g' | sed 's/ / -/g' | sed 's/--/-/g' | sed 's/^ *//g' | sed '0,/'$result0'/{s/'$result0'/-'$result0'/}' | sed '0,/'$result1'/{s/'$result1'/-'$result1'/}' | sed '0,/'$result2'/{s/'$result2'/-'$result2'/}' | sed '0,/'$result3'/{s/'$result3'/-'$result3'/}' | sed '0,/'$result4'/{s/'$result4'/-'$result4'/}' | sed 's/--//g')
        line2=$(sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed 's/.*'$TOTS' //')
	line3=$(sed -n '2p' files/solution_dode | sed 's/'$TOTC'.*//' | sed 's/$/'$TOTC'/')
        var="${line3} ${line} ${line2}"
        echo $var | sed 's/ /a /g' | tr ' ' '\n' | sed 's/a/ 0/g' | sed 's/'$TOT'/'$TOT' 0/g' >>  '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
        stringarray=($line)
        save=${stringarray[3]}
        result=$((save + TOT))
        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
        minisat -verb=0 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.icosahedron.fixed.Na'$SPECIES'Nc'$COLORS'.cls' '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_ico' > dump
        RRREEESSS=`cat /home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_ico | sed -n 1','1'p' | awk '{print $1}'`



	if [ $RES = "SAT" ] || [ $RESS = "SAT" ] || [ $RREESS = "SAT" ] || [ $RRREEESSS = "SAT" ] || [ $RESSS = "SAT" ] || [ $RESSSS = "SAT" ] || [ $RRES = "SAT" ] || [ $RRRES = "SAT" ] || [ $REES = "SAT" ] || [ $REEES = "SAT" ] || [ $RETS = "SAT" ] || [ $RETTS = "SAT" ]; then
		echo "Next $i $RES $RESSS $RESSSS $RESS $RREESS $RRREEESSS $RETS $RRES $RRRES $RETTS $REES $REEES"
		sed -n '2p' files/solution_dode | sed 's/'$TOT'.*//' | sed 's/$/'$TOT'/' | sed -e 's/^/ /' | sed 's/ / -/g' | sed 's/ --/ /g' | sed 's/^[ \t]*//' | sed 's/'$TOT'/'$TOT' 0/g' >> '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubdode.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
		line=$(head -n 1 '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubdode.fixed.Na'$SPECIES'Nc'$COLORS'.cls')
	        stringarray=($line)
		save=${stringarray[3]}
        	result=$((save + 1))
	        var="${stringarray[0]} ${stringarray[1]} ${stringarray[2]} ${result}"
	        sed -i "1s/.*/$var/" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/test.snubdode.fixed.Na'$SPECIES'Nc'$COLORS'.cls'
	else
		echo "Done $i $RES $RESS $RESSS $RESSSS $RRES $RRRES $REES $REEES $RREESS $RRREEESSS"
		i=$END
		python3 generate_cls_file.snubcube.py snubdode "$SPECIES" "$COLORS" '/home/diogo/MEGA/cenas/SAT-assembly/Results/scripts/files/solution_dode' 0
		#cp files/solution_dode.converted saved_sols_dodecahedron_exclusion/solution_dode.converted_"$i"
	fi
done

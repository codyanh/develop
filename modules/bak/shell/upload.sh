#!/bin/bash

zip_src=$1
mnt_path='/mnt/server'
script_path='/mnt/script'

cd ${mnt_path}

ls | grep -v `basename $zip_src` | xargs rm -rf

unzip $zip_src 2> /dev/null

for i in {1..16}
do
	cp -r GS GS$i
done
rm -rf GS/

for i in `ls GS* -d`
do
	mv ${i}/GS1 ${i}/${i}
	sed -i "s/GS/${i}/g" ${i}/run_newgs.sh
	chmod +x ${i}/${i} ${i}/run_newgs.sh
done


for i in {1..6}
do
	cp -r BCS BCS$i
done
rm -rf BCS/

for i in `ls BCS* -d`
do
	mv ${i}/BCS1 ${i}/${i}
	sed -i "s/BCS/${i}/g" ${i}/run_newbcs.sh
	chmod +x ${i}/${i} ${i}/run_newbcs.sh
done

for i in SCS DBS CCS DBM LS
do
    chmod +x $i/$i $i/run_new`echo $i|tr [A-Z] [a-z]`.sh
done

chmod +x blob/BLOB

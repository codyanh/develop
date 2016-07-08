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
	mv ${i}/GS1 ${i}/${i} 2> /dev/null
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
	mv ${i}/BCS1 ${i}/${i} 2> /dev/null
	sed -i "s/BCS/${i}/g" ${i}/run_newbcs.sh
	sed -i "s/127.0.0.1/$(awk '$0~"GDB[ |\t]*$"{print $1}' /etc/hosts)/" ${i}/AHThunkConfig.ini
	chmod +x ${i}/${i} ${i}/run_newbcs.sh
done

for i in SCS DBS CCS DBM LS
do
    chmod +x $i/$i $i/run_new`echo $i|tr [A-Z] [a-z]`.sh
done

chmod +x blob/BLOB

cd /mnt/script/;/usr/bin/expect cp_cfg.sh `awk '$0~"GDB[ |\t]*$"{print $1}' /etc/hosts`

cd $mnt_path
tmp_num=`basename $zip_src | cut -d. -f1`
tmp_num=`expr $tmp_num + 0`
sed -i "s/\(current_version.*([ |\t]*\)[0-9]\([ |\t]*\*[ |\t]*0x1000000\)/\1$tmp_num\2/" SCS/lua/config/server_config/ls_fixed_config.lua
tmp_num=`basename $zip_src | cut -d. -f2`
tmp_num=`expr $tmp_num + 0`
sed -i "s/\(current_version.*([ |\t]*\)[0-9]*\([ |\t]*\*[ |\t]*0x10000\)/\1$tmp_num\2/" SCS/lua/config/server_config/ls_fixed_config.lua
tmp_num=`basename $zip_src | cut -d. -f3`
tmp_num=`expr $tmp_num + 0`
sed -i "s/\(current_version.*+[ |\t]*\)[0-9]*\([ |\t]*[^)]*\)/\1$tmp_num\2/" SCS/lua/config/server_config/ls_fixed_config.lua

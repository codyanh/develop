#!/bin/bash
server_path='/home/AA_server'
mnt_path='/mnt/server'
server_name=`hostname | cut -d_ -f2`
backup_dir=backup`date +%Y%m%d_%H%M%S`

cd $server_path

mkdir $backup_dir

case $server_name in
GS01)
	for DIR in GS2 GS3 GS4 BCS2 lua
	do
		mv $DIR $backup_dir
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS01";;
GS02)
	for DIR in GS5 GS6 GS7 BCS3 lua
	do
		mv $DIR $backup_dir
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS02";;
GS03)
	for DIR in GS8 GS9 GS10 BCS4 lua
	do
		mv $DIR $backup_dir
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS03";;
GS04)
	for DIR in GS11 GS12 GS13 BCS5 lua
	do
		mv $DIR $backup_dir
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS04";;
GS05)
	for DIR in GS14 GS15 GS16 BCS6 lua
	do
		mv $DIR $backup_dir
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS05";;
GSBAK)
	echo "GSBAK have nothing to do!";;
GDB)
	for DIR in CCS DBS SCS blob lua
	do
		mv $DIR $backup_dir
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GDB";;
LS)
	for DIR in GS1 BCS1 LS lua
	do
		mv $DIR $backup_dir
		cp -r $mnt_path/$DIR $server_path
	done
	echo "LS";;
DBM)
	for DIR in DBM lua
	do
		mv $DIR $backup_dir
		cp -r $mnt_path/$DIR $server_path
	done
	echo "DBM";;
*)
	echo "wrong hostname!";;
esac

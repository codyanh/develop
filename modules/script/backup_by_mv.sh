#!/bin/bash
server_path=$1
server_name=$2
backup_dir=backup`date +%Y%m%d_%H%M%S`

cd $server_path

mkdir $backup_dir

case $server_name in
GS1)
	for DIR in GS2 GS3 GS4 BCS2 lua
	do
		mv $DIR $backup_dir
	done
	echo "GS1";;
GS2)
	for DIR in GS5 GS6 GS7 BCS3 lua
	do
		mv $DIR $backup_dir
	done
	echo "GS2";;
GS3)
	for DIR in GS8 GS9 GS10 BCS4 lua
	do
		mv $DIR $backup_dir
	done
	echo "GS3";;
GS4)
	for DIR in GS11 GS12 GS13 BCS5 lua
	do
		mv $DIR $backup_dir
	done
	echo "GS4";;
GS5)
	for DIR in GS14 GS15 GS16 BCS6 lua
	do
		mv $DIR $backup_dir
	done
	echo "GS5";;
GSBAK)
	echo "GSBAK have nothing to do!";;
GDB)
	for DIR in CCS DBS SCS blob lua
	do
		mv $DIR $backup_dir
	done
	echo "GDB";;
LS)
	for DIR in GS1 BCS1 LS lua
	do
		mv $DIR $backup_dir
	done
	echo "LS";;
DBM)
	for DIR in DBM lua
	do
		mv $DIR $backup_dir
	done
	echo "DBM";;
*)
	echo "wrong hostname!"
	exit 1;;
esac

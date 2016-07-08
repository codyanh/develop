#!/bin/bash
server_name=$1
gamegroup=$2
server_path='/home/AA_server'
mnt_path='/mnt/server'
if [[ $gamegroup -ne 1 ]];then
	server_path='/home/AA_server'$gamegroup
	mnt_path='/mnt/server'$gamegroup
fi

cd $server_path

case $server_name in
GS1)
	for DIR in GS2 GS3 GS4 BCS2 lua
	do
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS1";;
GS2)
	for DIR in GS5 GS6 GS7 BCS3 lua
	do
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS2";;
GS3)
	for DIR in GS8 GS9 GS10 BCS4 lua
	do
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS3";;
GS4)
	for DIR in GS11 GS12 GS13 BCS5 lua
	do
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS4";;
GS5)
	for DIR in GS14 GS15 GS16 BCS6 lua
	do
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GS5";;
GSBAK)
	echo "GSBAK have nothing to do!";;
GDB)
	for DIR in CCS DBS SCS blob lua
	do
		cp -r $mnt_path/$DIR $server_path
	done
	echo "GDB";;
LS)
	for DIR in GS1 BCS1 LS lua
	do
		cp -r $mnt_path/$DIR $server_path
	done
	echo "LS";;
DBM)
	for DIR in DBM lua
	do
		cp -r $mnt_path/$DIR $server_path
	done
	echo "DBM";;
*)
	echo "wrong hostname!"
	exit 1;;
esac

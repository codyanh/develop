#!/bin/sh
file=$1
user="syyx"
pass="shangY00"
prefix="http://wscp.lxdns.com:8080/wsCP/servlet/contReceiver?"
purgeurl=`cat $file | sed 's/http:\/\///g' | awk '{print $1}' | xargs echo | sed 's/ /;/g'`
md5sumpass=`printf "${user}${pass}${purgeurl}" | md5sum | awk '{print $1}'`
url="${prefix}username=${user}&passwd=${md5sumpass}&url=${purgeurl}"
echo $url

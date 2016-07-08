#!/bin/bash
../modules/scp_expect.sh patch_list.xml_ws 192.168.30.21:/home/agame/update/patch_list.xml && \
../modules/scp_expect.sh patch_list.xml_lx 192.168.30.21:/home/lx/agame/update/patch_list.xml && \
../modules/scp_expect.sh patch_list.xml_ws 172.19.0.90:/home/agame/update/patch_list.xml && \
../modules/scp_expect.sh patch_list.xml_lx 172.19.0.90:/home/lx/agame/update/patch_list.xml
if [[ $? -eq 0 ]];then
		echo "上传源站完毕,正在推送.."
else
		echo "上传源站失败!"
		exit 1
fi
###################################
echo -n "网宿推送的结果: " ;curl `push_shell_ws/cdnpush.sh push_shell_ws/push_url.patchlist`

###################################
#RID=$(java -jar push_shell_lx/examples-1.2.jar -POST syyx Iewa1Aeph6uu7a "{\"urls\":[\"http://lzupdate04.shangyoo.com/lx/agame/update/patch_list.xml\"],\"callback\":{\"email\":[\"*@*.com\"],\"acptNotice\":false}}" | sed -n "/r_id/s/^.*\"r_id\": \"\([^\"]*\)\".*/\1/p" )
#echo -n "蓝汛推送的结果: "
#for i in {1..6}
#do	
#	RESULT=$(java -jar push_shell_lx/examples-1.2.jar -GET syyx Iewa1Aeph6uu7a $RID )
#    if [[ $( echo $RESULT | grep  "SUCCESS") == "" ]]; then
#        echo "再等会儿..."
#        sleep 10
#    else
#        echo $RESULT
#        exit 0
#    fi
#done
#echo -n "蓝汛可能推送失败了,具体请看返回结果: "; java -jar push_shell_lx/examples-1.2.jar -GET syyx Iewa1Aeph6uu7a $RID


#!/bin/bash
../modules/scp_expect.sh patch_list.xml_ws 192.168.30.21:/home/agame/update/patch_list.xml && \
../modules/scp_expect.sh patch_list.xml_lx 192.168.30.21:/home/lx/agame/update/patch_list.xml && \
../modules/scp_expect.sh patch_list.xml_ws 172.19.0.90:/home/agame/update/patch_list.xml && \
../modules/scp_expect.sh patch_list.xml_lx 172.19.0.90:/home/lx/agame/update/patch_list.xml
if [[ $? -eq 0 ]];then
		echo "�ϴ�Դվ���,��������.."
else
		echo "�ϴ�Դվʧ��!"
		exit 1
fi
###################################
echo -n "�������͵Ľ��: " ;curl `push_shell_ws/cdnpush.sh push_shell_ws/push_url.patchlist`

###################################
#RID=$(java -jar push_shell_lx/examples-1.2.jar -POST syyx Iewa1Aeph6uu7a "{\"urls\":[\"http://lzupdate04.shangyoo.com/lx/agame/update/patch_list.xml\"],\"callback\":{\"email\":[\"*@*.com\"],\"acptNotice\":false}}" | sed -n "/r_id/s/^.*\"r_id\": \"\([^\"]*\)\".*/\1/p" )
#echo -n "��Ѵ���͵Ľ��: "
#for i in {1..6}
#do	
#	RESULT=$(java -jar push_shell_lx/examples-1.2.jar -GET syyx Iewa1Aeph6uu7a $RID )
#    if [[ $( echo $RESULT | grep  "SUCCESS") == "" ]]; then
#        echo "�ٵȻ��..."
#        sleep 10
#    else
#        echo $RESULT
#        exit 0
#    fi
#done
#echo -n "��Ѵ��������ʧ����,�����뿴���ؽ��: "; java -jar push_shell_lx/examples-1.2.jar -GET syyx Iewa1Aeph6uu7a $RID


#!/bin/bash

#wdve_list_file=$1

echo -n "�������͵Ľ����";curl `push_shell_ws/cdnpush.sh push_shell_ws/push_url_wdver_list`

########################################################

RID=$(java -jar push_shell_lx/examples-1.2.jar -POST syyx Iewa1Aeph6uu7a "{\"urls\":[\"http://lzupdate04.shangyoo.com/lx/agame/update/wdver_list.xml\"],\"callback\":{\"email\":[\"*@*.com\"],\"acptNotice\":false}}" | sed -n "/r_id/s/^.*\"r_id\": \"\([^\"]*\)\".*/\1/p" )

echo -n "��Ѵ���͵Ľ����"

for i in {1..6}
do
	RESULT=$(java -jar push_shell_lx/examples-1.2.jar -GET syyx Iewa1Aeph6uu7a $RID )
	if [[$(echo $RESULT | grep "SUCCESS") == ""]]; then
		echo "�ٵȻ�......"
		sleep 10
	else
		echo $RESULT
		exit 0
	fi
done

echo -n "��Ѵ��������ʧ����,�����뿴���ؽ��: "; java -jar push_shell_lx/examples-1.2.jar -GET syyx Iewa1Aeph6uu7a $RID

#!/bin/bash
../modules/scp_expect.sh 172.19.0.90:/home/agame/update/patch_list.xml patch_list.xml_ws && \
../modules/scp_expect.sh 172.19.0.90:/home/lx/agame/update/patch_list.xml patch_list.xml_lx
if [[ $? -eq 0 ]];then
	echo "����patch_list.xml�����سɹ�"
else
	echo "����patch_list.xml������ʧ��"
	exit 1
fi

echo "��ʼ����patch"
sed -i "/<\/patch>/d" patch_list.xml_ws
sed -i "/<\/root>/d" patch_list.xml_ws
sed -i "/<\/patch>/d" patch_list.xml_lx
sed -i "/<\/root>/d" patch_list.xml_lx

sed -n "/<file filename=/p" patchfile/*.txt >> patch_list.xml_ws
sed -n "/<file filename=/p" patchfile/*.txt >> patch_list.xml_lx

echo "</patch>" >> patch_list.xml_ws
echo "</root>" >> patch_list.xml_ws
echo "</patch>" >> patch_list.xml_lx
echo "</root>" >> patch_list.xml_lx

echo "patch_list.xml������ɣ���鿴patch_list.xml�Ƿ���ȷpatch_list.xml_ws(lx)"

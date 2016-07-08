#!/bin/bash
../modules/scp_expect.sh 172.19.0.90:/home/agame/update/patch_list.xml patch_list.xml_ws && \
../modules/scp_expect.sh 172.19.0.90:/home/lx/agame/update/patch_list.xml patch_list.xml_lx
if [[ $? -eq 0 ]];then
	echo "下载patch_list.xml到本地成功"
else
	echo "下载patch_list.xml到本地失败"
	exit 1
fi

echo "开始生成patch"
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

echo "patch_list.xml生成完成，请查看patch_list.xml是否正确patch_list.xml_ws(lx)"

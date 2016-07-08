#!/bin/bash

#wdve_list_file=$1

echo -n "网宿推送的结果：";curl `push_shell_ws/cdnpush.sh push_shell_ws/push_url_dlf`

########################################################

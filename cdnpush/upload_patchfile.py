#!/usr/bin/python
#-*- coding: utf-8 -*-
import urllib
import urllib2
import sys
import os
import time
import hashlib
import commands

UPLOAD_DIR='patchfile/'

UPLOAD_FILE=os.popen('ls %s |grep -v txt' % UPLOAD_DIR).readlines()
if not UPLOAD_FILE:
    print "%s have nothing!" % UPLOAD_DIR
    exit(1)

for filename in UPLOAD_FILE:
    print "../modules/scp_expect.sh %s%s %s" % (UPLOAD_DIR,filename.strip('\n'),"172.19.0.90:/home/agame/update/patchfile/")
    result = commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_DIR,filename.strip('\n'),"172.19.0.90:/home/agame/update/patchfile/"))
    if result[0] != 0:
        print "upload faild!"
        exit(1)

# exit(1)

LX_FIRST_ITEM_ID=''
lx_context=''
WS_FIRST_ITEM_ID=''
ws_context=''

for filename in UPLOAD_FILE:
    time.sleep(1)
    ###################   网宿的item信息  ##################
    LX_ITEM_ID=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    if not LX_FIRST_ITEM_ID:
        LX_FIRST_ITEM_ID = LX_ITEM_ID
    UPLOAD_FILENAME=os.path.basename(filename.strip('\n'))
    LX_SOURCE_PATH="http://121.43.166.36/agame/update/patchfile/" + UPLOAD_FILENAME
    LX_PUBLISH_PATH="http://lzdownload04.shangyoo.com/lz/update/patchfile/" + UPLOAD_FILENAME
    LX_MD5=os.popen("md5sum %s%s" % (UPLOAD_DIR,filename.strip('\n'))).readlines()[0].split()[0]

    lx_context_item='''
        <item_id value="%s">
            <source_path>%s</source_path>
            <publish_path>%s</publish_path>
            <md5>%s</md5>
            <checktype>MD5</checktype>
            <file_size></file_size>
            <unzip>0</unzip>
        </item_id>''' % (LX_ITEM_ID,LX_SOURCE_PATH,LX_PUBLISH_PATH,LX_MD5)
    lx_context = lx_context + lx_context_item

    ###################   蓝汛的item信息  ##################
    WS_ITEM_ID=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    if not WS_FIRST_ITEM_ID:
        WS_FIRST_ITEM_ID = WS_ITEM_ID
    UPLOAD_FILENAME=os.path.basename(filename.strip('\n'))
    WS_SOURCE_PATH="http://121.43.166.36/agame/update/patchfile/" + UPLOAD_FILENAME
    WS_PUBLISH_PATH="http://updatelz02.shangyoo.com/lz/update/patchfile/" + UPLOAD_FILENAME
    WS_MD5=os.popen("md5sum %s%s" % (UPLOAD_DIR,filename.strip('\n'))).readlines()[0].split()[0]

    ws_context_item='''
        <item_id value="%s">
            <source_path>%s</source_path>
            <publish_path>%s</publish_path>
            <md5>%s</md5>
            <file_size></file_size>
        </item_id>''' % (WS_ITEM_ID,WS_SOURCE_PATH,WS_PUBLISH_PATH,WS_MD5)
    ws_context = ws_context + ws_context_item

###################   网宿的context xml信息  ##################
WS_CUST_ID="syyx"
ws_tmpMd5Obj = hashlib.md5()
ws_tmpMd5Obj.update(WS_FIRST_ITEM_ID + WS_CUST_ID + 'chinanetcenter8gO0bi5bCIfH')
WS_PASSWD = ws_tmpMd5Obj.hexdigest()
ws_context_head='''
<?xml version="1.0" encoding="UTF-8"?>
    <ccsc>
        <cust_id>%s</cust_id>
        <passwd>%s</passwd>''' % (WS_CUST_ID,WS_PASSWD)
ws_context_end='''
    </ccsc>'''
ws_context=ws_context_head + ws_context + ws_context_end

###################   蓝汛的context xml信息  ##################
LX_CUST_ID="2993"
tmpMd5Obj = hashlib.md5()
tmpMd5Obj.update(LX_FIRST_ITEM_ID + LX_CUST_ID + 'chinacacheIewa1Aeph6uu7a')
LX_PASSWD = tmpMd5Obj.hexdigest()
lx_context_head='''
<?xml version="1.0" encoding="UTF-8"?>
    <ccsc>
        <cust_id>%s</cust_id>
        <passwd>%s</passwd>''' % (LX_CUST_ID,LX_PASSWD)
lx_context_end='''
    </ccsc>'''
lx_context=lx_context_head + lx_context + lx_context_end


# exit(1)
######################调用网宿接口########################
ws_post_data={'op':'publish','context':ws_context}
ws_post_data_urlencode = urllib.urlencode(ws_post_data)
ws_post_url="http://fd.chinanetcenter.com:8080/HttpUpdate/publishService.do"

ws_res_data = urllib2.urlopen(urllib2.Request(url = ws_post_url,data = ws_post_data_urlencode))
print 'WS push result:\n%s' % ws_res_data.read()

######################调用蓝汛接口########################
lx_post_data={'op':'publish','context':lx_context}
lx_post_data_urlencode = urllib.urlencode(lx_post_data)
lx_post_url="http://centre.fds.ccgslb.net:8080/fds/soap/receiveTask.php"

lx_res_data = urllib2.urlopen(urllib2.Request(url = lx_post_url,data = lx_post_data_urlencode))
print 'LX push result:\n%s' % lx_res_data.read()

os.system("mv %s/* %s_bak/" % (UPLOAD_DIR.strip('/'),UPLOAD_DIR.strip('/')))

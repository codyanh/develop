#!/usr/bin/python
#-*- coding: utf-8 -*-

from read_proc_cfg import *
from read_gamegroup_cfg import *
import pexpect
import re
import os
import commands
# import signal
import socket
import time

import GlobalConfig
# GameGroupCfgFile = GlobalConfig.GameGroupCfgFile
ServerCfgFile = GlobalConfig.ServerCfgFile

class init_server:
    RESULT = ''
    LOG_FILE = ''
    
    def __init__(self,server_infomation):
        self.SERVER_NAME =  server_infomation[0].strip()
        self.SERVER_MACHINE =  server_infomation[1].strip()
        self.SERVER_IP_SEGMENT =  server_infomation[2].strip()
        self.NICK_NAME =  server_infomation[3]
        self.GAME_GROUP =  server_infomation[4].strip()
        self.HOME_PATH = server_infomation[5].strip()
        self.UPLOAD_PATH = server_infomation[6].strip()
        self.FILEWALL_PORT = server_infomation[7].strip()

        TmpProc = read_proc_cfg(ServerCfgFile)
        if self.GAME_GROUP == '21' or self.GAME_GROUP == "22" or self.GAME_GROUP == "23" or self.GAME_GROUP == "24" or self.GAME_GROUP == "25":
            self.GS1_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS1',self.GAME_GROUP)
            self.GS2_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS2',self.GAME_GROUP)
            self.GS3_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS3',self.GAME_GROUP)
            self.GS4_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS4',self.GAME_GROUP)
            self.GS5_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS5',self.GAME_GROUP)
            self.GSBAK_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS5',self.GAME_GROUP)
            self.GDB_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GDB',self.GAME_GROUP)
            self.LS_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('LS',self.GAME_GROUP)
            self.DBM_IP = '172.16.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('DBM',self.GAME_GROUP)
        else:		
       	    self.GS1_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS1',self.GAME_GROUP)
            self.GS2_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS2',self.GAME_GROUP)
            self.GS3_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS3',self.GAME_GROUP)
            self.GS4_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS4',self.GAME_GROUP)
            self.GS5_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GS5',self.GAME_GROUP)
            if self.GAME_GROUP == '3' or self.GAME_GROUP == '4' or self.GAME_GROUP == '5':
                self.GSBAK_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.3'
            elif self.GAME_GROUP == '6' or self.GAME_GROUP == '7' or self.GAME_GROUP == '8':
                self.GSBAK_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.13'
            elif self.GAME_GROUP == '9' or self.GAME_GROUP == '10' or self.GAME_GROUP == '11':	
                self.GSBAK_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.23'
            elif self.GAME_GROUP == '12' or self.GAME_GROUP == '13' or self.GAME_GROUP == '14':
                self.GSBAK_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.18'
            elif self.GAME_GROUP == '15' or self.GAME_GROUP == '16' or self.GAME_GROUP == '17':	
                self.GSBAK_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.28'
       	    elif self.GAME_GROUP == '18' or self.GAME_GROUP == '19' or self.GAME_GROUP == '20':	
                self.GSBAK_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.38'
            else:
                self.GSBAK_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.6'
            self.GDB_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('GDB',self.GAME_GROUP)
            self.LS_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('LS',self.GAME_GROUP)
            self.DBM_IP = '192.168.' + self.SERVER_IP_SEGMENT + '.' + TmpProc.get_machine_ip('DBM',self.GAME_GROUP)


    def IP(self,proc_name):
        proc_ip = read_proc_cfg(ServerCfgFile).get_proc_ipaddr(proc_name,int(self.GAME_GROUP))
        if not proc_ip:
            print '<init_server.IP()> 找不到服务名为 %s 的IP信息' % proc_name
            return False
        else:
            if self.GAME_GROUP == '21' or self.GAME_GROUP == "22" or self.GAME_GROUP == "23" or self.GAME_GROUP == "24" or self.GAME_GROUP == "25":
                return '172.16.' + self.SERVER_IP_SEGMENT + '.' + proc_ip
            else:
                return '192.168.' + self.SERVER_IP_SEGMENT + '.' + proc_ip


    def PROCNAME(self,proc_name):
        procRealName = read_proc_cfg(ServerCfgFile).get_real_proc_name(proc_name,self.GAME_GROUP)
        if not procRealName:
            print '<init_server.PROCNAME()> 找不到服务名为 %s 的真实进程名' % procRealName
            return False
        else:
            return procRealName

    def PORT(self,proc_name):
        proc_port = read_proc_cfg(ServerCfgFile).get_proc_telnet_port(proc_name,int(self.GAME_GROUP))
        if not proc_port:
            print '<init_server.PORT()> 找不到服务名为 %s 的telnet 端口信息' % proc_name
            return False
        else:
            return proc_port

    def PATH(self,proc_name):
        proc_path = read_proc_cfg(ServerCfgFile).get_proc_path(proc_name,self.GAME_GROUP)
        if not proc_path:
            print '<init_server.PATH()> 找不到服务名为 %s 的目录信息' % proc_name
            return False
        else:
            return proc_path

    def LOG(self,str):
        try:
            f = open(self.LOG_FILE,'ab')
            f.write(str)
            f.close()
        except Exception,e:
            f.close()

    def create_ssh_conn(self,server_ip_add):
        username = 'omadmin'
        passwd = 'shangyoo!@#$'
        ssh_newkey = 'Are you sure you want to continue connecting'
        try:
            pe = pexpect.spawn('ssh ' + username.strip() + '@' + server_ip_add.strip())
            # pe.logfile = open(self.LOG_FILE,'ab')
            index = pe.expect([ssh_newkey,'(?i)password:','~$','~#',pexpect.TIMEOUT])
            if index == 0:
                pe.sendline('yes')
                pe.expect('(?i)password:')
                pe.sendline(passwd)
            elif index == 1:
                pe.sendline(passwd)
            elif index == 4:
                return False
            return pe
        except Exception,e:
            print 'Connecting %s@%s ERROR!!\nError:%s' % (username,server_ip_add,e)
            return False

    def create_root_conn(self,server_ip_add):
        username = 'root'
        passwd = 'syyx_REW_&*('
        ssh_newkey = 'Are you sure you want to continue connecting'
        try:
            pe = pexpect.spawn('ssh ' + username.strip() + '@' + server_ip_add.strip())
            # pe.logfile = open(self.LOG_FILE,'ab')
            index = pe.expect([ssh_newkey,'(?i)password:','~$','~#',pexpect.TIMEOUT])
            if index == 0:
                pe.sendline('yes')
                pe.expect('(?i)password:')
                pe.sendline(passwd)
            elif index == 1:
                pe.sendline(passwd)
            elif index == 4:
                return False
            return pe
        except Exception,e:
            print 'Connecting %s@%s ERROR!!\nError:%s' % (username,server_ip_add,e)
            return False

    def excute_cmd(self,ip_add,cmd):
        connection = self.create_ssh_conn(ip_add)
        if not connection:
            print '不能创建连接到%s' % ip_add
            return False
        connection.logfile = open(self.LOG_FILE,'ab')
        # regex = re.compile('^cmd_result:(.)')
        regex = re.compile('^cmd_result:(.)')
        
        try:
            connection.sendline(cmd)
            #a = connection.isalive()
            #while a == True:
            #    time.sleep(1)
            #    print a
            #print a
            #connection.expect(pexpect.EOF,timeout=None)
            #print 0
            #connection.expect('FinishUpload!',timeout=None)
            #print 1
            cmd_result='echo "cmd_result:`echo $?`"'
            connection.sendline(cmd_result)
			#connection.sendline('echo "cmd_result:`echo $?`"')
            #print 2
            connection.expect('cmd_result:',timeout=None)
            #print 3
            tmp_line = connection.readline()
            #print tmp_line
            while tmp_line:
                # print tmp_line
                if tmp_line and regex.match(tmp_line):
                    excute_result = regex.match(tmp_line).group(1)
                   #print excute_result
                    if excute_result == '0':
                        self.RESULT = True
                        connection.close()
                        return True
                    else:
                        self.RESULT = False
                        connection.close()
                        return False
                else:
                    tmp_line = connection.readline()

            self.RESULT = False
            connection.close()
            return False
        except Exception,e:
            self.RESULT = False
            connection.close()
            print 'Excuting %s ERROR!!\nERROR MSG:%s' % (cmd,e)
            return False


    def excute_upload_cmd(self,ip_add,cmd):
        connection = self.create_ssh_conn(ip_add)
        if not connection:
            print '不能创建连接到%s' % ip_add
            return False
        connection.logfile = open(self.LOG_FILE,'ab')
        # regex = re.compile('^cmd_result:(.)')
        regex = re.compile('^cmd_result:(.)')
        
        try:
            connection.sendline(cmd)
            #a = connection.isalive()
            #while a == True:
            #    time.sleep(1)
            #    print a
            #print a
            #connection.expect(pexpect.EOF,timeout=None)
            #print 0
            connection.expect('FinishUpload!',timeout=None)
            #print 1
            cmd_result='echo "cmd_result:`echo $?`"'
            connection.sendline(cmd_result)
			#connection.sendline('echo "cmd_result:`echo $?`"')
            #print 2
            connection.expect('cmd_result:',timeout=None)
            #print 3
            tmp_line = connection.readline()
            #print tmp_line
            while tmp_line:
                # print tmp_line
                if tmp_line and regex.match(tmp_line):
                    excute_result = regex.match(tmp_line).group(1)
                   #print excute_result
                    if excute_result == '0':
                        self.RESULT = True
                        connection.close()
                        return True
                    else:
                        self.RESULT = False
                        connection.close()
                        return False
                else:
                    tmp_line = connection.readline()

            self.RESULT = False
            connection.close()
            return False
        except Exception,e:
            self.RESULT = False
            connection.close()
            print 'Excuting %s ERROR!!\nERROR MSG:%s' % (cmd,e)
            return False


    def excute_root_cmd(self,ip_add,cmd):
        connection = self.create_root_conn(ip_add)
        if not connection:
            print '不能创建连接到%s' % ip_add
            return False
        connection.logfile = open(self.LOG_FILE,'ab')
        regex = re.compile('^cmd_result:(.)')
        
        try:
            connection.sendline(cmd)
            connection.sendline('echo "cmd_result:`echo $?`"')
            connection.expect('cmd_result:',timeout=None)
            tmp_line = connection.readline()
            while tmp_line:
                if tmp_line and regex.match(tmp_line):
                    excute_result = regex.match(tmp_line).group(1)
                    if excute_result == '0':
                        self.RESULT = True
                        connection.close()
                        return True
                    else:
                        self.RESULT = False
                        connection.close()
                        return False
                else:
                    tmp_line = connection.readline()

            self.RESULT = False
            connection.close()
            return False
        except Exception,e:
            self.RESULT = False
            connection.close()
            print 'Excuting %s ERROR!!\nERROR MSG:%s' % (cmd,e)
            return False         

    def excute_telnet_cmd(self,server_ip_add,port,tn_cmd):
        username = 'root'
        passwd = 'root'
        try:
            connection = pexpect.spawn('telnet ' + server_ip_add.strip() + ' ' + port)
            connection.logfile = open(self.LOG_FILE,'ab')
            index = connection.expect(['(?i)login:', '(?i)username', '(?i)Unknown host',pexpect.TIMEOUT]) 
            if index == 2 or index == 3:
                print 'telnet %s %s Fail!!\n' % (server_ip_add,port)
                return False
            connection.write(username + '\r')
            index = connection.expect(['(?i)password:',pexpect.TIMEOUT])
            if index == 0:
                connection.sendline(passwd + '\r')
            else:
                return False
            
            connection.expect('>')
            connection.sendline(tn_cmd + '\r')

        except Exception,e:
            print 'telnet %s %s ERROR!!\nError:%s' % (server_ip_add,port,e)
            self.RESULT = False
            return False
		######################################################20151113shanzhu added ,the purpose is to make the script do not throw the exception like EOF or Timeout##################
        try:
            index2 = connection.expect(['>','Connection closed by foreign host.'],timeout=None)
            if index2 == 0:
                connection.sendline('exit\r')
                connection.close()
            elif index2 == 1:
                connection.close()
				
            self.RESULT = True
            return True
        except Exception,e:
            print 'telnet %s %s Exit ERROR!!\nError:%s' % (server_ip_add,port,e)
            self.RESULT = False
            return False


    def multiple_excute_telnet_cmd(self,proc_list,tn_cmd):
        for proc_name in proc_list:
            proc_cfg = read_proc_cfg(ServerCfgFile)
            proc_ip = self.IP(proc_name)
            proc_port = self.PORT(proc_name)

            if not self.excute_telnet_cmd(proc_ip,proc_port,tn_cmd):
                return False

    #############################################################
    # function : check_firewall
    # usage : check the firewall open or close
    #############################################################
    def check_firewall(self):
        fw_cmd = 'test $(iptables-save | sed -n "/-A INPUT -i bond1 -p tcp -m tcp --dport ' + self.FILEWALL_PORT.strip() + ' -j ACCEPT/p" | wc -l ) == \'1\' '  
        fw_cloud_cmd = 'test $(iptables-save | sed -n "/-A INPUT -i eth0 -p tcp -m tcp --dport ' + self.FILEWALL_PORT.strip() + ' -j ACCEPT/p" | wc -l ) == \'1\' '  
       
        if self.GAME_GROUP == '21' or self.GAME_GROUP =="22" or self.GAME_GROUP == "23" or self.GAME_GROUP == "24" or self.GAME_GROUP == "25":
		
            try:
                if not self.excute_root_cmd(self.LS_IP,fw_cloud_cmd):
                    print 'the \033[0;32;40m first \033[0m gamegroup\'s firewall setting is \033[0;31;40m off \033[0m'
                    return False
                else:
                    print 'the \033[0;32;40m first \033[0m gamegroup\'s firewall setting is \033[0;32;40m on \033[0m'
                    return True     
            
            except Exception,e:
                print 'Excuting function <check_firewall> ERROR!!\nERROR MSG:%s' % (e)
                return False
        else:

            try:
                if not self.excute_root_cmd(self.LS_IP,fw_cmd):
                    print 'the \033[0;32;40m first \033[0m gamegroup\'s firewall setting is \033[0;31;40m off \033[0m'
                    return False
                else:
                    print 'the \033[0;32;40m first \033[0m gamegroup\'s firewall setting is \033[0;32;40m on \033[0m'
                    return True     
            
            except Exception,e:
                print 'Excuting function <check_firewall> ERROR!!\nERROR MSG:%s' % (e)
                return False

    ##################################################################
    # options:
    # 1: on , 0: off
    #################################################################
    def set_firewall(self,options): 
        if options not in [1,0]:
            print 'Wrong <options> values givn in function <set_firewall>!'
            self.RESUTL = False
            return False
        
        set_fw_cmd_on = 'iptables -I INPUT -i bond1 -p tcp -m tcp --dport ' + self.FILEWALL_PORT.strip() + ' -j ACCEPT'
        set_fw_cmd_off = 'iptables -D INPUT -i bond1 -p tcp -m tcp --dport ' + self.FILEWALL_PORT.strip() + ' -j ACCEPT'

        set_fw_cloud_cmd_on = 'iptables -I INPUT -i eth0 -p tcp -m tcp --dport ' + self.FILEWALL_PORT.strip() + ' -j ACCEPT'
        set_fw__cloud_cmd_off = 'iptables -D INPUT -i eth0 -p tcp -m tcp --dport ' + self.FILEWALL_PORT.strip() + ' -j ACCEPT'
       
        if self.GAME_GROUP == '21' or self.GAME_GROUP == "22" or self.GAME_GROUP == "23" or self.GAME_GROUP == "24" or self.GAME_GROUP == "25":
            try:
                if options == 1:
                    if self.excute_root_cmd(self.LS_IP,set_fw_cloud_cmd_on):
                        self.RESULT = True
                        return True
                    else:
                        print '\033[0;32;40m %s \033[0m防火墙开启失败...' % self.NICK_NAME
                        self.RESULT = False
                        return False
                if options == 0:
                    if self.excute_root_cmd(self.LS_IP,set_fw__cloud_cmd_off):
                        self.RESULT = True
                        return True
                    else:
                        print '\033[0;32;40m %s \033[0m防火墙关闭失败...' % self.NICK_NAME
                        self.RESULT = False
                        return False
            except Exception,e:
                print 'Excuting function <set_firewall> ERROR!!\nERROR MSG:%s' % (e)
                self.RESUTL = False
                return False
        else:
            try:
                if options == 1:
                    if self.excute_root_cmd(self.LS_IP,set_fw_cmd_on):
                        self.RESULT = True
                        return True
                    else:
                        print '\033[0;32;40m %s \033[0m防火墙开启失败...' % self.NICK_NAME
                        self.RESULT = False
                        return False
                if options == 0:
                    if self.excute_root_cmd(self.LS_IP,set_fw_cmd_off):
                        self.RESULT = True
                        return True
                    else:
                        print '\033[0;32;40m %s \033[0m防火墙关闭失败...' % self.NICK_NAME
                        self.RESULT = False
                        return False
            except Exception,e:
                print 'Excuting function <set_firewall> ERROR!!\nERROR MSG:%s' % (e)
                self.RESUTL = False
                return False

    ##########################################################
    # file_path:
    #   The file's path what you wanna upload
    # upload_host:
    #   The remote hosts IP'address
    # upload_path:
    #   The path on the remote hosts where you wanna place on
    ##########################################################
    # def upload_file(self,file_path,upload_host,upload_path):
    #     if not os.path.exists(file_path):
    #         print 'Wrong <file_path> values given in function <upload_file>!'
    #         self.RESULT = False
    #         return False
    #     conn = self.create_ssh_conn(upload_host)
    #     if not conn:
    #         print 'Can\'t connect the %s given in function <upload_file>!' % upload_host
    #         self.RESULT = False
    #         return False
    #     conn.logfile = open(self.LOG_FILE,'ab')
    #     if not self.excute_cmd(upload_host,'test -d ' + upload_path):
    #         print 'Wrong <upload_path> values given in function <upload_file>!'
    #         self.RESULT = False
    #         return False

    #     time.sleep(1)
    #     try:
    #         upload_shell = '../modules/scp_expect.sh '
    #         upload_cmd = upload_shell + ' ' + file_path + ' ' + upload_host + ':' + upload_path
    #         # print '#%s#' % upload_cmd
    #         print '%s UPLOADING...' % self.NICK_NAME
    #         upl_result = commands.getstatusoutput(upload_cmd)
    #         if upl_result[0] != 0:
    #             print 'Excuting '+ upload_cmd +' ERROR!!\nERROR MSG:%s' % upl_result
    #             self.RESULT = False
    #             return False
    #         else:
    #             print '%s UPLOADING\033[0;32;40m OK!\033[0m' % self.NICK_NAME
    #             self.RESULT = True
    #             return upl_result
    #     except KeyboardInterrupt:
    #         self.RESULT = False
    #         return False
    #     except Exception,e:
    #         print 'Excuting function <upload_file> ERROR!!\nERROR MSG:%s' % (e)
    #         self.RESULT = False
    #         return False

    def upload_file(self,file_path,upload_host,upload_path):
        if not os.path.exists(file_path):
            print 'Wrong <file_path> values given in function <upload_file>!'
            self.RESULT = False
            return False

        # if not self.excute_cmd(upload_host,'test -d ' + upload_path):
        #     print 'Wrong <upload_path> values given in function <upload_file>!'
        #     self.RESULT = False
        #     return False

        time.sleep(1)
        try:
            upload_shell = '../modules/scp_expect.sh '
            upload_cmd = upload_shell + ' ' + file_path + ' ' + upload_host + ':' + upload_path
            # print '#%s#' % upload_cmd
            print '%s UPLOADING...' % self.NICK_NAME
            upl_result = commands.getstatusoutput(upload_cmd)
            open(self.LOG_FILE,'ab').write(upl_result[1])
            if upl_result[0] != 0:
                print 'Excuting '+ upload_cmd +' ERROR!!\nERROR MSG:%s' % upl_result
                self.RESULT = False
                return False
            else:
                print '%s UPLOADING\033[0;32;40m OK!\033[0m' % self.NICK_NAME
                self.RESULT = True
                return upl_result
        except KeyboardInterrupt:
            self.RESULT = False
            return False
        except Exception,e:
            print 'Excuting function <upload_file> ERROR!!\nERROR MSG:%s' % (e)
            self.RESULT = False
            return False

    def multiple_upload_file(self,file_path,upload_path,proc_list):
        multiple_upload_result = True
        for proc_name in proc_list:
            proc_cfg = read_proc_cfg(ServerCfgFile)
            proc_path = proc_cfg.get_proc_path(proc_name,self.GAME_GROUP)
            upload_host = self.IP(proc_name)
            final_upload_path = proc_path + upload_path
            if not self.upload_file(file_path,upload_host,final_upload_path):
                multiple_upload_result = False

        if not multiple_upload_result:
            self.RESULT = False
            return False
        else:
            self.RESULT = True
            return True

    def download_file(self,download_path,remote_host,remote_path):
        # conn = self.create_ssh_conn(remote_host)
        # if not conn:
        #     print 'Can\'t connect the %s given in function <upload_file>!' % remote_host
        #     self.RESULT = False
        #     return False
        # conn.logfile = open(self.LOG_FILE,'ab')
        # if not self.excute_cmd(remote_host,'ls ' + remote_path ):
        #     print 'Wrong <remote_path> values given in function <download_file>!'
        #     self.RESULT = False
        #     return False
        if not os.path.exists(download_path):
            os.makedirs(download_path.rstrip('/'))

        time.sleep(1)
        try:
            download_shell = '../modules/scp_expect.sh '
            download_cmd = download_shell + ' ' + remote_host + ':' + remote_path + ' ' + download_path
            # print download_cmd
            print '%s DOWNLOADING...' % self.NICK_NAME
            downl_result = commands.getstatusoutput(download_cmd)
            open(self.LOG_FILE,'ab').write(downl_result[1])
            if downl_result[0] != 0:
                print 'Excuting '+ download_cmd +' ERROR!!\nERROR MSG:%s' % downl_result
                self.RESULT = False
                return False
            else:
                print '%s DOWNLOADING\033[0;32;40m OK! \033[0m' % self.NICK_NAME
                self.RESULT = True
                return downl_result
        except KeyboardInterrupt:
            self.RESULT = False
            return False
        except Exception,e:
            print 'Excuting function <download_file> ERROR!!\nERROR MSG:%s' % (e)
            self.RESULT = False
            return False

    def multiple_download_file(self,download_path,proc_list):
        multiple_download_result = True
        dl_path = '../DOWNLOAD/' + self.SERVER_NAME + time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time())) + '/'
        for proc_name in proc_list:
            proc_cfg = read_proc_cfg(ServerCfgFile)
            proc_path = proc_cfg.get_proc_path(proc_name,self.GAME_GROUP)
            proc_dl_path = dl_path + proc_name + '/'
            remote_host = self.IP(proc_name)
            remote_path = proc_path + download_path

            if not self.download_file(proc_dl_path,remote_host,remote_path):
                multiple_download_result = False

        if not multiple_download_result:
            self.RESULT = False
            return False
        else:
            self.RESULT = True
            return True

    # def timeout_handler(self,signum,frame):
    #     raise AssertionError('the function running timeout!!')

    def check_keyword(self,host_ip,file_path,key_word,word_count=1,Timeout=30):
        host_conn = self.create_ssh_conn(host_ip)
        if not host_conn:
            print '不能创建连接到%s' % host_ip
            return False
        host_conn.logfile = open(self.LOG_FILE,'ab')
        check_result = self.excute_cmd(host_ip,'test -f ' + file_path)
        if not check_result:
            print 'Wrong <file_path> values given in function <check_log>! %s' % file_path
            host_conn.close()
            return False
        
        # check_keyword_cmd = 'tail -n +1 -f ' + file_path
        check_keyword_cmd = 'tail -n 1000 -f ' + file_path
        # regex = re.compile('.*' + key_word + '.*')
        try:
            # signal.signal(signal.SIGALRM,self.timeout_handler)
            # signal.alarm(timeout)
            cur_count = 0
            host_conn.sendline(check_keyword_cmd)
            for i in range(word_count):
                expect_result = host_conn.expect([key_word,pexpect.TIMEOUT],timeout=Timeout)
                if expect_result == 0:
                    cur_count = cur_count + 1
                elif expect_result == 1:
                    break

            if cur_count == word_count:
                host_conn.close()
                return True
            else:
                host_conn.close()
                return False

            # while True:
            #     cur_count = 0
            #     host_conn.sendline(check_keyword_cmd)
            #     # host_conn.expect(check_keyword_cmd)
            #     tmp_line = host_conn.readline()
            #     while tmp_line:
            #         print '#%s#' % tmp_line
            #         if regex.match(tmp_line):
            #             cur_count = cur_count + 1
            #         if cur_count >= word_count:
            #             host_conn.close()
            #             return True
            #         tmp_line = host_conn.readline()

        except KeyboardInterrupt:
            return False

        except Exception,e:
            print 'Excuting function <found_keyword> ERROR!!\nERROR MSG:%s' % (e)
            host_conn.close()
            return False

    def check_proc_id(self,proc_name):
        host_ip = self.IP(proc_name)

		#20151019山竹增加判断进程名的过程
        #chk_proc_cmd = 'pidof ' + self.PROCNAME(proc_name)
        proc_real_name = self.PROCNAME(proc_name)
        if 'MGW' in proc_real_name:
            chk_proc_cmd = 'pidof ' + self.PROCNAME(proc_name) + '.bin'
        else:
            chk_proc_cmd = 'pidof ' + self.PROCNAME(proc_name)


        try:
            if self.excute_cmd(host_ip,chk_proc_cmd):
                return True
            else:
                return False
        except Exception,e:
            print 'Excuting function <check_proc_id> ERROR!!\nERROR MSG:%s' % (e)
            return False

    def check_proc_telnet(self,proc_name):
        host_ip = self.IP(proc_name)
        tn_port = self.PORT(proc_name)
        tmpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tmpSocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        try:
            tmpSocket.connect((host_ip,int(tn_port)))
            tmpSocket.close()
            return True
        except Exception,e:
            # print 'Excuting function <check_proc_telnet> ERROR!!\nERROR MSG: checking %s in %s %s %s' % (proc_name,host_ip,tn_port,e)
            return False

    # def check_telnet_port_on(self,host_ip,tn_port):
    #     try:
    #         tn = telnetlib.Telnet(host_ip,tn_port)
    #         tn.close()
    #         return True
    #     except Exception,e:
    #         print 'Excuting function <check_telnet_port_on> ERROR!!\nERROR MSG:%s' % (e)
    #         return False

    def stop_proc(self,proc_name_list):
        proc_list = proc_name_list
        proc_cfg = read_proc_cfg(ServerCfgFile)

        for proc_name in proc_list:
            check_proc_result = self.check_proc_id(proc_name)
            check_proc_port = self.check_proc_telnet(proc_name)
            if not ( check_proc_result and check_proc_port ):
                    print "\033[0;31;40m %s \033[0m %s 进程不存在,无法对其进行关闭!" % (self.NICK_NAME,proc_name)
                    self.RESULT = False
                    return False
            else:
                print "%s 进程检查通过" % proc_name

        for proc_name in proc_list:
            proc_ip = self.IP(proc_name)
            proc_port = self.PORT(proc_name)
            shutdown_cmd = 'cmd.shutdown()'
            if 'GS' in proc_name:
                if not self.excute_telnet_cmd(proc_ip,proc_port,shutdown_cmd):
                    self.RESULT = False
                    return False

        for proc_name in proc_list:
            proc_log = proc_cfg.get_proc_logfile(proc_name,self.GAME_GROUP)
            proc_path = proc_cfg.get_proc_path(proc_name,self.GAME_GROUP)
            proc_log_path = proc_path + '/' + proc_log
            proc_ip = self.IP(proc_name)
            proc_port = self.PORT(proc_name)
            proc_real_name = self.PROCNAME(proc_name)

            if proc_name == 'SCS':
                shutdown_cmd = 'kill -9 `pidof ' + proc_real_name + '`'
                if self.excute_cmd(proc_ip,shutdown_cmd):
                    if not self.check_proc_id(proc_name):
                        print "%s %s 进程关闭成功！" % (self.NICK_NAME,proc_real_name)
                        continue
                    else:
                        print "\033[0;31;40m %s \033[0m %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                        self.RESULT = False
                        return False
                else:
                    print "\033[0;31;40m %s \033[0m %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                    self.RESULT = False
                    return False

			#20151019山竹增加关闭MGW1的进程
            if proc_name == 'MGW1':
                shutdown_cmd = 'kill -9 `pidof ' + proc_real_name + '.bin`' 
                if self.excute_cmd(proc_ip,shutdown_cmd):
                    if not self.check_proc_id(proc_name):
                        print "%s %s 进程关闭成功！" % (self.NICK_NAME,proc_real_name)
                        continue
                    else:
                        print "\033[0;31;40m %s \033[0m %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                        self.RESULT = False
                        return False
                else:
                    print  "\033[0;31;40m %s \033[0m %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                    self.RESULT = False
                    return False

            stop_telnet_cmd = 'cmd.shutdown()'
            if 'GS' in proc_name:
                key_word = 'Finish Saving Player Data'
            elif 'LS' in proc_name:
                key_word = '.*'
            else:
                key_word = 'STOP COMPLETED'

            if not self.excute_telnet_cmd(proc_ip,proc_port,stop_telnet_cmd):
                print "\033[0;31;40m %s \033[0m %s 进程命令执行失败!" % (self.NICK_NAME,proc_real_name)
                self.RESULT =False
                return False

            result = self.check_keyword(proc_ip,proc_log_path,key_word,Timeout=330)
            if result:
                print "%s %s 进程关闭成功！" % (self.NICK_NAME,proc_real_name)
                continue
            else:
                print "\033[0;31;40m %s \033[0m %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                self.RESULT =False
                return False

        self.RESULT = True
        return True

    def start_proc(self,proc_name_list):
        proc_list = proc_name_list
        proc_cfg = read_proc_cfg(ServerCfgFile)

        for proc_name in proc_list:
            check_proc_result = self.check_proc_id(proc_name)
            check_proc_port = self.check_proc_telnet(proc_name)
            if check_proc_result or check_proc_port :
                    print "%s 进程可能存在,无法对其进行开启!" % proc_name
                    self.RESULT = False
                    return False
            else:
                print "%s 进程检查通过" % proc_name

        for proc_name in proc_list:
            proc_log = proc_cfg.get_proc_logfile(proc_name,self.GAME_GROUP)
            proc_path = proc_cfg.get_proc_path(proc_name,self.GAME_GROUP)
            proc_log_path = proc_path + '/' + proc_log
            proc_ip = self.IP(proc_name)
            proc_shell = proc_cfg.get_proc_shell(proc_name,self.GAME_GROUP)
            proc_real_name = self.PROCNAME(proc_name)
            start_cmd = 'cd ' + proc_path + '; ' + proc_shell

            # print "is going to start %s" % proc_name

            if 'GS' in proc_name:
                fail_keyword = 'starting failed'
                if not self.excute_cmd(proc_ip,start_cmd):
                    print "%s %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                    self.RESUTL = False
                    return False
                else:
                    result = self.check_keyword(proc_ip,proc_log_path,fail_keyword,word_count=1,Timeout=1)
                    if result:
                        print "%s %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                        self.RESULT = False
                        return False
                    else:
                        print "%s %s 进程开启成功！" % (self.NICK_NAME,proc_real_name)
                        continue
			#20151019增加启动MGW1进程过程
            elif 'MGW' in proc_name:
                pass_keyword = "vs register succeded"
                if not self.excute_cmd(proc_ip,start_cmd):
                    print "%s %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                    self.RESULT = False
                    return False
                else:
                    result = self.check_keyword(proc_ip,proc_log_path,fail_keyword,word_count=1,Timeout=1)
                    if result:
                        print "%s %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                        self.RESULT = False
                        return False
                    else:
                        print "%s %s 进程开启成功！" % (self.NICK_NAME,proc_real_name)
                        continue

            else:
                pass_keyword = 'STARTUP COMPLETED'
                fail_keyword = 'starting failed'
                pass_count = 1

                if 'BLOB' in proc_name:
                    pass_keyword = 'blob passed'
                    fail_keyword = 'blob failed'
                    fail_keyword2 = 'starting failed'

                    host_conn = self.create_ssh_conn(proc_ip)
                    if not host_conn:
                        print '不能创建连接到%s' % host_ip
                        return False
                    host_conn.logfile = open(self.LOG_FILE,'ab')

                    result_regex = re.compile('^cmd_result:(.)')
                    check_file_exist = 'cd ' + proc_path + ';' 'chmod +x ' + proc_shell 
        
                    host_conn.sendline(check_file_exist)
                    host_conn.sendline('echo "cmd_result:`echo $?`"')
                    host_conn.expect('cmd_result:')
                    tmp_line = host_conn.readline()
                    while tmp_line:
                        # print tmp_line
                        if tmp_line and result_regex.match(tmp_line):
                            excute_result = result_regex.match(tmp_line).group(1)
                            # print '#%s#' % excute_result
                            if excute_result.strip() == '0':
                                isFileExist = True
                                break
                            else:
                                isFileExist = False
                                break
                        else:
                            tmp_line = host_conn.readline()

                    if not isFileExist:
                        print '执行程序 %s;%s 无法执行' % (proc_path,proc_shell)
                        self.RESULT = False
                        return False

                    regex1 = re.compile('.*' + pass_keyword + '.*')
                    regex2 = re.compile('.*' + fail_keyword + '.*')
                    regex3 = re.compile('.*' + fail_keyword2 + '.*')
                    try:
                        Continue = True
                        while Continue:
                            host_conn.sendline(start_cmd)
                            tmp_line = host_conn.readline()
                            while tmp_line:
                                if regex1.match(tmp_line):
                                    print "%s %s 进程开启成功！" % (self.NICK_NAME,proc_real_name)
                                    host_conn.close()
                                    Continue = False
                                    break
                                elif regex2.match(tmp_line) or regex3.match(tmp_line):
                                    print "%s %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                                    self.RESUTL = False
                                    host_conn.close()
                                    return False
                                else:
                                    tmp_line = host_conn.readline()
                        continue

                    except Exception,e:
                        print 'Excuting function <found_keyword> ERROR!!\nERROR MSG:%s' % (e)
                        host_conn.close()
                        return False

                if ( 'BCS' in proc_name ) and 'BCS1' not in proc_name:
                    pass_count = 3

                if not self.excute_cmd(proc_ip,start_cmd):
                    print "%s %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                    self.RESUTL = False
                    return False

                for i in range(6):
                    result = self.check_keyword(proc_ip,proc_log_path,pass_keyword,word_count=pass_count,Timeout=10)
                    if result:
                        print "%s %s 进程开启成功！" % (self.NICK_NAME,proc_real_name)
                        break
                    result = self.check_keyword(proc_ip,proc_log_path,fail_keyword,word_count=1,Timeout=5)
                    if result:
                        print "\033[0;31;40m %s \033[0m %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                        self.RESULT = False
                        return False
                if result:
                    continue
                else:
                    print "\033[0;31;40m %s \033[0m %s 进程执行失败!" % (self.NICK_NAME,proc_real_name)
                    self.RESULT = False
                    return False

        self.RESULT = True
        return True
    ##################################################################
    # options:
    # 'mv': 移除备份 , 'cp': 拷贝备份
    #################################################################
    def backup_mod(self,machine_list,option='mv'):
        for mc in machine_list:
            if option.strip() == 'mv':
                backup_cmd = "sh /mnt/script/backup_by_mv.sh " + getattr(self,'HOME_PATH') + ' ' + mc + ' ' + self.GAME_GROUP
            elif option.strip() == 'cp':
                backup_cmd = "sh /mnt/script/backup_by_cp.sh " + getattr(self,'HOME_PATH') + ' ' + mc + ' ' + self.GAME_GROUP

            if not self.excute_cmd(getattr(self,mc+"_IP"),backup_cmd):
                print "%s %s备份模块执行失败!" % (self.NICK_NAME,mc)
                self.RESULT = False
                return False

        self.RESULT = True
        return True

    ##################################################################
    # 函数 : 拷贝模块
    #
    #################################################################
    def cp_mod(self,machine_list):
        for mc in machine_list:
            update_cmd = 'sh /mnt/script/update_mod_by_cp.sh ' + mc + ' ' + self.GAME_GROUP
            if not self.excute_cmd(getattr(self,mc+"_IP"),update_cmd):
                print "%s %s拷贝模块执行失败!" % (self.NICK_NAME,mc)
                self.RESULT = False
                return False

        self.RESULT = True
        return True



# print 'fuck####################################################'
# svr1 = read_gamegroup_cfg('../../etc/gamegroup.cfg')
# server1 = init_server(svr1.get_svr_info_by_name('weiduan'))
# server1.stop_proc('SCS')
# server1.start_proc('BLOB')
# server1.check_firewall()
# server1.set_firewall(0)
# print server1.PATH('LS')
# server1.upload_file('/home/omadmin/kaola/develop/modules/testfile','192.168.242.11','/home/omadmin')
# server1.download_file('/home/omadmin/kaola/develop/modules/sadf','192.168.242.11','/home/omadmin/testfile')
# print server1.check_keyword('192.168.242.11','/home/AA_server/GS1/gs.log','Finish Saving Player Data',1,10)
# print server1.check_proc_id('LS')
# print server1.check_proc_telnet('GS16')

# print server1.excute_telnet_cmd('192.168.223.51','9915','cmd.ls()')


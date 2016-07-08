#!/usr/bin/python
#-*- coding: utf-8 -*-

import re

# read the configuretion from server.cfg
class read_proc_cfg:
    def __init__(self,cfg_filename):
        self.__proc_info = []
        note = re.compile('^[ |\t]*#') # grep the  note (#.....)
        blank = re.compile('^$') # grep the  note (#.....)
        f = open(cfg_filename)
        while 1:
            cfg_line = f.readline()
            if not cfg_line:
                break
            if not (note.match(cfg_line) or blank.match(cfg_line)):
                self.__proc_info.append(cfg_line.strip('\n').split(','))
        f.close()
    
    def get_all_proc_info(self):
        return self.__proc_info

    def get_all_proc_name(self,gamegroup):
        proc_name = []
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0:
                proc_name.append(self.__proc_info[i][0].strip())
        return proc_name

    def get_proc_ipaddr(self,proc_name,gamegroup):
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0 and cmp(self.__proc_info[i][0].strip(),proc_name.strip()) == 0:
                    return self.__proc_info[i][4].strip()
        return None

    def get_proc_path(self,proc_name,gamegroup):
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0 and cmp(self.__proc_info[i][0].strip(),proc_name.strip()) == 0:
                return self.__proc_info[i][5].strip()
        return None

    def get_proc_shell(self,proc_name,gamegroup):
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0 and cmp(self.__proc_info[i][0].strip(),proc_name.strip()) == 0:
                return self.__proc_info[i][6].strip()
        return None

    def get_proc_logfile(self,proc_name,gamegroup):
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0 and cmp(self.__proc_info[i][0].strip(),proc_name.strip()) == 0:
                return self.__proc_info[i][7].strip()
        return None

    def get_proc_telnet_port(self,proc_name,gamegroup):
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0 and cmp(self.__proc_info[i][0].strip(),proc_name.strip()) == 0:
                return self.__proc_info[i][8].strip()
        return None

    def get_machine_proc(self,machine_name,gamegroup):
        proc_name = []
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0 and cmp(self.__proc_info[i][3].strip(),machine_name.strip()) == 0:
                proc_name.append(self.__proc_info[i][0].strip())
        return proc_name

    def get_machine_ip(self,machine_name,gamegroup):
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0 and cmp(self.__proc_info[i][3].strip(),machine_name.strip()) == 0:
                return self.__proc_info[i][4].strip()
        return None

    def get_real_proc_name(self,proc_name,gamegroup):
        for i in range(len(self.__proc_info)):
            if cmp(self.__proc_info[i][1].strip(),str(gamegroup).strip()) == 0 and cmp(self.__proc_info[i][0].strip(),proc_name.strip()) == 0:
                return self.__proc_info[i][2].strip()
        return None


# print "######################################################"
# proc1 = read_proc_cfg('../../etc/proc.cfg')
# print proc1.get_proc_ipaddr('LS',1)
# print proc1.get_all_proc_name(1)
# print proc1.get_all_proc_info()
# print proc1.get_proc_ipaddr('GS1',1)
# print proc1.get_proc_path('GS1',1)
# print proc1.get_proc_shell('GS1',1)
# print proc1.get_proc_logfile('GS1',1)
# print proc1.get_proc_telnet_port('GS1',1)
# print proc1.get_machine_proc('GS1',1)
# print proc1.get_machine_ip('GS1',1)
# print proc1.get_real_proc_name('GS2',1)
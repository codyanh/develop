#!/usr/bin/python
#-*- coding: utf-8 -*-
import re

# the <read_gamegroup_cfg> will read the configuretions from the config file you given
# to protect the running process from others
class read_gamegroup_cfg:
    __max_server = 100  # the max num of server
    __current_server_num = 0 # the current num of server
    def __init__(self,cfg_filename):
        self.__server_info = []     # all the server infomation from gamegroup.cfg
        note = re.compile('^[ |\t]*#') # grep the  note (#.....)
        blank = re.compile('^$') # grep the  note (#.....)
        f = open(cfg_filename)
        while 1:
            cfg_line = f.readline()
            if not cfg_line:
                break
            if not (note.match(cfg_line) or blank.match(cfg_line)): # save the server infomation to <__server_info> list 
                if self.__current_server_num <= self.__max_server:
                    self.__server_info.append(cfg_line.rstrip('\n').split(','))
                else:
                    print 'current server is out of the max_num!'
                    break
                self.__current_server_num += 1
        f.close()
    
    def get_all_svr_info(self): # return all the server infomation
        return self.__server_info

    def get_all_svr_name(self): # return all the server name in <__server_info>
        tmp_svr_name_list = []
        for i in range(len(self.__server_info)):
            tmp_svr_name_list.append(self.__server_info[i][0].strip())
        return tmp_svr_name_list

    def get_svr_info_by_name(self,svr_name): # return the server infomation which you want , by using the <svr_name>, example:get_svr_info_by_name('xiangyu')
        for i in range(len(self.__server_info)):
            if cmp(self.__server_info[i][0].strip(),svr_name) == 0:
                    return  self.__server_info[i]
        return None

    def get_current_svr_num(self): # keep an account of server_info 
        return self.__current_server_num

# print "######################################################"
# svr1 = read_gamegroup_cfg('../../etc/gamegroup.cfg')
# print svr1.get_all_svr_info()
# print svr1.get_all_svr_name()
# print svr1.get_svr_info_by_name('huihuang')
# print svr1.get_current_svr_num()
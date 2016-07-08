#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import threading
import sys
import time
sys.path.append("./lib")
from show_meun import *
from read_gamegroup_cfg import *
from read_proc_cfg import *
from server_method import *

import re
import time
import commands
import pexpect
import pxssh
import getpass



GameGroupCfgFile = "../etc/gamegroup.cfg"
ServerCfgFile = "../etc/proc.cfg"

##############################
# 函数名  : 排列进程
# 开关    : 
# option : 	1 按开启进程排序
# 			0 按关闭进程排序

def Proc_sort(proc_list,option):
	proc_list_on = ['SCS', 'BLOB', 'DBS', 'DBM', 'CCS', 'LS', 'GS1', 'GS2', 'GS3', 'GS4', 'GS5', 'GS6', 'GS7', 'GS8', 'GS9', 'GS10', 'GS11', 'GS12', 'GS13', 'GS14', 'GS15', 'GS16','BCS1', 'BCS2', 'BCS3', 'BCS4', 'BCS5', 'BCS6', 'MGW1']
	proc_list_off = ['GS1', 'GS2', 'GS3', 'GS4', 'GS5', 'GS6', 'GS7', 'GS8', 'GS9', 'GS10', 'GS11', 'GS12', 'GS13', 'GS14', 'GS15', 'GS16', 'BCS1', 'BCS2', 'BCS3', 'BCS4', 'BCS5','BCS6', 'LS', 'CCS', 'DBS', 'DBM', 'BLOB', 'SCS', 'MGW1']
	if option == 1:
		sort_result = proc_list_on
	elif option == 0:
		sort_result = proc_list_off
	if option not in [0,1]:
		return False

	tmp_list = sort_result[:]
	for tmp_cho in tmp_list:
		if tmp_cho not in proc_list:
			sort_result.remove(tmp_cho)
		
	return sort_result

##############################

	
SVR_CFG = read_gamegroup_cfg(GameGroupCfgFile)
PROC_CFG = read_proc_cfg(ServerCfgFile)
Meun = meun()

def Main():
	#########################
	# a  : 例行维护
	# b  : 动态更新相关
	# q  : 退出
	#########################
	while 1:
		choose = ''
		choose = Meun.Main_meun()
		if choose == 'a':
			MaintainJob()
		elif choose == 'b':
			DailyJob()
		elif choose == 'c':
			CDNJob()
		elif choose == 'd':
			WeiDuanJob()
		elif choose == 'q':
			exit(0)

def MaintainJob():
	#########################
	# a  : 上传版本
	# b  : 防火墙设置
	# c  : 关闭服务
	# d  : 备份模块
	# e  : 备份数据库
	# f  : 拷贝模块
	# g  : 优化数据库
	# h  : 启动服务
	# q  : 返回
	#########################

	choose = Meun.Maintain_meun()

	######################################################## 上传版本 ########################################################
	if choose == 'a':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False

		upload_file = raw_input('输入你要上传的版本:\n>>>')
		if not os.path.exists(upload_file):
			print '错误的文件路径!'
			return False

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return True
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			while threading.activeCount() > 11:
				# print 'current threading count: %d' % threading.activeCount()
				# print threading.enumerate()
				time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			upload_path = svr_obj.UPLOAD_PATH
			upload_host = getattr(svr_obj,'GSBAK_IP')
			# svr_obj.LOG_FILE = os.path.join('../log/'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt')
			svr_obj.LOG_FILE = '../log/upload_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始上传... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)
			threading.Thread(target=svr_obj.upload_file,args=(upload_file,upload_host,upload_path)).start()
			time.sleep(1)
			
		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		for svr_obj in svr_obj_list:
			if not svr_obj.RESULT:
				print '\033[0;31;40m %s \033[0m 上传版本出错了!' % svr.NICK_NAME
				continue
			#print svr_obj.GAME_GROUP
			if svr_obj.excute_upload_cmd(svr_obj.GSBAK_IP,'cd /mnt/script; ./upload.sh `basename '+upload_file+'` '+svr_obj.GAME_GROUP):
				svr_obj.RESULT = True
			else:
				svr_obj.RESULT = False

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True

	######################################################## 开关防火墙 ######################################################	

	if choose == 'b':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False
		fw_choose = raw_input('fw_on : 允许玩家进入\nfw_off : 拒绝玩家进入\n请输入 [ fw_on fw_off ] >>>').strip()
		if fw_choose not in ['fw_on','fw_off']:
			print '错误的选择!'
			return False

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return True
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)

			svr_obj.LOG_FILE = '../log/firewall_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m正在操作... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			chk_fw_result = svr_obj.check_firewall()
			if fw_choose == 'fw_on':
				if not chk_fw_result :
					threading.Thread(target=svr_obj.set_firewall,args=(1,)).start()
				else:
					svr_obj.RESULT = False
					print '%s 防火墙已经打开了，请勿重复操作！' % svr_obj.NICK_NAME

			if fw_choose == 'fw_off':
				if chk_fw_result :
					threading.Thread(target=svr_obj.set_firewall,args=(0,)).start()
				else:
					svr_obj.RESULT = False
					print '%s 防火墙已经关闭了，请勿重复操作！' % svr_obj.NICK_NAME

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
 			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'
		
		return True
	######################################################## 关闭进程 ########################################################
	if choose == 'c':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False
		proc_choose = Meun.Choose_proc(0)
		if not proc_choose:
			print '错误的服务选择'
			return False

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/closeProc_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始关闭服务... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)
			
			threading.Thread(target=svr_obj.stop_proc,args=(Proc_sort(proc_choose,0),)).start()
			time.sleep(1)

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	######################################################## 备份模块 ########################################################
	if choose == 'd':
		svr_obj_list = []

		backup_opt = raw_input('a:移除备份 b:拷贝备份\n>>>')
		if backup_opt not in ['a','b']:
			print '错误的选择！'
			return False
		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False
		mc_choose = Meun.Choose_machine()
		if not mc_choose:
			print '错误的机器选择'
			return False

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 11:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/backupMod_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始备份模块... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			if backup_opt == 'a':
				threading.Thread(target=svr_obj.backup_mod,args=(mc_choose,'mv')).start()
				time.sleep(1)
			else:
				threading.Thread(target=svr_obj.backup_mod,args=(mc_choose,'cp')).start()
				time.sleep(1)

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True

	######################################################## 备份数据库 ########################################################

	if choose == 'e':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False
		# db_choose = Meun.Choose_database()
		# if not db_choose:
		# 	print '错误的服务器选择'
		# 	return False

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/backupDB_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始备份数据库... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			if svr_obj.GAME_GROUP == "21":
				backupdb_cmd = 'mysqldump --default-character-set=latin1 --opt -umysqlbak -pmysqlbakom1c2b -h172.16.0.3 -P3306 '\
							+ 'a_game' + '>~/' + 'agame' + '_'+ svr_obj.SERVER_NAME + '_`date +%Y%m%d_%H%M%S`.sql'
			elif svr_obj.GAME_GROUP == "22":
				backupdb_cmd = 'mysqldump --default-character-set=latin1 --opt -umysqlbak -pmysqlbakom1c2b -h172.16.0.3 -P3306 '\
							+ 'a_game2' + '>~/' + 'agame2' + '_'+ svr_obj.SERVER_NAME + '_`date +%Y%m%d_%H%M%S`.sql'
			elif svr_obj.GAME_GROUP == "23":
				backupdb_cmd = 'mysqldump --default-character-set=latin1 --opt -umysqlbak -pmysqlbakom1c2b -h172.16.0.3 -P3306 '\
							+ 'a_game3' + '>~/' + 'agame3' + '_'+ svr_obj.SERVER_NAME + '_`date +%Y%m%d_%H%M%S`.sql'
			elif svr_obj.GAME_GROUP == "24":
				backupdb_cmd = 'mysqldump --default-character-set=latin1 --opt -umysqlbak -pmysqlbakom1c2b -h172.16.0.3 -P3306 '\
							+ 'a_game4' + '>~/' + 'agame4' + '_'+ svr_obj.SERVER_NAME + '_`date +%Y%m%d_%H%M%S`.sql'
			elif svr_obj.GAME_GROUP == "25":
				backupdb_cmd = 'mysqldump --default-character-set=latin1 --opt -umysqlbak -pmysqlbakom1c2b -h172.16.0.3 -P3306 '\
							+ 'a_game5' + '>~/' + 'agame5' + '_'+ svr_obj.SERVER_NAME + '_`date +%Y%m%d_%H%M%S`.sql'
			else:
				backupdb_cmd = 'mysqldump --default-character-set=latin1 --opt --flush-logs -umysqlbak -pmysqlbakom1c2b -h127.0.0.1 -P3306 '\
							+ 'a_game' + '>~/' + 'agame' + '_'+ svr_obj.SERVER_NAME + '_`date +%Y%m%d_%H%M%S`.sql'

			threading.Thread(target=svr_obj.excute_cmd,args=(getattr(svr_obj,'GDB_IP'),backupdb_cmd)).start()
			time.sleep(1)


		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'
		
		return True
	######################################################## 拷贝模块 ########################################################
	if choose == 'f':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False
		mc_choose = Meun.Choose_machine()
		if not mc_choose:
			print '错误的服务器选择'
			return False

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		print "执行中..."
		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/copyMod_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始拷贝模块... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			threading.Thread(target=svr_obj.cp_mod,args=(mc_choose,)).start()
			time.sleep(1)

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	######################################################## 优化数据库 ########################################################
# 	if choose == 'g':
# 		print '不好意思！暂时没有这个需要！'
# 		return False
 	if choose == 'g':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False
#		dbop_choose = Meun.Choose_proc(1)
#		if not dbop_choose:
#			print '错误的服务选择'
#			return False

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/optimize_DB_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始优化数据库... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			optimizedb_cmd = 'mysql -umysqlbak -pmysqlbakom1c2b -h127.0.0.1 -P3306 a_game -e "optimize table player"'
			threading.Thread(target=svr_obj.excute_cmd,args=(getattr(svr_obj,'GDB_IP'),optimizedb_cmd)).start()
			time.sleep(1)


		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'
		
		return True

	######################################################## 开启进程 ########################################################
	if choose == 'h':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False
		proc_choose = Meun.Choose_proc(1)
		if not proc_choose:
			print '错误的服务选择'
			return False

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/startProc_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始开启服务... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)
			
			threading.Thread(target=svr_obj.start_proc,args=(Proc_sort(proc_choose,1),)).start()
			time.sleep(1)

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	########################################################
	if choose == 'q':
		return True
	########################################################












def DailyJob():
	#########################
	# a  : 上传文件
	# b  : 执行动态更新
	# c  : 下载文件
	# q  : 返回
	#########################

	choose = Meun.Daily_meun()
	######################################################## 上传文件 ########################################################
	if choose == 'a':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False

		upload_file = raw_input('输入你要上传的文件:\n')
		if not os.path.exists(upload_file):
			print '错误的文件路径!'
			return False

		proc_choose = Meun.Choose_proc(1)
		if not proc_choose:
			print '错误的上传进程路径'
			return False

		upload_path = raw_input('请输入你要上传的相对路径，如果是要上传的是进程根目录，请直接回车\n例[\'log/modules/\']\n>>>')
		if not upload_path:
			upload_path = upload_path.rstrip('/') + '/'

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			while threading.activeCount() > 11:
				time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/upload_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始上传... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			threading.Thread(target=svr_obj.multiple_upload_file,args=(upload_file,upload_path,proc_choose)).start()
			time.sleep(1)
			
		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	######################################################## 动态更新 ########################################################
	if choose == 'b':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False
		proc_choose = Meun.Choose_proc(1)
		if not proc_choose:
			print '错误的服务选择'
			return False
		cmd_choose = raw_input('请输入要执行的命令\n>>>')
		if not cmd_choose:
			print '错误的命令'
			return False
		# cmd_choose = repr(cmd_choose)

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 11:
			# 	time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/telnet_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始执行telnet命令... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			threading.Thread(target=svr_obj.multiple_excute_telnet_cmd,args=(proc_choose,cmd_choose)).start()
			time.sleep(1)
			
		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	######################################################## 下载文件 ########################################################
	if choose == 'c':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '错误的服务器选择'
			return False

		proc_choose = Meun.Choose_proc(1)
		if not proc_choose:
			print '错误的下载进程'
			return False

		download_path = raw_input('请输入你要下载的相对路径，\n例[\'log/*.log\']\n>>>')

		excu_choose = raw_input('确定要执行吗?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '错误的选择！'
			return False
		else:
			pass

		for svr in svr_choose:
			while threading.activeCount() > 11:
				time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/download_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m开始下载... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			threading.Thread(target=svr_obj.multiple_download_file,args=(download_path,proc_choose)).start()
			time.sleep(1)
	
		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########下面的服执行成功啦！############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########下面的服执行失败啦！############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True

	########################################################
	if choose == 'q':
		return True
	########################################################


def CDNJob():
	#########################
	# a : 第一步:下载并修改patch_list.xml,并上传补丁包文件
	# b : 第二步:推送patch_list.xml
	# c : 第三步:推送server_list.xml
	#########################

	choose = Meun.CDN_meun()
	########################################## 下载并修改patch_list.xml,并上传补丁包文件 ########################################
	if choose == 'a':
		PATCH_LOG_FILE= '../log/cdnpushlog/uploadpatchfiles_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+'_log.txt'


		print "##################################################################################################"
		print '#请将所有的patch.sy , patch.exe , depatch.sy , depatch.exe , patch.sy.md5.txt , depatch.sy.md5.txt'
		print '#放到 ../cdnpush/patchfile/ 目录下面去, 否则要出错哦~'

		make_patchlist_cmd = 'cd ../cdnpush/ ; ./make_patchlist.sh'
		print '#首先,将执行生成新的patch_list.xml 命令: %s' % make_patchlist_cmd
		print '#生成的patch_list.xml : ../cdnpush/patch_list.xml_ws(patch_list.xml_lx)'
		print "##################################################################################################"
		continue_choose = raw_input('确定放好了?继续?[ yes 或者任意键中断操作 ]\n>>>')
		if continue_choose.strip() != 'yes':
			return False
		os.system("touch "+PATCH_LOG_FILE+";"+make_patchlist_cmd+" | tee "+PATCH_LOG_FILE)

		
		upload_patchfile_cmd = 'cd ../cdnpush/ ; ./upload_patchfile.py'
		print '然后,将执行上传补丁包 命令: %s' % upload_patchfile_cmd
		continue_choose = raw_input('生成完了,继续上传补丁包?[ yes 或者任意键中断操作 ]\n>>>')
		if continue_choose.strip() != 'yes':
			return False
		os.system(upload_patchfile_cmd+" | tee "+PATCH_LOG_FILE)
		
		print "##################################################################################################"
		print '#是否完全分发完,请打开 网宿后台-->内容管理-->大文件系统-->任务查询 进行查看'
		print '#                      蓝汛的打开fds4.exe 工具查看是否已经 可服务 状态'
		print "##################################################################################################"

		return True

	########################################## 推送patch_list.xml ########################################
	if choose == 'b':
		PUSH_PATCH_LIST_LOG_FILE= '../log/cdnpushlog/uploadpatch_list_xml_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+'_log.txt'
			
		print "##################################################################################################"
		print '#请确保patch_list.xml内容正确 : ../cdnpush/patch_list.xml_ws(patch_list.xml_lx)'
		
		push_patchlist_cmd = 'cd ../cdnpush/ ; ./lz_cdnpush_patchlist.sh'
		print '#将执行推送patch_list 命令: %s' % push_patchlist_cmd
		print "##################################################################################################"

		continue_choose = raw_input('检查完了?继续?[ yes 或者任意键中断操作 ]\n>>>')
		if continue_choose.strip() != 'yes':
			return False
		os.system("touch "+PUSH_PATCH_LIST_LOG_FILE+";"+push_patchlist_cmd+" | tee "+PUSH_PATCH_LIST_LOG_FILE)

		print "##################################################################################################"
		print '#请到网宿相应的后台查询是否完全分发完成'
		print "##################################################################################################"
		return True

	########################################## 推送server_list.xml ########################################
	if choose == 'c':
		PUSH_SERVER_LIST_LOG_FILE= '../log/cdnpushlog/uploadserver_list_xml_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+'_log.txt'
		
		print "##################################################################################################"
		print "#需要从现网下载一份新的server_list.xml下来吗？"

		download_serverlist_cmd = "cd ../cdnpush/ ; wget -N http://172.19.0.90/agame/update/server_list.xml"
		print '#将执行下载server_list 命令: %s' % download_serverlist_cmd
		print "#下载完了请瞅这 : more ../cdnpush/server_list.xml "
		print "##################################################################################################"
		download_choose = raw_input('需要吗？[ yes 或者任意键跳过此操作 ]\n>>>')
		if download_choose.strip() == 'yes':
			os.system("touch "+PUSH_SERVER_LIST_LOG_FILE+";"+download_serverlist_cmd+" | tee "+PUSH_SERVER_LIST_LOG_FILE)

		print "##################################################################################################"
		print '#请确保server_list.xml内容正确 : ../cdnpush/server_list.xml'

		push_serverlist_cmd = 'cd ../cdnpush/ ; ./lz_cdnpush_serverlist.sh server_list.xml'
		print '#将执行推送server_list 命令: %s' % push_serverlist_cmd
		print '''#你也可以手动执行或者定时操作: "cd ../cdnpush/ ; ./lz_cdnpush_serverlist.sh <serverlist文件>" '''
		print "##################################################################################################"

		continue_choose = raw_input('检查完了?继续?[ yes 或者任意键中断操作 ]\n>>>')
		if continue_choose.strip() != 'yes':
			return False
		os.system(push_serverlist_cmd+" | tee "+PUSH_SERVER_LIST_LOG_FILE)

		print "##################################################################################################"
		print '#请到网宿相应的后台查询是否完全分发完成'
		print "##################################################################################################"

		return True

	########################################################
	if choose == 'q':
		return True
	########################################################

#20151028山竹添加微端资源推送模块
def WeiDuanJob():
	#################################################
	#  a : 微端资源推送
	#  b : 微端下载器推送
	#
	#################################################
	
	choose = Meun.WeiDuan_meun()

	#print "choose:"+choose
	########################################################微端资源##############################################
	if choose == 'a':
		UPLOAD_LOG_FILE= '../log/wdupdate_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+'_log.txt'
		print "###################################################################################"
		print "#接下来将到ftp://192.168.10.123/aplan/上下载微端资源"
		print "#下载好的微端资源将保存在../cdnpush/wdupdatefile中"
		print "#本次微端资源上传操作的日志文件为:"+UPLOAD_LOG_FILE
		mail_weiduan_download_url = raw_input(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>请输入本次邮件中微端资源的URL链接：")
		weiduan_download_folder = mail_weiduan_download_url.replace('ftp://192.168.4.1/','')
		weiduan_download = weiduan_download_folder.strip()
		#######################处理微端版本######
		weiduan_download_split = weiduan_download.split('/')
		weiduan_download_part2 = weiduan_download_split[1]
		weiduan_download_number = weiduan_download_part2[7:13]
		weiduan_download_nomal = weiduan_download_number[0]+'.'+weiduan_download_number[1:3]+'.'+weiduan_download_number[3:6]

		#########################################

		print "\n\n请确认此次微端的版本号："+ weiduan_download_nomal
		print "\n\n请确认邮件的微端资源位置为：ftp://192.168.4.1/"+ weiduan_download

		continue_choose = raw_input('\n与邮件的微端资源位置一样吗？【yes继续执行  或者  任意其他键返回上一层  】>>>>>>>>>>>')
		
		if continue_choose.strip() == 'yes':
			pass
		else:
			return False


		#######################################打开日志文件####################################
		f=open(UPLOAD_LOG_FILE,'a+')


		
		cmd_download_weiduan='cd ../cdnpush/wdupdatefile/ ; wget --ftp-user=om --ftp-password=D6ollHZyIVRCg ftp://192.168.10.123/aplan/'+weiduan_download
		download_weiduan_result=os.system(cmd_download_weiduan)
		result_float2str=str(download_weiduan_result)
		result='下载微端资源的结果为：'+result_float2str+'\n'
		f.write(result)


		download_wdver_result=os.system('cd ../cdnpush/wdupdatefile/ ;wget -N http://192.168.30.21/agame/update/wdver_list.xml')
		result_float2str=str(download_wdver_result)
		result='下载wdver_list.xml的结果为：'+result_float2str+'\n'
		f.write(result)

		
		f.close()
		####################接下来的代码是处理wdver_list.xml,对该文件作出更新#############################
        

		count = len(open(r"../cdnpush/wdupdatefile/wdver_list.xml",'rU').readlines())

		count = count - 2
		
		content = '     <version ver="'+ weiduan_download_nomal +'"/>'

		fp = open('../cdnpush/wdupdatefile/wdver_list.xml','rU')
		s = fp.read()
		fp.flush()
		fp.close()
		a = s.split('\n')
		a.insert(count, content) 
		s = '\n'.join(a)
		fp = open('../cdnpush/wdupdatefile/wdver_list.xml', 'w')
		fp.write(s)
		fp.flush()
		fp.close()

		#######################修改wdver_list.xml文件处理完成##########################################
		
		######################md5sum######################################################
		re_md5sum = re.compile(' ')
		weiduan_md5sum_pre = commands.getoutput('md5sum ../cdnpush/wdupdatefile/'+weiduan_download_part2)
		weiduan_md5sum_1 = re_md5sum.split(weiduan_md5sum_pre)
		md5sum_weiduan_1 = weiduan_md5sum_1[0]
		
		wdver_md5sum_pre = commands.getoutput('md5sum ../cdnpush/wdupdatefile/wdver_list.xml')
		wdver_md5sum_1 = re_md5sum.split(wdver_md5sum_pre)
		md5sum_wdver_1 = wdver_md5sum_1[0]

		######################上面的为未上传的md5sum码##############################################
		
		UPLOAD_WEIDUAN_DIR='../cdnpush/wdupdatefile/'

		UPLOAD_WEIDUAN_FILE=os.popen('ls %s | grep -v xml'% UPLOAD_WEIDUAN_DIR).readlines()
	
		if not UPLOAD_WEIDUAN_FILE:
			print "%s has nothing!!Please exit the script and try again!" % UPLOAD_WEIDUAN_DIR
			return False
		UPLOAD_WDVER_LIST_FILE ='wdver_list.xml'

		###########################################到CDN_new1和DuanYou_CDN1上备份wdver_list.xml
		
		try:
			re_cp_ssh = re.compile(r'[\n]')

			s = pxssh.pxssh()
			CDN_new1_ip = '192.168.30.21'
			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(CDN_new1_ip, username, password)
			
			s.logfile = open(UPLOAD_LOG_FILE,'a+')

			s.sendline("cp /home/agame/update/wdver_list.xml /home/agame/update/wdver_list.xml`date +%Y%m%d%H%M%S`;echo RESULT:$? | awk -F ':' '{print $2}'")
			s.prompt()

			result_pre = s.before
			result_ed = re_cp_ssh.split(result_pre)
			result_after = result_ed[1]

			result = int(result_after)

			#print result
			
			if result != 0:
				print "\n在CDN_new1上备份wdver_list.xml的时候出错了。。。请重新开始"
				return False
			s.logout()

		except Exception, e:
			print '远程连接到CDN_new1上备份wdver_list.xml的过程中，远程连接未能建立！'
			print e
			return False

		try:
			re_cp_ssh = re.compile(r'[\n]')
			s = pxssh.pxssh()
			DuanYou_CDN1_ip = '172.19.0.90'
			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(DuanYou_CDN1_ip, username, password)


			s.logfile = open(UPLOAD_LOG_FILE,'a+')

			s.sendline("cp /home/agame/update/wdver_list.xml /home/agame/update/wdver_list.xml`date +%Y%m%d%H%M%S`;echo RESULT:$? | awk -F ':' '{print $2}'")

			s.prompt()

			result_pre = s.before
			result_ed = re_cp_ssh.split(result_pre)
			result_after = result_ed[1]

			result = int(result_after)
			
			if result != 0:
				print "\n在DuanYou_CDN1上备份wdver_list.xml的时候出错了。。。请重新开始"
				return False
			s.logout()

		except Exception, e:
			print '远程连接到DuanYou_CDN1上备份wdver_list.xml的过程中，远程连接未能建立！'
			print e
			return False
			
		#################################################################################################



		####################上传微端资源和微端下载器到CDN_new1(192.168.30.21)和DuanYou_CDN1(172.19.0.90)############################################
		
		print "接下来将把微端资源和wdver_list.xml上传到CDN_new1(192.168.30.21)和DuanYou_CDN1(172.19.0.90)>>>>>>>>>>"

		print "\n上传微端资源过程较长，请耐心等待......\n"

		#result_weiduan_CND_new1 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,weiduan_download_part2.strip(), "192.168.30.21:/home/agame/update/wdupdate"))
		#result_wdver_CDN_new1 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,"wdver_list.xml", "192.168.30.21:/home/agame/update/"))
		#result_weiduan_DuanYou_CDN1 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,weiduan_download_part2.strip(), "172.19.0.90:/home/agame/update/wdupdate"))
		#result_wdver_DuanYou_CDN1 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,"wdver_list.xml", "172.19.0.90:/home/agame/update/"))

		cmd_weiduan_CDN_new1 ="../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,weiduan_download_part2.strip(), "192.168.30.21:/home/agame/update/wdupdate")

		cmd_wdver_CDN_new1 ="../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,"wdver_list.xml", "192.168.30.21:/home/agame/update/")
	
		cmd_weiduan_DuanYou_CDN1 ="../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,weiduan_download_part2.strip(), "172.19.0.90:/home/agame/update/wdupdate")
		
		cmd_wdver_DuanYou_CDN1 ="../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,"wdver_list.xml", "172.19.0.90:/home/agame/update/")


		cmd = [cmd_weiduan_CDN_new1,cmd_wdver_CDN_new1,cmd_weiduan_DuanYou_CDN1, cmd_wdver_DuanYou_CDN1]
		#cmd = [cmd_wdver_CDN_new1,cmd_wdver_DuanYou_CDN1]
		
			
		for i in range(len(cmd)):
			threading.Thread(target=commands.getstatusoutput,args=(cmd[i],)).start()
			time.sleep(1)
    

		print "上传中......请您稍等！！！！>>>>>>>>>\n"
		print "Uploading......\n"
		while threading.activeCount() != 1:
			time.sleep(1)
		
        
		print "微端资源和wdver_list.xml上传完毕......\n"

		print "上传微端资源和wdver_list.xml完毕，继续进行下一步----检验本地微端资源和wdver_list.xml的md5sum与CDN_new1&DuanYou_CDN1上文件的md5sum是否相同>>>>>>>>>>"
		
		#time.sleep(5)




		###################在10.251上测试##################################
		#conntinue_to_upload=raw_input('继续上传到remote machine吗？》》》》》》')
		
		#print "准备上传微端资源：../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,weiduan_download_part2.strip(), "192.168.30.21:/home/omadmin/shanzhu" )

		#result_weiduan_10_251 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,weiduan_download_part2.strip(), "192.168.30.21:/home/omadmin/shanzhu"))
		
		#result_weiduan_system =os.system("../modules/scp_expect.sh"+" "+ UPLOAD_WEIDUAN_DIR + weiduan_download_part2.strip() +" "+"192.168.30.21:/home/omadmin/shanzhu")

		#if result_weiduan_system !=0:
		#	print "上传"+weiduan_download_part2.strip()+"不成功！！！！"
		#else:
		#	print "上传 "+weiduan_download_part2.strip()+" 成功！！！！！"

		#if result_weiduan_10_251[0] != 0:
		#	print "upload 微端资源失败！！！"
		#else:
		#	print result_weiduan_10_251[1]

		#print "准备上传wdver_list.xml: ../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,UPLOAD_WDVER_LIST_FILE,"192.168.30.21:/home/omadmin/shanzhu")

		#result_wdver_10_251 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,UPLOAD_WDVER_LIST_FILE, "192.168.30.21:/home/omadmin/shanzhu"))

		#result_wdver_10_251 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,UPLOAD_WDVER_LIST_FILE, "192.168.30.21:/home/omadmin/shanzhu"))
	
		#result_wdver_system =os.system("../modules/scp_expect.sh"+" "+ UPLOAD_WEIDUAN_DIR + UPLOAD_WDVER_LIST_FILE +" "+"192.168.30.21:/home/omadmin/shanzhu")
		
		#if result_wdver_system !=0:
		#	print "上传"+UPLOAD_WDVER_LIST_FILE+"不成功！！！！"
		#else:
		#	print "上传 "+UPLOAD_WDVER_LIST_FILE+" 成功！！！！！"
		#if result_wdver_10_251[0] != 0:
		#	print "upload 微端下载器失败！！！"
		#else:
		#	print result_wdver_10_251[1]
		
		#os.system("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,UPLOAD_WDVER_LIST_FILE, "192.168.10.251:/home/agame/update/"))
	
		###################检验传上去的md5sum###########################################################################################################

		re_md5sum_ssh = re.compile(r'[\s\n]')
		
		CDN_new1_ip = '192.168.30.21'
		DuanYou_CDN1 = '172.19.0.90'
		
		get_weiduan_md5_cmd = 'md5sum /home/agame/update/wdupdate/'+weiduan_download_part2

		get_wdver_list_md5_cmd = 'md5sum /home/agame/update/wdver_list.xml'
		
		try:
			##############################CDN_new1	
			s = pxssh.pxssh()

			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(CDN_new1_ip, username, password)

			
			s.logfile = open(UPLOAD_LOG_FILE,'a+')
			#############################检验wdver_list.xml
			s.sendline(get_wdver_list_md5_cmd)
			s.prompt(timeout=None)
			wdver_md5sum_uploaded_pre = s.before
			wdver_md5sum_uploaded = re_md5sum_ssh.split(wdver_md5sum_uploaded_pre)
			md5sum_wdver_uploaded = wdver_md5sum_uploaded[3]
			if md5sum_wdver_1 == md5sum_wdver_uploaded:
				print 'wdver_list.xml本地与传到CDN_new1上的文件md5sum码相同\n'
			else:
				print 'wdver_list.xml本地与传到CDN_new1上的文件md5sum码不相同,请检查相关参数，重新上传\n'
				print '本地wdver_list.xml文件的md5sum码为：'+md5sum_wdver_1+'\n'
				print 'CDN_new1上的wdver_list.xml文件的md5usm码为：'+md5sum_wdver_uploaded+'\n'
				return False
			#############################检验微端资源
			s.sendline(get_weiduan_md5_cmd)
			s.prompt(timeout=None)
			weiduan_md5sum_uploaded_pre = s.before
			weiduan_md5sum_uploaded = re_md5sum_ssh.split(weiduan_md5sum_uploaded_pre)
			md5sum_weiduan_uploaded = weiduan_md5sum_uploaded[3]
            
			#print weiduan_md5sum_uploaded_pre
			#print md5sum_weiduan_uploaded
			#print md5sum_weiduan_1
            
			if md5sum_weiduan_1 == md5sum_weiduan_uploaded:
				print '本地微端资源与传到CDN_new1上的文件md5sum码相同\n'
			else:
				print '本地微端资源与传到CDN_new1上的文件md5sum码不相同,请检查相关参数，重新上传\n'
				print '本地微端资源文件的md5sum码为：'+md5sum_weiduan_1+'\n'
				print 'CDN_new1上的文件的md5sum码为：'+md5sum_weiduan_uploaded+'\n'
				return False

			s.logout()

			
			################################DuanYou_CDN1

			s = pxssh.pxssh()

			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(DuanYou_CDN1_ip, username, password)
			
			
			s.logfile = open(UPLOAD_LOG_FILE,'a+')
			#############################检验wdver_list.xml
			s.sendline(get_wdver_list_md5_cmd)
			s.prompt(timeout=None)
			wdver_md5sum_uploaded_pre = s.before
			wdver_md5sum_uploaded = re_md5sum_ssh.split(wdver_md5sum_uploaded_pre)
			md5sum_wdver_uploaded = wdver_md5sum_uploaded[3]
			if md5sum_wdver_1 == md5sum_wdver_uploaded:
				print '本地wdver_list.xml与传到DuanYou_CDN1上的文件md5sum码相同'
			else:
				print '本地wdver_list.xml与传到DuanYou_CDN1上的文件md5sum码不相同，请检查相关文件后，重新上传\n'
				print '本地wdver_list.xml文件的md5sum码为：'+md5sum_wdver_1+'\n'
				print 'DuanYou_CDN1上wdver_list.xml文件的md5sum码为：'+md5sum_wdver_uploaded+'\n'
				return False
			#############################检验微端资源
			s.sendline(get_weiduan_md5_cmd)
			s.prompt(timeout=None)
			weiduan_md5sum_uploaded_pre = s.before
			weiduan_md5sum_uploaded = re_md5sum_ssh.split(weiduan_md5sum_uploaded_pre)
			md5sum_weiduan_uploaded = weiduan_md5sum_uploaded[3]
			if md5sum_weiduan_1 == md5sum_weiduan_uploaded:
				print '本地微端资源与传到DuanYou_CDN1上的文件md5sum码相同\n'
			else:
				print '本地微端资源与传导DuanYou_CDN1上的文件md5sum码不相同，请检查相关文件后，重新上传\n'
				print '本地微端资源的文件md5sum码为：'+md5sum_weiduan_1+'\n'
				print 'DuanYou_CDN1上的微端资源文件md5sum码为：'+md5sum_weiduan_uploaded+'\n'
				return False

			s.logout()


		except Exception, e:
			print 'pxssh failed on login.'
			print str(e)

		#################以上md5sum检验正常继续下面步骤#################################################################


        ################接下来将会对微端资源创建文件夹后，解压到这个文件夹#############################################
		print '对CDN_new1和DuanYou_CDN1上的微端资源进行解压>>>>>>>>>>>>'
		
		try:
			#####################################################解压CDN_new1上的微端资源
			s = pxssh.pxssh()
			
			#CDN_new1_ip = '192.168.30.21'
			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(CDN_new1_ip, username, password)
		
			
			s.logfile = open(UPLOAD_LOG_FILE,'a+')
			#s.sendline('cd /home/agame/update/wdupdate')
			
			#cmd_mkdir_weiduan = 'mkdir '+ weiduan_download_part2[0:13]
			#print cmd_mkdir_weiduan

			#s.sendline(cmd_mkdir_weiduan)

			#cmd_unzip_weiduan = 'unzip '+weiduan_download_part2+' -d '+weiduan_download_part2[0:13]
			#s.sendline(cmd_unzip_weiduan)

			s.sendline("mkdir /home/agame/update/wdupdate/"+weiduan_download_part2[0:13]+"; unzip /home/agame/update/wdupdate/"+weiduan_download_part2+" -d /home/agame/update/wdupdate/"+weiduan_download_part2[0:13])
			s.prompt(timeout=None)
	

			s.sendline("echo RESULT:$? | awk -F ':' '{print $2}'")
			s.prompt(timeout=None)

			re_result_unzip_ssh = re.compile(r'[\n]')
			result_pre = s.before
			result_ed = re_result_unzip_ssh.split(result_pre)
			result_after = result_ed[1]

			result = int(result_after)

			if result != 0:
				print "unzip微端资源不成功！！！"
				return False
			else:
				print "在CDN_new1解压微端资源包成功！\n"

			s.logout()
			
			#####################################################################解压DuanYou_CDN1上的微端资源

			s = pxssh.pxssh()

			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(DuanYou_CDN1_ip, username, password)
		
			
			s.logfile = open(UPLOAD_LOG_FILE,'a+')
			#s.sendline('cd /home/agame/update/wdupdate')
			
			#cmd_mkdir_weiduan = 'mkdir '+ weiduan_download_part2[0:13]
			#print cmd_mkdir_weiduan

			#s.sendline(cmd_mkdir_weiduan)

			#cmd_unzip_weiduan = 'unzip '+weiduan_download_part2+' -d '+weiduan_download_part2[0:13]
			#s.sendline(cmd_unzip_weiduan)

			
			s.sendline("mkdir /home/agame/update/wdupdate/"+weiduan_download_part2[0:13]+"; unzip /home/agame/update/wdupdate/"+weiduan_download_part2+" -d /home/agame/update/wdupdate/"+weiduan_download_part2[0:13])
			s.prompt(timeout=None)

			s.sendline("echo RESULT:$? | awk -F ':' '{print $2}'")
			s.prompt(timeout=None)

			re_result_unzip_ssh = re.compile(r'[\n]')
			result_pre = s.before
			result_ed = re_result_unzip_ssh.split(result_pre)
			result_after = result_ed[1]

			result = int(result_after)

			if result != 0:
				print "unzip微端资源不成功！！！"
				return False
			else:
				print "在DuanYou_CDN1解压微端资源包成功！\n"


			s.logout()

		except Exception, e:
			print '进行远程到CDN_new1和DuanYou_CDN1上解压微端资源的时候出错了'
			print '出错原因为：\n%s' % str(e)


		######################################################推送wdver_list.xml###########################################


		push_wdverlist_cmd = 'cd ../cdnpush/ ; ./lz_cdnpush_wdver_list.sh'
	
		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
		print '#将要执行推送wdver_list.xml命令：%s' % push_wdverlist_cmd
		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
		print '开始推送>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

		os.system(push_wdverlist_cmd)

		print "##################################################################################################################"
		print " "
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>请到网宿&蓝汛相应后台查询是否完全分发完成"
		print " "
		print "##################################################################################################################"

		print " "

		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>本次微端资源推送工作已经完成\n###################################"
		print " "

		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>本次微端资源推送的zip包为：%s" % weiduan_download_part2
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>本次微端资源推送的版本号为： %s" % weiduan_download_nomal


		#########删除本地的文件######################################################################
		clear_local_wdupdate_cmd='rm -rf ../cdnpush/wdupdatefile/*'

		os.system(clear_local_wdupdate_cmd)


	#######################################################微端安装器############################################
	if choose == 'b':
		
		print ">>>>>>>>>>>>>>>>>>>>推送微端安装器资源>>>>>>>>>>"
		print " "
		mail_wd_downloadfiles_url = raw_input(">>>>>>>>>>>>>>>>>>>>请输入邮件中的微端安装器资源的URL链接：")

		weiduan_downloadfiles = mail_wd_downloadfiles_url.replace('ftp://192.168.4.1/','')

		cmd_download_weiduan='cd ../cdnpush/wdupdatefile/ ; wget -r --ftp-user=om --ftp-password=D6ollHZyIVRCg ftp://192.168.10.123/aplan/'+weiduan_downloadfiles.strip()

		commands.getstatusoutput(cmd_download_weiduan)

		cmd_ls_download_weiduan = 'ls -l ../cdnpush/wdupdatefile/192.168.10.123/aplan/'+weiduan_downloadfiles


		print "\n>>>>>>>>>>>>>>>>>>>>本次微端安装器资源将要更新的xml文件有："
		
		os.system(cmd_ls_download_weiduan)

		print "\n>>>>>>>>>>>>>>>>>>>>请与邮件上地址的内容进行确认，需要更新的微端安装器资源是否为以上内容"

		confirm = raw_input('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>确认无误后将进行本次微端安装器资源的推送工作：【yes or no】>>>')

		if confirm != 'yes':
			return False
		
		
		CDN_new1_ip = '192.168.30.21'
		DuanYou_CDN1_ip = '172.19.0.90'
		
		print '\n正在备份CDN_new1&DuanYou_CDN1上的dlf文件夹>>>>>>>>>>>>>>>>>>>\n'
		#############备份CDN_new1的dlf###################################################################
		try:
        	
			re_backup_ssh = re.compile(r'[\n]')
			
			s = pxssh.pxssh()
			#CDN_new1_ip = '192.168.30.21'
			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(CDN_new1_ip, username, password)

			s.sendline("cp -rf /home/agame/update/dlf /home/agame/update/dlf.`date +%Y%m%d%H%M%S`;echo RESULT:$? | awk -F ':' '{print $2}'")
			
			
			s.prompt()

			result_pre = s.before
			result_ed = re_backup_ssh.split(result_pre)
			result_after = result_ed[1]
			
			result = int(result_after)
			if result != 0:
				print '在CDN_new1上备份dlf的时候出错了。。。'
				return False
			
			s.logout()

		############备份DuanYou_CDN1的dlf###############################################################
			

			s = pxssh.pxssh()
			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(DuanYou_CDN1_ip, username, password)

			s.sendline("cp -rf /home/agame/update/dlf /home/agame/update/dlf.`date +%Y%m%d%H%M%S`;echo RESULT:$? | awk -F ':' '{print $2}'")

			s.prompt()

			result_pre = s.before
			result_ed = re_backup_ssh.split(result_pre)
			result_after = result_ed[1]
			
			result = int(result_after)

			if result != 0:
				print '\n执行备份dlf文件夹出错'
				return False


			s.logout()


		except Exception, e:


			print '执行备份CDN_new1和DuanYou_CDN1上的dlf时出错了！'
			print str(e)
			return False



		print '在两个源站上备份dlf文件夹完毕，接下来进行更新两个源站的dlf的文件夹>>>>>>>>>>>>>>>>>'


		####################################上传dlf
		UPLOAD_dlf_DIR = '../cdnpush/wdupdatefile/192.168.10.123/aplan/'+weiduan_downloadfiles.strip()


		UPLOAD_dlf_FILE = os.popen('ls %s' % UPLOAD_dlf_DIR).readlines()
		
		i = 0
		for filename in UPLOAD_dlf_FILE:
			i = i + 1
			print '>>>>>>>>>>>>>>>>>>>>正在更新第%s个dlf文件：%s' % (i,filename.strip('\n'))
			result_CDN_new1 = commands.getstatusoutput("../modules/scp_expect.sh %s/%s %s" % (UPLOAD_dlf_DIR,filename.strip('\n',),"192.168.30.21:/home/agame/update/dlf"))
			result_DuanYou_CDN1 = commands.getstatusoutput("../modules/scp_expect.sh %s/%s %s" % (UPLOAD_dlf_DIR,filename.strip('\n',),"172.19.0.90:/home/agame/update/dlf"))
			if (result_CDN_new1[0] != 0) or (result_DuanYou_CDN1[0] != 0):
				print '更新第%s个dlf文件失败，该文件名为：%s' % (i,filename.strip('\n'))
				return False



		##########推送dlf目录#########################################################################
		push_dlf_cmd = 'cd ../cdnpush/; ./lz_cdnpush_dlf.sh'
		print "##############################################################################################"
		os.system(push_dlf_cmd)
		print " "
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>请到网宿查看是否分发完成"
		print " "
		print "##############################################################################################"

		print " "

		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>本次微端安装器推送工作已经完成######################"

		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>本次微端安装器更新了的dlf里的文件有：\n"
		os.system(cmd_ls_download_weiduan)


		#########删除本地的文件######################################################################
		clear_local_wdupdate_cmd='rm -rf ../cdnpush/wdupdatefile/*'

		os.system(clear_local_wdupdate_cmd)




	######################################################################################################
	if choose == 'q':
		return True





Main()


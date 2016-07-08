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
# ������  : ���н���
# ����    : 
# option : 	1 ��������������
# 			0 ���رս�������

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
	# a  : ����ά��
	# b  : ��̬�������
	# q  : �˳�
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
	# a  : �ϴ��汾
	# b  : ����ǽ����
	# c  : �رշ���
	# d  : ����ģ��
	# e  : �������ݿ�
	# f  : ����ģ��
	# g  : �Ż����ݿ�
	# h  : ��������
	# q  : ����
	#########################

	choose = Meun.Maintain_meun()

	######################################################## �ϴ��汾 ########################################################
	if choose == 'a':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False

		upload_file = raw_input('������Ҫ�ϴ��İ汾:\n>>>')
		if not os.path.exists(upload_file):
			print '������ļ�·��!'
			return False

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return True
		elif excu_choose != 'start':
			print '�����ѡ��'
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
			print '\033[0;32;40m %s \033[0m��ʼ�ϴ�... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)
			threading.Thread(target=svr_obj.upload_file,args=(upload_file,upload_host,upload_path)).start()
			time.sleep(1)
			
		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		for svr_obj in svr_obj_list:
			if not svr_obj.RESULT:
				print '\033[0;31;40m %s \033[0m �ϴ��汾������!' % svr.NICK_NAME
				continue
			#print svr_obj.GAME_GROUP
			if svr_obj.excute_upload_cmd(svr_obj.GSBAK_IP,'cd /mnt/script; ./upload.sh `basename '+upload_file+'` '+svr_obj.GAME_GROUP):
				svr_obj.RESULT = True
			else:
				svr_obj.RESULT = False

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True

	######################################################## ���ط���ǽ ######################################################	

	if choose == 'b':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False
		fw_choose = raw_input('fw_on : ������ҽ���\nfw_off : �ܾ���ҽ���\n������ [ fw_on fw_off ] >>>').strip()
		if fw_choose not in ['fw_on','fw_off']:
			print '�����ѡ��!'
			return False

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return True
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)

			svr_obj.LOG_FILE = '../log/firewall_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m���ڲ���... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			chk_fw_result = svr_obj.check_firewall()
			if fw_choose == 'fw_on':
				if not chk_fw_result :
					threading.Thread(target=svr_obj.set_firewall,args=(1,)).start()
				else:
					svr_obj.RESULT = False
					print '%s ����ǽ�Ѿ����ˣ������ظ�������' % svr_obj.NICK_NAME

			if fw_choose == 'fw_off':
				if chk_fw_result :
					threading.Thread(target=svr_obj.set_firewall,args=(0,)).start()
				else:
					svr_obj.RESULT = False
					print '%s ����ǽ�Ѿ��ر��ˣ������ظ�������' % svr_obj.NICK_NAME

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
 			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'
		
		return True
	######################################################## �رս��� ########################################################
	if choose == 'c':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False
		proc_choose = Meun.Choose_proc(0)
		if not proc_choose:
			print '����ķ���ѡ��'
			return False

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/closeProc_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼ�رշ���... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)
			
			threading.Thread(target=svr_obj.stop_proc,args=(Proc_sort(proc_choose,0),)).start()
			time.sleep(1)

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	######################################################## ����ģ�� ########################################################
	if choose == 'd':
		svr_obj_list = []

		backup_opt = raw_input('a:�Ƴ����� b:��������\n>>>')
		if backup_opt not in ['a','b']:
			print '�����ѡ��'
			return False
		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False
		mc_choose = Meun.Choose_machine()
		if not mc_choose:
			print '����Ļ���ѡ��'
			return False

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 11:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/backupMod_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼ����ģ��... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			if backup_opt == 'a':
				threading.Thread(target=svr_obj.backup_mod,args=(mc_choose,'mv')).start()
				time.sleep(1)
			else:
				threading.Thread(target=svr_obj.backup_mod,args=(mc_choose,'cp')).start()
				time.sleep(1)

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True

	######################################################## �������ݿ� ########################################################

	if choose == 'e':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False
		# db_choose = Meun.Choose_database()
		# if not db_choose:
		# 	print '����ķ�����ѡ��'
		# 	return False

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/backupDB_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼ�������ݿ�... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

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

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'
		
		return True
	######################################################## ����ģ�� ########################################################
	if choose == 'f':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False
		mc_choose = Meun.Choose_machine()
		if not mc_choose:
			print '����ķ�����ѡ��'
			return False

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		print "ִ����..."
		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/copyMod_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼ����ģ��... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			threading.Thread(target=svr_obj.cp_mod,args=(mc_choose,)).start()
			time.sleep(1)

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	######################################################## �Ż����ݿ� ########################################################
# 	if choose == 'g':
# 		print '������˼����ʱû�������Ҫ��'
# 		return False
 	if choose == 'g':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False
#		dbop_choose = Meun.Choose_proc(1)
#		if not dbop_choose:
#			print '����ķ���ѡ��'
#			return False

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/optimize_DB_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼ�Ż����ݿ�... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			optimizedb_cmd = 'mysql -umysqlbak -pmysqlbakom1c2b -h127.0.0.1 -P3306 a_game -e "optimize table player"'
			threading.Thread(target=svr_obj.excute_cmd,args=(getattr(svr_obj,'GDB_IP'),optimizedb_cmd)).start()
			time.sleep(1)


		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'
		
		return True

	######################################################## �������� ########################################################
	if choose == 'h':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False
		proc_choose = Meun.Choose_proc(1)
		if not proc_choose:
			print '����ķ���ѡ��'
			return False

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 10:
			# 	time.sleep(1)
			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/startProc_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼ��������... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)
			
			threading.Thread(target=svr_obj.start_proc,args=(Proc_sort(proc_choose,1),)).start()
			time.sleep(1)

		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
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
	# a  : �ϴ��ļ�
	# b  : ִ�ж�̬����
	# c  : �����ļ�
	# q  : ����
	#########################

	choose = Meun.Daily_meun()
	######################################################## �ϴ��ļ� ########################################################
	if choose == 'a':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False

		upload_file = raw_input('������Ҫ�ϴ����ļ�:\n')
		if not os.path.exists(upload_file):
			print '������ļ�·��!'
			return False

		proc_choose = Meun.Choose_proc(1)
		if not proc_choose:
			print '������ϴ�����·��'
			return False

		upload_path = raw_input('��������Ҫ�ϴ������·���������Ҫ�ϴ����ǽ��̸�Ŀ¼����ֱ�ӻس�\n��[\'log/modules/\']\n>>>')
		if not upload_path:
			upload_path = upload_path.rstrip('/') + '/'

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			while threading.activeCount() > 11:
				time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/upload_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼ�ϴ�... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			threading.Thread(target=svr_obj.multiple_upload_file,args=(upload_file,upload_path,proc_choose)).start()
			time.sleep(1)
			
		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	######################################################## ��̬���� ########################################################
	if choose == 'b':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False
		proc_choose = Meun.Choose_proc(1)
		if not proc_choose:
			print '����ķ���ѡ��'
			return False
		cmd_choose = raw_input('������Ҫִ�е�����\n>>>')
		if not cmd_choose:
			print '���������'
			return False
		# cmd_choose = repr(cmd_choose)

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			# while threading.activeCount() > 11:
			# 	time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/telnet_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼִ��telnet����... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			threading.Thread(target=svr_obj.multiple_excute_telnet_cmd,args=(proc_choose,cmd_choose)).start()
			time.sleep(1)
			
		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
		for svr in svr_obj_list:
			if not svr.RESULT:
				print '\033[0;31;40m %s \033[0m' % svr.NICK_NAME
		print '###########################################'

		return True
	######################################################## �����ļ� ########################################################
	if choose == 'c':
		svr_obj_list = []

		svr_choose = Meun.Choose_server()
		if not svr_choose:
			print '����ķ�����ѡ��'
			return False

		proc_choose = Meun.Choose_proc(1)
		if not proc_choose:
			print '��������ؽ���'
			return False

		download_path = raw_input('��������Ҫ���ص����·����\n��[\'log/*.log\']\n>>>')

		excu_choose = raw_input('ȷ��Ҫִ����?[ start return ]\n>>>').strip()
		if excu_choose == 'return':
			return False
		elif excu_choose != 'start':
			print '�����ѡ��'
			return False
		else:
			pass

		for svr in svr_choose:
			while threading.activeCount() > 11:
				time.sleep(1)

			svr_obj = init_server(SVR_CFG.get_svr_info_by_name(svr))
			svr_obj_list.append(svr_obj)
			svr_obj.LOG_FILE = '../log/download_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+svr_obj.SERVER_NAME+'_log.txt'
			print '\033[0;32;40m %s \033[0m��ʼ����... ###%s###' % (svr_obj.NICK_NAME,svr_obj.LOG_FILE)

			threading.Thread(target=svr_obj.multiple_download_file,args=(download_path,proc_choose)).start()
			time.sleep(1)
	
		while threading.activeCount() != 1:
			#print threading.enumerate()
			time.sleep(1)

		print '###########����ķ�ִ�гɹ�����############'
		for svr in svr_obj_list:
			if svr.RESULT:
				print '\033[0;32;40m %s \033[0m' % svr.NICK_NAME
		print '###########����ķ�ִ��ʧ������############'
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
	# a : ��һ��:���ز��޸�patch_list.xml,���ϴ��������ļ�
	# b : �ڶ���:����patch_list.xml
	# c : ������:����server_list.xml
	#########################

	choose = Meun.CDN_meun()
	########################################## ���ز��޸�patch_list.xml,���ϴ��������ļ� ########################################
	if choose == 'a':
		PATCH_LOG_FILE= '../log/cdnpushlog/uploadpatchfiles_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+'_log.txt'


		print "##################################################################################################"
		print '#�뽫���е�patch.sy , patch.exe , depatch.sy , depatch.exe , patch.sy.md5.txt , depatch.sy.md5.txt'
		print '#�ŵ� ../cdnpush/patchfile/ Ŀ¼����ȥ, ����Ҫ����Ŷ~'

		make_patchlist_cmd = 'cd ../cdnpush/ ; ./make_patchlist.sh'
		print '#����,��ִ�������µ�patch_list.xml ����: %s' % make_patchlist_cmd
		print '#���ɵ�patch_list.xml : ../cdnpush/patch_list.xml_ws(patch_list.xml_lx)'
		print "##################################################################################################"
		continue_choose = raw_input('ȷ���ź���?����?[ yes ����������жϲ��� ]\n>>>')
		if continue_choose.strip() != 'yes':
			return False
		os.system("touch "+PATCH_LOG_FILE+";"+make_patchlist_cmd+" | tee "+PATCH_LOG_FILE)

		
		upload_patchfile_cmd = 'cd ../cdnpush/ ; ./upload_patchfile.py'
		print 'Ȼ��,��ִ���ϴ������� ����: %s' % upload_patchfile_cmd
		continue_choose = raw_input('��������,�����ϴ�������?[ yes ����������жϲ��� ]\n>>>')
		if continue_choose.strip() != 'yes':
			return False
		os.system(upload_patchfile_cmd+" | tee "+PATCH_LOG_FILE)
		
		print "##################################################################################################"
		print '#�Ƿ���ȫ�ַ���,��� ���޺�̨-->���ݹ���-->���ļ�ϵͳ-->�����ѯ ���в鿴'
		print '#                      ��Ѵ�Ĵ�fds4.exe ���߲鿴�Ƿ��Ѿ� �ɷ��� ״̬'
		print "##################################################################################################"

		return True

	########################################## ����patch_list.xml ########################################
	if choose == 'b':
		PUSH_PATCH_LIST_LOG_FILE= '../log/cdnpushlog/uploadpatch_list_xml_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+'_log.txt'
			
		print "##################################################################################################"
		print '#��ȷ��patch_list.xml������ȷ : ../cdnpush/patch_list.xml_ws(patch_list.xml_lx)'
		
		push_patchlist_cmd = 'cd ../cdnpush/ ; ./lz_cdnpush_patchlist.sh'
		print '#��ִ������patch_list ����: %s' % push_patchlist_cmd
		print "##################################################################################################"

		continue_choose = raw_input('�������?����?[ yes ����������жϲ��� ]\n>>>')
		if continue_choose.strip() != 'yes':
			return False
		os.system("touch "+PUSH_PATCH_LIST_LOG_FILE+";"+push_patchlist_cmd+" | tee "+PUSH_PATCH_LIST_LOG_FILE)

		print "##################################################################################################"
		print '#�뵽������Ӧ�ĺ�̨��ѯ�Ƿ���ȫ�ַ����'
		print "##################################################################################################"
		return True

	########################################## ����server_list.xml ########################################
	if choose == 'c':
		PUSH_SERVER_LIST_LOG_FILE= '../log/cdnpushlog/uploadserver_list_xml_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+'_log.txt'
		
		print "##################################################################################################"
		print "#��Ҫ����������һ���µ�server_list.xml������"

		download_serverlist_cmd = "cd ../cdnpush/ ; wget -N http://172.19.0.90/agame/update/server_list.xml"
		print '#��ִ������server_list ����: %s' % download_serverlist_cmd
		print "#������������� : more ../cdnpush/server_list.xml "
		print "##################################################################################################"
		download_choose = raw_input('��Ҫ��[ yes ��������������˲��� ]\n>>>')
		if download_choose.strip() == 'yes':
			os.system("touch "+PUSH_SERVER_LIST_LOG_FILE+";"+download_serverlist_cmd+" | tee "+PUSH_SERVER_LIST_LOG_FILE)

		print "##################################################################################################"
		print '#��ȷ��server_list.xml������ȷ : ../cdnpush/server_list.xml'

		push_serverlist_cmd = 'cd ../cdnpush/ ; ./lz_cdnpush_serverlist.sh server_list.xml'
		print '#��ִ������server_list ����: %s' % push_serverlist_cmd
		print '''#��Ҳ�����ֶ�ִ�л��߶�ʱ����: "cd ../cdnpush/ ; ./lz_cdnpush_serverlist.sh <serverlist�ļ�>" '''
		print "##################################################################################################"

		continue_choose = raw_input('�������?����?[ yes ����������жϲ��� ]\n>>>')
		if continue_choose.strip() != 'yes':
			return False
		os.system(push_serverlist_cmd+" | tee "+PUSH_SERVER_LIST_LOG_FILE)

		print "##################################################################################################"
		print '#�뵽������Ӧ�ĺ�̨��ѯ�Ƿ���ȫ�ַ����'
		print "##################################################################################################"

		return True

	########################################################
	if choose == 'q':
		return True
	########################################################

#20151028ɽ�����΢����Դ����ģ��
def WeiDuanJob():
	#################################################
	#  a : ΢����Դ����
	#  b : ΢������������
	#
	#################################################
	
	choose = Meun.WeiDuan_meun()

	#print "choose:"+choose
	########################################################΢����Դ##############################################
	if choose == 'a':
		UPLOAD_LOG_FILE= '../log/wdupdate_'+time.strftime(time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time())))+'_log.txt'
		print "###################################################################################"
		print "#����������ftp://192.168.10.123/aplan/������΢����Դ"
		print "#���غõ�΢����Դ��������../cdnpush/wdupdatefile��"
		print "#����΢����Դ�ϴ���������־�ļ�Ϊ:"+UPLOAD_LOG_FILE
		mail_weiduan_download_url = raw_input(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>�����뱾���ʼ���΢����Դ��URL���ӣ�")
		weiduan_download_folder = mail_weiduan_download_url.replace('ftp://192.168.4.1/','')
		weiduan_download = weiduan_download_folder.strip()
		#######################����΢�˰汾######
		weiduan_download_split = weiduan_download.split('/')
		weiduan_download_part2 = weiduan_download_split[1]
		weiduan_download_number = weiduan_download_part2[7:13]
		weiduan_download_nomal = weiduan_download_number[0]+'.'+weiduan_download_number[1:3]+'.'+weiduan_download_number[3:6]

		#########################################

		print "\n\n��ȷ�ϴ˴�΢�˵İ汾�ţ�"+ weiduan_download_nomal
		print "\n\n��ȷ���ʼ���΢����Դλ��Ϊ��ftp://192.168.4.1/"+ weiduan_download

		continue_choose = raw_input('\n���ʼ���΢����Դλ��һ���𣿡�yes����ִ��  ����  ����������������һ��  ��>>>>>>>>>>>')
		
		if continue_choose.strip() == 'yes':
			pass
		else:
			return False


		#######################################����־�ļ�####################################
		f=open(UPLOAD_LOG_FILE,'a+')


		
		cmd_download_weiduan='cd ../cdnpush/wdupdatefile/ ; wget --ftp-user=om --ftp-password=D6ollHZyIVRCg ftp://192.168.10.123/aplan/'+weiduan_download
		download_weiduan_result=os.system(cmd_download_weiduan)
		result_float2str=str(download_weiduan_result)
		result='����΢����Դ�Ľ��Ϊ��'+result_float2str+'\n'
		f.write(result)


		download_wdver_result=os.system('cd ../cdnpush/wdupdatefile/ ;wget -N http://192.168.30.21/agame/update/wdver_list.xml')
		result_float2str=str(download_wdver_result)
		result='����wdver_list.xml�Ľ��Ϊ��'+result_float2str+'\n'
		f.write(result)

		
		f.close()
		####################�������Ĵ����Ǵ���wdver_list.xml,�Ը��ļ���������#############################
        

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

		#######################�޸�wdver_list.xml�ļ��������##########################################
		
		######################md5sum######################################################
		re_md5sum = re.compile(' ')
		weiduan_md5sum_pre = commands.getoutput('md5sum ../cdnpush/wdupdatefile/'+weiduan_download_part2)
		weiduan_md5sum_1 = re_md5sum.split(weiduan_md5sum_pre)
		md5sum_weiduan_1 = weiduan_md5sum_1[0]
		
		wdver_md5sum_pre = commands.getoutput('md5sum ../cdnpush/wdupdatefile/wdver_list.xml')
		wdver_md5sum_1 = re_md5sum.split(wdver_md5sum_pre)
		md5sum_wdver_1 = wdver_md5sum_1[0]

		######################�����Ϊδ�ϴ���md5sum��##############################################
		
		UPLOAD_WEIDUAN_DIR='../cdnpush/wdupdatefile/'

		UPLOAD_WEIDUAN_FILE=os.popen('ls %s | grep -v xml'% UPLOAD_WEIDUAN_DIR).readlines()
	
		if not UPLOAD_WEIDUAN_FILE:
			print "%s has nothing!!Please exit the script and try again!" % UPLOAD_WEIDUAN_DIR
			return False
		UPLOAD_WDVER_LIST_FILE ='wdver_list.xml'

		###########################################��CDN_new1��DuanYou_CDN1�ϱ���wdver_list.xml
		
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
				print "\n��CDN_new1�ϱ���wdver_list.xml��ʱ������ˡ����������¿�ʼ"
				return False
			s.logout()

		except Exception, e:
			print 'Զ�����ӵ�CDN_new1�ϱ���wdver_list.xml�Ĺ����У�Զ������δ�ܽ�����'
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
				print "\n��DuanYou_CDN1�ϱ���wdver_list.xml��ʱ������ˡ����������¿�ʼ"
				return False
			s.logout()

		except Exception, e:
			print 'Զ�����ӵ�DuanYou_CDN1�ϱ���wdver_list.xml�Ĺ����У�Զ������δ�ܽ�����'
			print e
			return False
			
		#################################################################################################



		####################�ϴ�΢����Դ��΢����������CDN_new1(192.168.30.21)��DuanYou_CDN1(172.19.0.90)############################################
		
		print "����������΢����Դ��wdver_list.xml�ϴ���CDN_new1(192.168.30.21)��DuanYou_CDN1(172.19.0.90)>>>>>>>>>>"

		print "\n�ϴ�΢����Դ���̽ϳ��������ĵȴ�......\n"

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
    

		print "�ϴ���......�����Եȣ�������>>>>>>>>>\n"
		print "Uploading......\n"
		while threading.activeCount() != 1:
			time.sleep(1)
		
        
		print "΢����Դ��wdver_list.xml�ϴ����......\n"

		print "�ϴ�΢����Դ��wdver_list.xml��ϣ�����������һ��----���鱾��΢����Դ��wdver_list.xml��md5sum��CDN_new1&DuanYou_CDN1���ļ���md5sum�Ƿ���ͬ>>>>>>>>>>"
		
		#time.sleep(5)




		###################��10.251�ϲ���##################################
		#conntinue_to_upload=raw_input('�����ϴ���remote machine�𣿡�����������')
		
		#print "׼���ϴ�΢����Դ��../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,weiduan_download_part2.strip(), "192.168.30.21:/home/omadmin/shanzhu" )

		#result_weiduan_10_251 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,weiduan_download_part2.strip(), "192.168.30.21:/home/omadmin/shanzhu"))
		
		#result_weiduan_system =os.system("../modules/scp_expect.sh"+" "+ UPLOAD_WEIDUAN_DIR + weiduan_download_part2.strip() +" "+"192.168.30.21:/home/omadmin/shanzhu")

		#if result_weiduan_system !=0:
		#	print "�ϴ�"+weiduan_download_part2.strip()+"���ɹ���������"
		#else:
		#	print "�ϴ� "+weiduan_download_part2.strip()+" �ɹ�����������"

		#if result_weiduan_10_251[0] != 0:
		#	print "upload ΢����Դʧ�ܣ�����"
		#else:
		#	print result_weiduan_10_251[1]

		#print "׼���ϴ�wdver_list.xml: ../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,UPLOAD_WDVER_LIST_FILE,"192.168.30.21:/home/omadmin/shanzhu")

		#result_wdver_10_251 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,UPLOAD_WDVER_LIST_FILE, "192.168.30.21:/home/omadmin/shanzhu"))

		#result_wdver_10_251 =commands.getstatusoutput("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,UPLOAD_WDVER_LIST_FILE, "192.168.30.21:/home/omadmin/shanzhu"))
	
		#result_wdver_system =os.system("../modules/scp_expect.sh"+" "+ UPLOAD_WEIDUAN_DIR + UPLOAD_WDVER_LIST_FILE +" "+"192.168.30.21:/home/omadmin/shanzhu")
		
		#if result_wdver_system !=0:
		#	print "�ϴ�"+UPLOAD_WDVER_LIST_FILE+"���ɹ���������"
		#else:
		#	print "�ϴ� "+UPLOAD_WDVER_LIST_FILE+" �ɹ�����������"
		#if result_wdver_10_251[0] != 0:
		#	print "upload ΢��������ʧ�ܣ�����"
		#else:
		#	print result_wdver_10_251[1]
		
		#os.system("../modules/scp_expect.sh %s%s %s" % (UPLOAD_WEIDUAN_DIR,UPLOAD_WDVER_LIST_FILE, "192.168.10.251:/home/agame/update/"))
	
		###################���鴫��ȥ��md5sum###########################################################################################################

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
			#############################����wdver_list.xml
			s.sendline(get_wdver_list_md5_cmd)
			s.prompt(timeout=None)
			wdver_md5sum_uploaded_pre = s.before
			wdver_md5sum_uploaded = re_md5sum_ssh.split(wdver_md5sum_uploaded_pre)
			md5sum_wdver_uploaded = wdver_md5sum_uploaded[3]
			if md5sum_wdver_1 == md5sum_wdver_uploaded:
				print 'wdver_list.xml�����봫��CDN_new1�ϵ��ļ�md5sum����ͬ\n'
			else:
				print 'wdver_list.xml�����봫��CDN_new1�ϵ��ļ�md5sum�벻��ͬ,������ز����������ϴ�\n'
				print '����wdver_list.xml�ļ���md5sum��Ϊ��'+md5sum_wdver_1+'\n'
				print 'CDN_new1�ϵ�wdver_list.xml�ļ���md5usm��Ϊ��'+md5sum_wdver_uploaded+'\n'
				return False
			#############################����΢����Դ
			s.sendline(get_weiduan_md5_cmd)
			s.prompt(timeout=None)
			weiduan_md5sum_uploaded_pre = s.before
			weiduan_md5sum_uploaded = re_md5sum_ssh.split(weiduan_md5sum_uploaded_pre)
			md5sum_weiduan_uploaded = weiduan_md5sum_uploaded[3]
            
			#print weiduan_md5sum_uploaded_pre
			#print md5sum_weiduan_uploaded
			#print md5sum_weiduan_1
            
			if md5sum_weiduan_1 == md5sum_weiduan_uploaded:
				print '����΢����Դ�봫��CDN_new1�ϵ��ļ�md5sum����ͬ\n'
			else:
				print '����΢����Դ�봫��CDN_new1�ϵ��ļ�md5sum�벻��ͬ,������ز����������ϴ�\n'
				print '����΢����Դ�ļ���md5sum��Ϊ��'+md5sum_weiduan_1+'\n'
				print 'CDN_new1�ϵ��ļ���md5sum��Ϊ��'+md5sum_weiduan_uploaded+'\n'
				return False

			s.logout()

			
			################################DuanYou_CDN1

			s = pxssh.pxssh()

			username = 'omadmin'
			password = 'shangyoo!@#$'

			s.login(DuanYou_CDN1_ip, username, password)
			
			
			s.logfile = open(UPLOAD_LOG_FILE,'a+')
			#############################����wdver_list.xml
			s.sendline(get_wdver_list_md5_cmd)
			s.prompt(timeout=None)
			wdver_md5sum_uploaded_pre = s.before
			wdver_md5sum_uploaded = re_md5sum_ssh.split(wdver_md5sum_uploaded_pre)
			md5sum_wdver_uploaded = wdver_md5sum_uploaded[3]
			if md5sum_wdver_1 == md5sum_wdver_uploaded:
				print '����wdver_list.xml�봫��DuanYou_CDN1�ϵ��ļ�md5sum����ͬ'
			else:
				print '����wdver_list.xml�봫��DuanYou_CDN1�ϵ��ļ�md5sum�벻��ͬ����������ļ��������ϴ�\n'
				print '����wdver_list.xml�ļ���md5sum��Ϊ��'+md5sum_wdver_1+'\n'
				print 'DuanYou_CDN1��wdver_list.xml�ļ���md5sum��Ϊ��'+md5sum_wdver_uploaded+'\n'
				return False
			#############################����΢����Դ
			s.sendline(get_weiduan_md5_cmd)
			s.prompt(timeout=None)
			weiduan_md5sum_uploaded_pre = s.before
			weiduan_md5sum_uploaded = re_md5sum_ssh.split(weiduan_md5sum_uploaded_pre)
			md5sum_weiduan_uploaded = weiduan_md5sum_uploaded[3]
			if md5sum_weiduan_1 == md5sum_weiduan_uploaded:
				print '����΢����Դ�봫��DuanYou_CDN1�ϵ��ļ�md5sum����ͬ\n'
			else:
				print '����΢����Դ�봫��DuanYou_CDN1�ϵ��ļ�md5sum�벻��ͬ����������ļ��������ϴ�\n'
				print '����΢����Դ���ļ�md5sum��Ϊ��'+md5sum_weiduan_1+'\n'
				print 'DuanYou_CDN1�ϵ�΢����Դ�ļ�md5sum��Ϊ��'+md5sum_weiduan_uploaded+'\n'
				return False

			s.logout()


		except Exception, e:
			print 'pxssh failed on login.'
			print str(e)

		#################����md5sum���������������沽��#################################################################


        ################�����������΢����Դ�����ļ��к󣬽�ѹ������ļ���#############################################
		print '��CDN_new1��DuanYou_CDN1�ϵ�΢����Դ���н�ѹ>>>>>>>>>>>>'
		
		try:
			#####################################################��ѹCDN_new1�ϵ�΢����Դ
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
				print "unzip΢����Դ���ɹ�������"
				return False
			else:
				print "��CDN_new1��ѹ΢����Դ���ɹ���\n"

			s.logout()
			
			#####################################################################��ѹDuanYou_CDN1�ϵ�΢����Դ

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
				print "unzip΢����Դ���ɹ�������"
				return False
			else:
				print "��DuanYou_CDN1��ѹ΢����Դ���ɹ���\n"


			s.logout()

		except Exception, e:
			print '����Զ�̵�CDN_new1��DuanYou_CDN1�Ͻ�ѹ΢����Դ��ʱ�������'
			print '����ԭ��Ϊ��\n%s' % str(e)


		######################################################����wdver_list.xml###########################################


		push_wdverlist_cmd = 'cd ../cdnpush/ ; ./lz_cdnpush_wdver_list.sh'
	
		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
		print '#��Ҫִ������wdver_list.xml���%s' % push_wdverlist_cmd
		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
		print '��ʼ����>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

		os.system(push_wdverlist_cmd)

		print "##################################################################################################################"
		print " "
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>�뵽����&��Ѵ��Ӧ��̨��ѯ�Ƿ���ȫ�ַ����"
		print " "
		print "##################################################################################################################"

		print " "

		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>����΢����Դ���͹����Ѿ����\n###################################"
		print " "

		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>����΢����Դ���͵�zip��Ϊ��%s" % weiduan_download_part2
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>����΢����Դ���͵İ汾��Ϊ�� %s" % weiduan_download_nomal


		#########ɾ�����ص��ļ�######################################################################
		clear_local_wdupdate_cmd='rm -rf ../cdnpush/wdupdatefile/*'

		os.system(clear_local_wdupdate_cmd)


	#######################################################΢�˰�װ��############################################
	if choose == 'b':
		
		print ">>>>>>>>>>>>>>>>>>>>����΢�˰�װ����Դ>>>>>>>>>>"
		print " "
		mail_wd_downloadfiles_url = raw_input(">>>>>>>>>>>>>>>>>>>>�������ʼ��е�΢�˰�װ����Դ��URL���ӣ�")

		weiduan_downloadfiles = mail_wd_downloadfiles_url.replace('ftp://192.168.4.1/','')

		cmd_download_weiduan='cd ../cdnpush/wdupdatefile/ ; wget -r --ftp-user=om --ftp-password=D6ollHZyIVRCg ftp://192.168.10.123/aplan/'+weiduan_downloadfiles.strip()

		commands.getstatusoutput(cmd_download_weiduan)

		cmd_ls_download_weiduan = 'ls -l ../cdnpush/wdupdatefile/192.168.10.123/aplan/'+weiduan_downloadfiles


		print "\n>>>>>>>>>>>>>>>>>>>>����΢�˰�װ����Դ��Ҫ���µ�xml�ļ��У�"
		
		os.system(cmd_ls_download_weiduan)

		print "\n>>>>>>>>>>>>>>>>>>>>�����ʼ��ϵ�ַ�����ݽ���ȷ�ϣ���Ҫ���µ�΢�˰�װ����Դ�Ƿ�Ϊ��������"

		confirm = raw_input('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ȷ������󽫽��б���΢�˰�װ����Դ�����͹�������yes or no��>>>')

		if confirm != 'yes':
			return False
		
		
		CDN_new1_ip = '192.168.30.21'
		DuanYou_CDN1_ip = '172.19.0.90'
		
		print '\n���ڱ���CDN_new1&DuanYou_CDN1�ϵ�dlf�ļ���>>>>>>>>>>>>>>>>>>>\n'
		#############����CDN_new1��dlf###################################################################
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
				print '��CDN_new1�ϱ���dlf��ʱ������ˡ�����'
				return False
			
			s.logout()

		############����DuanYou_CDN1��dlf###############################################################
			

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
				print '\nִ�б���dlf�ļ��г���'
				return False


			s.logout()


		except Exception, e:


			print 'ִ�б���CDN_new1��DuanYou_CDN1�ϵ�dlfʱ�����ˣ�'
			print str(e)
			return False



		print '������Դվ�ϱ���dlf�ļ�����ϣ����������и�������Դվ��dlf���ļ���>>>>>>>>>>>>>>>>>'


		####################################�ϴ�dlf
		UPLOAD_dlf_DIR = '../cdnpush/wdupdatefile/192.168.10.123/aplan/'+weiduan_downloadfiles.strip()


		UPLOAD_dlf_FILE = os.popen('ls %s' % UPLOAD_dlf_DIR).readlines()
		
		i = 0
		for filename in UPLOAD_dlf_FILE:
			i = i + 1
			print '>>>>>>>>>>>>>>>>>>>>���ڸ��µ�%s��dlf�ļ���%s' % (i,filename.strip('\n'))
			result_CDN_new1 = commands.getstatusoutput("../modules/scp_expect.sh %s/%s %s" % (UPLOAD_dlf_DIR,filename.strip('\n',),"192.168.30.21:/home/agame/update/dlf"))
			result_DuanYou_CDN1 = commands.getstatusoutput("../modules/scp_expect.sh %s/%s %s" % (UPLOAD_dlf_DIR,filename.strip('\n',),"172.19.0.90:/home/agame/update/dlf"))
			if (result_CDN_new1[0] != 0) or (result_DuanYou_CDN1[0] != 0):
				print '���µ�%s��dlf�ļ�ʧ�ܣ����ļ���Ϊ��%s' % (i,filename.strip('\n'))
				return False



		##########����dlfĿ¼#########################################################################
		push_dlf_cmd = 'cd ../cdnpush/; ./lz_cdnpush_dlf.sh'
		print "##############################################################################################"
		os.system(push_dlf_cmd)
		print " "
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>�뵽���޲鿴�Ƿ�ַ����"
		print " "
		print "##############################################################################################"

		print " "

		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>����΢�˰�װ�����͹����Ѿ����######################"

		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>����΢�˰�װ�������˵�dlf����ļ��У�\n"
		os.system(cmd_ls_download_weiduan)


		#########ɾ�����ص��ļ�######################################################################
		clear_local_wdupdate_cmd='rm -rf ../cdnpush/wdupdatefile/*'

		os.system(clear_local_wdupdate_cmd)




	######################################################################################################
	if choose == 'q':
		return True





Main()


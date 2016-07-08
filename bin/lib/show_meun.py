#!/usr/bin/python
#-*- coding: utf-8 -*-

import GlobalConfig
from read_gamegroup_cfg import *
from read_proc_cfg import *

class meun:
	GameGroupCfgFile = GlobalConfig.GameGroupCfgFile
	ServerCfgFile = GlobalConfig.ServerCfgFile

	def Main_meun(self):
		show_menu = {'a':'����ά��',
					 'b':'�ճ�ά��',
					 'c':'CDNά��',
					 'd':'΢��ά��',
					 'q':'�˳�'}
		
		for cho in ['a','b','c','d','q']:
			print '\033[0;32;40m %s \033[0m : %s' % (cho,show_menu[cho])

		while 1:
			choose = ''
			choose = raw_input('Input your choose:\n>>>')
			if choose not in ['a','b','c','d','q']:
				print 'don\'t fool me!'
			else:
				return choose

	def Maintain_meun(self):
		show_menu = {'a':'�ϴ��汾',
					 'b':'����ǽ����',
					 'c':'�رշ���',
					 'd':'����ģ��',
					 'e':'�������ݿ�',
					 'f':'����ģ��',
					 'g':'�Ż����ݿ�',
					 'h':'��������',
					 'q':'����'}

		for cho in ['a','b','c','d','e','f','g','h','q']:
			print '\033[0;32;40m %s \033[0m : %s' % (cho,show_menu[cho])

		while 1:
			choose = ''
			choose = raw_input('Input your choose:\n>>>')
			if choose not in ['a','b','c','d','e','f','g','h','q']:
				print 'don\'t fool me!'
			else:
				return choose

	def Daily_meun(self):
		show_menu = {'a':'�ϴ��ļ�',
					 'b':'ִ�ж�̬����',
					 'c':'�����ļ�',
					 'q':'����'}

		for cho in ['a','b','c','q']:
			print '\033[0;32;40m %s \033[0m : %s' % (cho,show_menu[cho])

		while 1:
			choose = ''
			choose = raw_input('Input your choose:\n>>>')
			if choose not in ['a','b','c','q']:
				print 'don\'t fool me!'
			else:
				return choose

	def CDN_meun(self):
		show_menu = {'a':'��һ��:���ز��޸�patch_list.xml,���ϴ��������ļ�',
					 'b':'�ڶ���:����patch_list.xml',
					 'c':'������:����server_list.xml',
					 'q':'����'}

		for cho in ['a','b','c','q']:
			print '\033[0;32;40m %s \033[0m : %s' % (cho,show_menu[cho])

		while 1:
			choose = ''
			choose = raw_input('Input your choose:\n>>>')
			if choose not in ['a','b','c','q']:
				print 'don\'t fool me!'
			else:
				return choose
#20151027ɽ�����
	def WeiDuan_meun(self):
		show_menu= {'a':'΢����Դ����',
					'b':'΢�˰�װ������',
					'q':'����'}

		for cho in ['a','b','q']:
			print '\033[0;32;40m %s \033[0m : %s' % (cho,show_menu[cho])

		while 1:
			choose = ''
			choose = raw_input('Input your choose:\n>>>')
			if choose not in ['a','b','q']:
				print 'don\'t fool me!'
			else: 
				return choose



	def Choose_server(self):
		svr_info = read_gamegroup_cfg(self.GameGroupCfgFile).get_all_svr_info()
		svr_name = read_gamegroup_cfg(self.GameGroupCfgFile).get_all_svr_name()

		print '��ѡ����Ҫ�����ķ�:'
		for i in range(len(svr_info)):
			print '\t%s \033[0;33;40m (%s) \033[0m' % (svr_info[i][0],svr_info[i][3])

		choose = ''
		choose = raw_input('������:[ ALL Ϊȫѡ ]\n>>>').split()
		if choose == []:
			return False
		if len(choose) == 1 and choose[0] == 'ALL':
			choose = svr_name
		for i in range(len(choose)):
			if choose[i] not in svr_name:
				return False
			else:
				continue
		print '###############  ��ѡ�������� %d ����  ##############' % len(choose)
		for i in range(len(choose)):
			print choose[i],
		print '\n###################################################'
		return choose

	def Choose_proc(self,sort_option):
		proc_name = Proc_sort(read_proc_cfg(self.ServerCfgFile).get_all_proc_name(1),sort_option)

		print '��ѡ����Ҫ�����Ľ���:'
		for i in range(len(proc_name)):
			print ' \033[0;33;40m%s\033[0m' % (proc_name[i]),

		choose = ''
		choose = raw_input('\n������:[ ALL Ϊ���ϳ��� BLOB ֮������н��� ]\n>>>').split()
		if choose == []:
			return False
		if len(choose) == 1 and choose[0] == 'ALL':
			all_proc = proc_name[:]
			all_proc.remove('BLOB')
			choose = all_proc
		for i in range(len(choose)):
			if choose[i] not in proc_name:
				return False
			else:
				continue
		print '###############  ��ѡ�������� %d ������  ##############' % len(choose)
		for i in range(len(choose)):
			print choose[i],
		print '\n#####################################################'
		return choose

	def Choose_machine(self):
		machine_name = ['GS1','GS2','GS3','GS4','GS5','GSBAK','GDB','LS','DBM']
		print '��ѡ�������:'
		for i in range(len(machine_name)):
			print ' \033[0;33;40m%s\033[0m' % (machine_name[i]),

		choose = ''
		choose = raw_input('\n������:\n>>>').split()
		if choose == []:
			return False
		if len(choose) == 1 and choose[0] == 'ALL':
			choose = machine_name
		for i in range(len(choose)):
			if choose[i] not in machine_name:
				return False
			else:
				continue
		print '###############  ��ѡ�������� %d ��������  ##############' % len(choose)
		for i in range(len(choose)):
			print choose[i],
		print '\n#####################################################'
		return choose

	def Choose_database(self):
		# database_name = ['a_game','a_gamelog','a_gamemining','lz_public_log']
		database_name = ['a_game']
		print '��ѡ�����ݿ�:'
		for i in range(len(database_name)):
			print ' \033[0;33;40m%s\033[0m' % (database_name[i]),

		choose = ''
		choose = raw_input('\n������:\n').split()
		for i in range(len(choose)):
			if choose[i] not in database_name:
				return False
			else:
				continue
		return choose





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

# meun1 = meun()
# print meun1.Main_meun()
# print meun1.Maintain_meun()
# print meun1.Daily_meun()
# print meun1.Choose_server()
# pl = meun1.Choose_proc(proc1.get_all_proc_name())
# print meun1.Proc_sort(pl,0)

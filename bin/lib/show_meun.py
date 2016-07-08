#!/usr/bin/python
#-*- coding: utf-8 -*-

import GlobalConfig
from read_gamegroup_cfg import *
from read_proc_cfg import *

class meun:
	GameGroupCfgFile = GlobalConfig.GameGroupCfgFile
	ServerCfgFile = GlobalConfig.ServerCfgFile

	def Main_meun(self):
		show_menu = {'a':'例行维护',
					 'b':'日常维护',
					 'c':'CDN维护',
					 'd':'微端维护',
					 'q':'退出'}
		
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
		show_menu = {'a':'上传版本',
					 'b':'防火墙设置',
					 'c':'关闭服务',
					 'd':'备份模块',
					 'e':'备份数据库',
					 'f':'拷贝模块',
					 'g':'优化数据库',
					 'h':'启动服务',
					 'q':'返回'}

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
		show_menu = {'a':'上传文件',
					 'b':'执行动态更新',
					 'c':'下载文件',
					 'q':'返回'}

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
		show_menu = {'a':'第一步:下载并修改patch_list.xml,并上传补丁包文件',
					 'b':'第二步:推送patch_list.xml',
					 'c':'第三步:推送server_list.xml',
					 'q':'返回'}

		for cho in ['a','b','c','q']:
			print '\033[0;32;40m %s \033[0m : %s' % (cho,show_menu[cho])

		while 1:
			choose = ''
			choose = raw_input('Input your choose:\n>>>')
			if choose not in ['a','b','c','q']:
				print 'don\'t fool me!'
			else:
				return choose
#20151027山竹添加
	def WeiDuan_meun(self):
		show_menu= {'a':'微端资源推送',
					'b':'微端安装器推送',
					'q':'返回'}

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

		print '请选择需要操作的服:'
		for i in range(len(svr_info)):
			print '\t%s \033[0;33;40m (%s) \033[0m' % (svr_info[i][0],svr_info[i][3])

		choose = ''
		choose = raw_input('请输入:[ ALL 为全选 ]\n>>>').split()
		if choose == []:
			return False
		if len(choose) == 1 and choose[0] == 'ALL':
			choose = svr_name
		for i in range(len(choose)):
			if choose[i] not in svr_name:
				return False
			else:
				continue
		print '###############  你选择了以下 %d 个服  ##############' % len(choose)
		for i in range(len(choose)):
			print choose[i],
		print '\n###################################################'
		return choose

	def Choose_proc(self,sort_option):
		proc_name = Proc_sort(read_proc_cfg(self.ServerCfgFile).get_all_proc_name(1),sort_option)

		print '请选择需要操作的进程:'
		for i in range(len(proc_name)):
			print ' \033[0;33;40m%s\033[0m' % (proc_name[i]),

		choose = ''
		choose = raw_input('\n请输入:[ ALL 为以上除了 BLOB 之外的所有进程 ]\n>>>').split()
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
		print '###############  你选择了以下 %d 个进程  ##############' % len(choose)
		for i in range(len(choose)):
			print choose[i],
		print '\n#####################################################'
		return choose

	def Choose_machine(self):
		machine_name = ['GS1','GS2','GS3','GS4','GS5','GSBAK','GDB','LS','DBM']
		print '请选择服务器:'
		for i in range(len(machine_name)):
			print ' \033[0;33;40m%s\033[0m' % (machine_name[i]),

		choose = ''
		choose = raw_input('\n请输入:\n>>>').split()
		if choose == []:
			return False
		if len(choose) == 1 and choose[0] == 'ALL':
			choose = machine_name
		for i in range(len(choose)):
			if choose[i] not in machine_name:
				return False
			else:
				continue
		print '###############  你选择了以下 %d 个服务器  ##############' % len(choose)
		for i in range(len(choose)):
			print choose[i],
		print '\n#####################################################'
		return choose

	def Choose_database(self):
		# database_name = ['a_game','a_gamelog','a_gamemining','lz_public_log']
		database_name = ['a_game']
		print '请选择数据库:'
		for i in range(len(database_name)):
			print ' \033[0;33;40m%s\033[0m' % (database_name[i]),

		choose = ''
		choose = raw_input('\n请输入:\n').split()
		for i in range(len(choose)):
			if choose[i] not in database_name:
				return False
			else:
				continue
		return choose





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

# meun1 = meun()
# print meun1.Main_meun()
# print meun1.Maintain_meun()
# print meun1.Daily_meun()
# print meun1.Choose_server()
# pl = meun1.Choose_proc(proc1.get_all_proc_name())
# print meun1.Proc_sort(pl,0)

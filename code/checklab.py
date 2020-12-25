#!/usr/bin/env python3

# v0.1 (the first version)

# 原则
# 1. 依赖字符流传输信息
# 2. Keep Stupid 只使用python内置模块及linux常规指令来实现模块
# 3. 如果2无法满足，需内置到本项目或其它语言二进制程序(同时符合原则一)

# 统一检测模块
# 入口：{local|<remote>} 检测类型 类型参数 [...] 
# <remote>: remote,<hostname>,<user>,<password>,[<port>]
# 出口: 暂定 yes | <other>

import os
import sys
import random
import string
import paramiko

# os.chdir('/usr/local/checklab/code')
check_module = sys.argv[2].replace('.', '/')
check_param = ' '.join(sys.argv[3:])


class Remotecheck:
    # TODO: 后续以trans的方式实现
    def __init__(self, remoteinfo, check_module, check_param, workspece='/tmp/'):
        self.hostname = remoteinfo[0]
        self.username = remoteinfo[1]
        self.password = remoteinfo[2]
        self.execfile = workspece + ''.join(random.sample(string.ascii_letters + string.digits,12))
        try:
            self.port = remoteinfo[3]
        except IndexError:
            self.port = 22
        self.workspace = workspece
        self.check_module = check_module
        self.check_param = check_param


    # 暂时实现短连接，后续仔细考虑
    def execremote(self):
        try:
            client = paramiko.client.SSHClient()
            # TODO: 后续需调整为任何主机
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
            client.exec_command('chmod +x ' + self.execfile)
            execcommand = self.execfile + ' ' + self.check_param
            stdin, stdout, stderr = client.exec_command(execcommand)
            # 与下面的finally配合，可能存在bug
            # 对bytes类型进行转换
            print(stdout.read().decode())
        finally:
            stdio, stdout, stderr = client.exec_command('rm -f ' + self.execfile)
            client.close()

    # 未考虑｜未验证 KeyPolicy，暂修改客户机 ssh_config
    # 暂时传递所有modules
    def scpremote(self):
        try:
            t = paramiko.Transport((self.hostname, self.port))
            t.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            local_path = 'modules/' + self.check_module
            sftp.put(local_path, self.execfile)
        finally:
            t.close()

    def exec(self):
        self.scpremote()
        self.execremote()

class Localcheck:
    def __init__(self, check_module, check_param):
        self.check_module = check_module
        self.check_param = check_param
    def exec(self):
        os.system('modules/' + self.check_module + ' ' + self.check_param)



# 判断本地还是远端执行
# 由变量"isremote"呈现
# TODO: 暂时不考虑reomote含local字符串
hostlocation = sys.argv[1]
if 'local' in hostlocation:
    check = Localcheck(check_module, check_param)
else:
    remoteinfo = hostlocation.split(',')[1:]
    check = Remotecheck(remoteinfo, check_module, check_param)

check.exec()
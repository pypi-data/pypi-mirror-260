#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@time   : 2020/10/20 19:13
@file   : shell.py
@author : 
@desc   : 
@exec   : 
"""
import subprocess
import sys


class Shell(object):
    def __init__(self, target_ip, target_port='22'):
        if not target_ip:
            sys.exit("IP can not empty!")
        self.target_ip = target_ip
        self.target_port = target_port

    @staticmethod
    def run(exec_cmd, is_exit=False):
        """
        传入shell脚本，默认执行报错不退出当前执行脚本。
        :param exec_cmd:
        :param is_exit:
        :return:
        """
        r_shell = subprocess.Popen(
            exec_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = r_shell.communicate()
        r_code = r_shell.returncode
        if r_code == 0:
            return stdout.strip().decode('utf8'), r_code
        else:
            err_msg = 'failed cmd: {cmd}\n{err}'.format(
                err=stderr.decode(), cmd=exec_cmd)
            if is_exit:
                sys.exit(err_msg)
            else:
                return err_msg, r_code

    def run_cmd(self, cmd):
        rd, rc = Shell.run(cmd)
        # print(cmd)
        if rc == 0:
            if rd == "0":
                return 0
            else:
                return 1
        else:
            sys.exit("Check exists failed!")

    def file_exists(self, target_path, file_type) -> int:
        cmd = f"ssh -p{self.target_port} {self.target_ip}  \"if [ -{file_type} '{target_path}' ]; " \
              f"then echo 1; else echo 0; fi;\""
        # print(cmd)
        return self.run_cmd(cmd)

    def cron_exists(self, corn_keyword) -> int:
        cmd = f"ssh -p{self.target_port} {self.target_ip} \"cat /var/spool/cron/root | grep '{corn_keyword}' | wc -l;\""
        return self.run_cmd(cmd)

    def pid_exists(self, prc):
        cmd = f"ssh -p{self.target_port} {self.target_ip} \"ps -ef | grep '{prc}'| grep -v 'grep' | wc -l;\""
        # print(cmd)
        return self.run_cmd(cmd)

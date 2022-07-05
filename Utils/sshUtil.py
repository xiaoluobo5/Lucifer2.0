#!/usr/bin/python
# -*-coding:utf-8 -*-
import json
import os
import re
import subprocess
import time

import paramiko
from PyQt5.QtCore import pyqtSignal, QThread


class SSHConnection(QThread, object):
    _signalSSH = pyqtSignal(str)

    def __init__(self, host='169.254.1.32', port=22, username='root', pwd='123456'):
        super(SSHConnection, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        # self.username = 'radish'
        self.pwd = pwd
        self.__k = None
        self.ssh = ''

    def connect(self):
        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.pwd)
            self.__transport = transport
            return True
        except:
            return False

    def close(self):
        self.__transport.close()
        del self

    def upload(self, local_path, target_path):
        # file_name = self.create_file()
        try:
            sftp = paramiko.SFTPClient.from_transport(self.__transport)
            return sftp.put(local_path, target_path)
        except IOError:
            print("fail..")

    def download(self, remote_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode('utf-8')
        # print(result.strip("\n"))
        print(result)
        return result

    def reboot(self):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        ssh.exec_command("reboot", get_pty=True)

    def setIp(self, target):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        ssh.exec_command("echo {} > /boot/ip_addr.conf".format(target))
        stdin, stdout, stderr = ssh.exec_command("cat /boot/ip_addr.conf")
        if stderr:
            return stderr
        ret = stdout.read().decode('utf-8')
        print(ret)
        return True if str(ret).strip("\n") == str(target) else False

    def exe_invoke(self, cmd, end_str=None):
        """
        交互式执行命令，和exe实现功能相同。执行出错的时候可以尝试
        :param cmd:
        :param end_str: 通过该字段判断命令是否结束
        :param delaytime:
        :return:
        """
        try:
            ssh = paramiko.SSHClient()
            ssh._transport = self.__transport
            ssh.get_pty()
            ssh.invoke_shell()
            ssh.send(cmd + '\n')
            ret = ""
            while True:
                out = ssh.recv(1024)
                # print(out.decode('utf-8'))
                ret = ret + out.decode('utf-8').replace('\r', '')
                if end_str in out.decode('utf-8'):
                    break
            return ret
        except Exception as e:
            # log(e)
            return 'Exception no return'

    def cmd2(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        while not stdout.channel.exit_status_ready():
            result = stdout.readline().strip("\n")
            print(result)
            self._signalSSH.emit(result)
            # 由于在退出时，stdout还是会有一次输出，因此需要单独处理，处理完之后，就可以跳出了
            if stdout.channel.exit_status_ready():
                ret = stdout.readlines()
                if ret:
                    print("!!!!")
                    print(ret.strip("\n"))
                    print("!!!!")
                break

    def restarService(self):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin1, stdout1, stderr1 = ssh.exec_command("killall -9 python")
        # context = con.cmd("sh /mix/lynx/script/start.sh")
        # stdin, stdout, stderr = ssh.exec_command("sh /mix/lynx/script/start.sh", get_pty=True)
        stdin, stdout, stderr = ssh.exec_command("sh /mix/lynx/launcher/run_launcher.sh", get_pty=True)
        while not stdout.channel.exit_status_ready():
            result = stdout.readline().strip("\n")
            print(result)
            # 由于在退出时，stdout还是会有一次输出，因此需要单独处理，处理完之后，就可以跳出了
            if stdout.channel.exit_status_ready():
                a = stdout.readlines()
                print(a)
                break
        # for line in stdout:
        #     print(line.strip("\n"))


def get_mix_version(ip):
    con = SSHConnection(ip)
    flag = con.connect()
    if flag:
        context = con.cmd("cat /mix/version.json")
        # context = con.cmd("cat /home/radish/Desktop/mix/version.json")
        con.close()
        if context:
            json_text = context[context.index("{"):context.index("}") + 1]
            mix_version_dict = json.loads(json_text)
            return mix_version_dict["MIX_FW_PACKAGE"]
        else:
            return False
    else:
        return False


def _ping_ip(_ip):
    cmd = "ping -t 1 {}".format(_ip)
    ipconfig_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    ipstr = r'64 bytes from ([0-9]{1,3}\.){3}[0-9]{1,3}.*'
    output = ipconfig_process.stdout.read()
    ip_pattern = re.compile(ipstr)
    for i in re.finditer(ip_pattern, str(output)):
        r = i.group()
        if r:
            return True
    return False


def check_firmware(firmware):
    if not os.path.exists(firmware):
        print("No {}".format(firmware))
        return None, None
    if os.path.isdir(firmware):
        print("{} is a directory, not a file".format(firmware))
        return None, None
    file_name = os.path.split(firmware)[1]
    match_result = re.match(r"MIX_FW_.*_(\d+).tgz", file_name)
    # match_result = re.match(r"MIX_FW_X\d+_\w{3}_\w+_(\d{3}).tgz", file_name)
    if match_result is not None and match_result.group(0) == file_name:
        md5 = re.match(r'MD5 .* = (\w+)', os.popen('md5 {}'.format(firmware)).read()).group(1)
        print(file_name, match_result.group(1), md5)
        return match_result.group(1), md5
    else:
        print("{} is a invalid firmware".format(firmware))
        return None, None


def upload_firmware(ip, firmware, md5):
    _, file_name = os.path.split(firmware)
    target_path = r"/var/fw_update/upload/"
    # target_path = "/home/radish/Desktop/"
    target_file = target_path + file_name
    con = SSHConnection(ip)
    con.connect()
    con.upload(firmware, target_file)
    for i in range(10):
        fw_md5_info = con.cmd("md5sum {}".format(target_file))
        if re.match(r'([0-9a-f]+)  {}'.format(target_file), fw_md5_info).group(1) == md5:
            return "upload done"
            break
        time.sleep(0.5)
    else:
        return "upload fail"
    con.close()


def update_ioMap(ip, filePath):
    if not os.path.exists(filePath):
        print("No {}".format(filePath))
        return "No {}".format(filePath)
    if os.path.isdir(filePath):
        print("{} is a directory, not a file".format(filePath))
        return "{} is a directory, not a file".format(filePath)
    file_name = os.path.split(filePath)[1]
    if file_name:
        md5 = re.match(r'MD5 .* = (\w+)', os.popen('md5 {}'.format(filePath)).read()).group(1)
        print(file_name, md5)

        target_path = "/mix/addon/test_function/"
        # target_path = "/home/radish/Desktop/"
        target_file = target_path + file_name
        con = SSHConnection(ip)
        if con.connect():
            if con.upload(filePath, target_file):
                for i in range(10):
                    fw_md5_info = con.cmd("md5sum {}".format(target_file))
                    if re.match(r'([0-9a-f]+)  {}'.format(target_file), fw_md5_info).group(1) == md5:
                        con.reboot()
                        return "upload done"
                        break
                    time.sleep(0.5)
            con.close()
            return "upload \"io_map.json\" fail"
        else:
            return "connected xavier fail"
    else:
        print("{} is a invalid file".format(filePath))
        return "{} is a invalid file".format(filePath)


def xavier_reboot(ip):
    con = SSHConnection(ip)
    con.connect()
    con.cmd('reboot')
    con.close()


# def restarService(ip):
#     _signalMsg2 = pyqtSignal(str)
#     con = SSHConnection(ip)
#     con.connect()
#     con.cmd("killall -9 python")
#     # context = con.cmd("sh /mix/lynx/script/start.sh")
#     stdin, stdout, stderr = con.exec_command("sh /mix/lynx/script/start.sh", get_pty=True)
#     while not stdout.channel.exit_status_ready():
#         result = stdout.readline().strip("\n")
#         print(result)
#         _signalMsg2.emit(result)
#         # 由于在退出时，stdout还是会有一次输出，因此需要单独处理，处理完之后，就可以跳出了
#         if stdout.channel.exit_status_ready():
#             a = stdout.readlines()
#             print(a)
#             _signalMsg2.emit(a)
#             break
#     con.close()


if __name__ == "__main__":

    _file = '/Users'
    fileName = "12"

    # IP = "192.168.101.1"
    IP = "172.16.180.130"
    if _ping_ip(IP):
        print("target Ip is:{}".format(IP))
    else:
        raise RuntimeError("Can not connected,please check it".format(IP))
    rpc = SSHConnection(host=IP, username='radish')
    print(rpc)
    if rpc:
        rpc.connect()
        # print(rpc.cmd("rm -rf /var/log/rpc_log/*"))
        # rpc.upload(_file, "/var/fw_update/upload/{}".format(fileName))
        # print("Upload MIX_FW finished,update now...please wait about 3 min,Do not power off")

        # update_result = rpc.cmd("sh /mix/script/update.sh")
        # update_result = rpc.exe_invoke("python3 /home/radish/Desktop/untitled.py")
        b = rpc.upload("/Users/radish/Desktop/DFU.zip", "/home/radish/Desktop/DFU.zip")
        print(b)
        update_result = rpc.cmd2("python3 /home/radish/Desktop/untitled.py")
        # print(update_result)
        if update_result:
            print("Firmware Update finished.")
            print("now reboot....")
            # rpc.cmd("reboot")
        rpc.close()

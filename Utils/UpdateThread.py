import os
import re
import time
import paramiko
from PyQt5.QtCore import QThread, pyqtSignal

from Utils.sshUtil import _ping_ip, check_firmware, update_ioMap


class UpDateThreadS(QThread):
    _signalBtn = pyqtSignal()
    _signalMsg = pyqtSignal(str, int)

    def __init__(self, ip, filePath, fileName):
        super(UpDateThreadS, self).__init__()
        self.ip = ip
        self.host = ip
        self.port = 22
        self.username = 'root'
        # self.username = 'radish'
        self.pwd = '123456'
        self.__k = None
        self.filePath = filePath
        self.fileName = fileName
        self.updateFlag = 0

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()
        del self

    def upload(self, local_path, target_path):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.__transport)
            sftp.put(local_path, target_path)
        except:
            return False
        return True

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode('utf-8')
        # print(result.strip("\n"))
        return result

    def upload_firmware(self, firmware, md5):
        _, file_name = os.path.split(firmware)
        target_path = r"/var/fw_update/upload/"
        # target_path = "/home/radish/Desktop/"
        target_file = target_path + file_name
        # ssh = paramiko.SSHClient()
        # ssh._transport = self.__transport
        if self.upload(firmware, target_file):
            for i in range(10):
                fw_md5_info = self.cmd("md5sum {}".format(target_file))
                if re.match(r'([0-9a-f]+)  {}'.format(target_file), fw_md5_info).group(1) == md5:
                    return "upload done"
                    break
                time.sleep(0.5)
            else:
                return "upload fail"
        else:
            return "Upload '{}' to Xavier fail!".format(file_name)

    def run(self):
        if _ping_ip(self.ip):
            msg = "Target Ip is:{}".format(self.ip)
            print(msg)
            if "MIX_FW" in self.fileName:
                version, md5 = check_firmware(self.filePath)
                if version and md5:
                    command = "/mix/lynx/script/update.sh"
                    # command = "/home/radish/Desktop/mix/ttt.sh"
                    try:
                        ssh = paramiko.SSHClient()
                        transport = paramiko.Transport((self.host, self.port))
                        transport.connect(username=self.username, password=self.pwd)
                        ssh._transport = transport
                        self.__transport = transport
                        self._signalMsg.emit("Uploading......", -1)
                    except:
                        self._signalMsg.emit("{} login fail!".format(self.host), 0)
                    ret = self.upload_firmware(self.filePath, md5)
                    if ret == "upload done":
                        msg = "upload \"{}\" done!".format(self.fileName)
                        self._signalMsg.emit(msg, 1)
                        # flagStr = " - Success - '{}' Firmware Update finished.".format(self.fileName)
                        flagStr = r"- Success - '{}' Firmware Update finished.".format(self.fileName)
                        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                        while not stdout.channel.exit_status_ready():
                            result = stdout.readline().strip()
                            if result:
                                print(result)
                                self._signalMsg.emit(result, -1)
                                if re.search(flagStr, str(result).strip()):
                                    print("@@@@@:normalRet")
                                    self.updateFlag = 1
                                    self._signalMsg.emit("{} Update OK!".format(self.fileName), 1)
                                    break
                            # 由于在退出时，stdout还是会有一次输出，因此需要单独处理，处理完之后，就可以跳出了
                            if stdout.channel.exit_status_ready():
                                lastRet = stdout.readlines()
                                print("@@@@@:lastRet")
                                if lastRet:
                                    for x in range(len(lastRet)):
                                        ret = lastRet[x]
                                        if ret and ret.strip():
                                            print(ret.strip())
                                            self._signalMsg.emit(ret.strip(), -1)
                                            if re.search(flagStr, ret):
                                                self.updateFlag = 1
                                                self._signalMsg.emit("{} Update OK!".format(self.fileName), 1)
                                            else:
                                                pass
                                        else:
                                            pass
                                else:
                                    pass
                                break
                        if self.updateFlag == 1:
                            self.updateFlag = 0
                            time.sleep(1)
                            msg2 = "Xavier {} Restarting...".format(self.ip)
                            print(msg2)
                            self._signalMsg.emit(msg2, 1)
                            ssh.exec_command("reboot", get_pty=True)
                            time.sleep(1)
                            ssh.close()
                        else:
                            msg = "Xavier update Fail!!!"
                            self._signalMsg.emit(msg, 0)
                    else:
                        self._signalMsg.emit(ret, 0)
                    time.sleep(1)
                    ssh.close()
                else:
                    self._signalMsg.emit("The MIX_FW is invalid!", 0)
            elif 'io_map.json' == self.fileName:
                ret = update_ioMap(self.ip, self.filePath)
                if "upload done" == ret:
                    self._signalMsg.emit("Upload io_map.json OK! Xavier Restarting...", 1)
                else:
                    self._signalMsg.emit(ret, 0)
            else:
                self._signalMsg.emit("Input file is invalid!", 0)
            self._signalBtn.emit()
        else:
            self._signalMsg.emit("Failed to connect {}".format(self.ip), 0)
            self._signalBtn.emit()

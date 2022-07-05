import os
import time
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal

from Utils.common import ping_xavier
from Utils.sshUtil import _ping_ip, SSHConnection, get_mix_version, check_firmware, upload_firmware


class Thread_setIp(QThread):  # 线程2
    _signalBtn = pyqtSignal()
    _signalMsg = pyqtSignal(str, int)

    def __init__(self, ip, target):
        super().__init__()
        self.ip = ip
        self.target = target

    def run(self):
        if _ping_ip(self.ip):
            msg = "Target Ip is:{}".format(self.ip)
            print(msg)
            # self._signalMsg.emit(msg)
            rpc = SSHConnection(host=self.ip)
            rpc.connect()
            flag = rpc.setIp(self.target)
            if flag:
                self._signalMsg.emit("Xavier {} change ip to {} OK!".format(self.ip, self.target), 1)
            else:
                self._signalMsg.emit("Xavier {} change ip Fail!".format(self.ip), 0)
            self._signalBtn.emit()
            time.sleep(1)
            rpc.close()
        else:
            self._signalMsg.emit("Failed to connect {}".format(self.ip), 0)
            self._signalBtn.emit()


class Thread_ping(QThread):
    _signal = pyqtSignal()
    _signal2 = pyqtSignal(str, int)

    def __init__(self, ip):
        super(Thread_ping, self).__init__()
        self.ipaddr = ip

    def run(self):
        bRet = ping_xavier(self.ipaddr, 3)
        if bRet:
            self._signal2.emit("Ping {} Succeed!".format(self.ipaddr), 1)
        else:
            self._signal2.emit("Ping {} FAIL".format(self.ipaddr), 0)
        self._signal.emit()


class Thread_mixReboot(QThread):
    _signalBtn = pyqtSignal()
    _signalMsg = pyqtSignal(str, int)

    def __init__(self, ip):
        super(Thread_mixReboot, self).__init__()
        self.ip = ip

    def run(self):
        if _ping_ip(self.ip):
            msg = "Target Ip is:{}".format(self.ip)
            print(msg)
            # self._signalMsg.emit(msg)
            rpc = SSHConnection(host=self.ip)
            if rpc:
                if rpc.connect():
                    rpc.reboot()
                    msg = "Xavier {} Restarting...".format(self.ip)
                    print(msg)
                    self._signalMsg.emit(msg, 1)
                    time.sleep(1)
                    rpc.close()
                else:
                    msg = "connected xavier fail!!!"
                    print(msg)
                    self._signalMsg.emit(msg, 0)
            self._signalBtn.emit()
        else:
            self._signalMsg.emit("Failed to connect {}".format(self.ip), 0)
            self._signalBtn.emit()


class Thread_fwVersion(QThread):
    _signalBtn = pyqtSignal()
    _signalMsg = pyqtSignal(str, int)

    def __init__(self, ip):
        super(Thread_fwVersion, self).__init__()
        self.ip = ip

    def run(self):
        if _ping_ip(self.ip):
            msg = "Target Ip is:{}".format(self.ip)
            print(msg)
            # self._signalMsg.emit(msg)
            strRet = get_mix_version(self.ip)
            if strRet:
                self._signalMsg.emit("MIX_FW version is:{}".format(strRet), 1)
            else:
                self._signalMsg.emit("Get MIX_FW version fail!", 0)
            self._signalBtn.emit()
        else:
            self._signalMsg.emit("Failed to connect {}".format(self.ip), 0)
            self._signalBtn.emit()


class Thread_Update(QThread):
    _signalBtn = pyqtSignal()
    _signalMsg = pyqtSignal(str,int)

    def __init__(self, ip, filePath):
        super(Thread_Update, self).__init__()
        self.ip = ip
        self.filePath = filePath
        self.fileName = ''

    def handleMsg(self, msg):
        self._signalMsg.emit(msg)

    def run(self) -> None:
        if _ping_ip(self.ip):
            msg = "Target Ip is:{}".format(self.ip)
            print(msg)
            # self._signalMsg.emit(msg)
            version, md5 = check_firmware(self.filePath)
            ret = upload_firmware(self.ip, self.filePath, md5)
            if ret == "upload done":
                rpc = SSHConnection(host=self.ip)
                rpc.connect()
                rpc.cmd2("/mix/lynx/script/update.sh")
                self.rpc._signalSSH.connect(self.handleMsg)
            self._signalMsg.emit(ret)
            self._signalBtn.emit()
        else:
            msg = "Can not connected {},please check it".format(self.ip)
            print(msg)
            self._signalMsg.emit(msg)
            self._signalBtn.emit()


class Thread_RestarServer(QThread):
    _signalBtn = pyqtSignal()
    _signalMsg = pyqtSignal(str)

    def __init__(self, ip):
        super(Thread_RestarServer, self).__init__()
        self.ip = ip

    def run(self) -> None:
        if _ping_ip(self.ip):
            msg = "Target Ip is:{}".format(self.ip)
            print(msg)
            # self._signalMsg.emit(msg)
            # con = SSHConnection(self.ip)
            # con.connect()
            # con.cmd("killall -9 python")
            # stdin, stdout, stderr = con.connect().exec_command("sh /mix/lynx/script/start.sh", get_pty=True)
            # while not stdout.channel.exit_status_ready():
            #     result = stdout.readline().strip("\n")
            #     print(result)
            #     self._signalMsg.emit(result)
            #     if stdout.channel.exit_status_ready():
            #         a = stdout.readlines()
            #         print(a)
            #         self._signalMsg.emit(a)
            #         break
            # con.close()
            rpc = SSHConnection(host=self.ip)
            rpc.connect()
            rpc.restarService()
            self._signalBtn.emit()
        else:
            self._signalMsg.emit("Failed to connect {}".format(self.ip))
            self._signalBtn.emit()

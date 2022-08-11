import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from GUI.LuciferTool2 import Ui_Lucifer
from Resources.StreamLite import StreamLite
from Resources.configLoader import getIpConfig
from Utils.UpdateThread import UpDateThreadS
from Utils.common import check_ip_valid
from Utils.bt_Thread import Thread_ping, Thread_setIp, Thread_mixReboot, Thread_fwVersion, \
    Thread_RestarServer


class main(QMainWindow, Ui_Lucifer):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setupUi(self)
        self.fixture = ""
        self.msg = ""
        self.fixtureflag = 0
        self.fixtureLockFlag = 0
        self.connectedIp = ''
        self.XavierUpdateFlag = 0
        self.ipConfig1, self.ipConfig2 = getIpConfig()
        self.Xavier1.setText(self.ipConfig1)
        self.Xavier2.setText(self.ipConfig2)
        self.Fixture1.setText(self.ipConfig1)
        self.Fixture2.setText(self.ipConfig2)

    @QtCore.pyqtSlot()
    def on_ConnectFixture_clicked(self):
        if self.Fixture1.isChecked() or self.Fixture2.isChecked():
            if self.Fixture1.isChecked():
                # ip = "192.168.50.99"
                ip = self.ipConfig1
            else:
                ip = self.ipConfig2
            if self.fixtureflag == 1:
                # self.fixture.__del__()
                self.ConnectFixture.setText("Connect")
                self.handleMsgBox("{} Disconnect!".format(self.connectedIp), 0)
                self.fixtureflag = 0
                self.fixture = ""
                self.IN_Sensor.setStyleSheet("background:rgba(255, 255, 255, 0)")
                self.OUT_Sensor.setStyleSheet("background:rgba(255, 255, 255, 0)")
                self.Up_Sensor.setStyleSheet("background:rgba(255, 255, 255, 0)")
                self.DOWN_Sensor.setStyleSheet("background:rgba(255, 255, 255, 0)")
                self.Fixture_lock.setText("FixtureLock")

            else:
                self.fixture = StreamLite(ip)
                if self.fixture:
                    ret = self.fixture.getConnectFlag()
                    if ret == 1:
                        self.ConnectFixture.setText("Disconnect")
                        self.fixtureflag = 1
                        self.connectedIp = ip
                        self.handleMsgBox("{} Connected OK!".format(ip), 1)
                    else:
                        self.fixture = ""
                        self.handleMsgBox("{} Connected fail!".format(ip), 0)
        else:
            msg = "Please select an IP address first"
            print(msg)
            self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_CheckFanSpeed1_clicked(self):
        if self.fixtureflag == 1:
            for x in range(1, 7):
                fan = (self.fixture.getFanSpeed(x))
                if fan:
                    msg = "Fan[{}] Speed is：{}".format(x, str(fan, 'utf-8'))
                    self.handleMsgBox(msg, -1)
                else:
                    self.handleMsgBox("Get Fan Speed Fail!", 0)
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)
            # To do alert !

    @QtCore.pyqtSlot()
    def on_CheckFanSpeed2_clicked(self):
        if self.fixtureflag == 1:
            for x in range(7, 13):
                fan = (self.fixture.getFanSpeed(x))
                if fan:
                    msg = "Fan[{}] Speed is：{}".format(x, str(fan, 'utf-8'))
                    self.handleMsgBox(msg, -1)
                else:
                    self.handleMsgBox("Get Fan Speed Fail!", 0)
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_CheckDUTSensor_clicked(self):
        if self.fixture != "":
            print(self.fixture)
            ret = self.fixture.checkDUTSensor()
            if ret:
                msg = str(ret, 'utf-8')
                status = 1 if msg=="dut_sensor_on" else 0
                self.handleMsgBox(msg,status)
            else:
                # TO DO
                print(ret)
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_Fixture_init_clicked(self):
        if self.fixture != "":
            print(self.fixture)
            ret = self.fixture.initialFixture()
            if ret:
                msg = "Fixture init OK!"
                self.handleMsgBox(msg, 1)
            else:
                msg = "Fixture init Fail!"
                self.handleMsgBox(msg, 0)
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_CheckFixtureSensor_clicked(self):
        if self.fixture != "":
            ret = self.fixture.checkPositionSensor()
            if ret:
                ret = ret.split(";")
                if int(ret[0]) == 1:
                    self.IN_Sensor.setStyleSheet("background:rgb(89, 255, 62)")
                else:
                    self.IN_Sensor.setStyleSheet("background:rgba(255, 255, 255, 0)")
                if int(ret[1]) == 1:
                    self.OUT_Sensor.setStyleSheet("background:rgb(89, 255, 62)")
                else:
                    self.OUT_Sensor.setStyleSheet("background:rgba(255, 255, 255, 0)")
                if int(ret[2]) == 1:
                    self.Up_Sensor.setStyleSheet("background:rgb(89, 255, 62)")
                else:
                    self.Up_Sensor.setStyleSheet("background:rgba(255, 255, 255, 0)")
                if int(ret[3]) == 1:
                    self.DOWN_Sensor.setStyleSheet("background:rgb(89, 255, 62)")
                else:
                    self.DOWN_Sensor.setStyleSheet("background:rgba(255, 255, 255, 0)")
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_Fixture_UP_clicked(self):
        if self.Fixture_UP.isEnabled():
            if self.fixture != "":
                # print(self.fixture)
                ret = self.fixture.trayUp()
                if ret:
                    msg = "Fixture trayUp OK!"
                    self.handleMsgBox(str(ret, 'utf-8'))
                else:
                    msg = "Fixture trayUp Fail!"
                    self.handleMsgBox(msg, 0)
            else:
                msg = "Fixture not connected!"
                self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_Fixture_DOWN_clicked(self):
        if self.fixture != "":
            ret = self.fixture.trayDown()
            if ret:
                msg = "Fixture trayDown OK!"
                self.handleMsgBox(str(ret, 'utf-8'))
            else:
                msg = "Fixture trayDown Fail!"
                self.handleMsgBox(msg, 0)
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_Fixture_IN_clicked(self):
        if self.fixture != "":
            ret = self.fixture.trayIn()
            if ret:
                # msg = "Fixture trayIN OK!"
                self.handleMsgBox(str(ret, 'utf-8'))
            else:
                msg = "Fixture trayIn Fail!"
                self.handleMsgBox(msg, 0)
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_Fixture_OUT_clicked(self):
        if self.fixture != "":
            ret = self.fixture.trayOut()
            if ret:
                msg = "Fixture trayOut OK!"
                self.handleMsgBox(str(ret, 'utf-8'))
            else:
                msg = "Fixture Out Fail!"
                self.handleMsgBox(msg, 0)
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)

    @QtCore.pyqtSlot()
    def on_Fixture_lock_clicked(self):
        if self.fixture != "":
            if self.fixtureLockFlag == 0:
                ret = self.fixture.fixtureLock("on")
                if ret:
                    self.handleMsgBox(str(ret, 'utf-8'))
                    if str(ret, 'utf-8') in "magnet control done":
                        self.Fixture_lock.setText("Magnet:ON")
                        self.fixtureLockFlag = 1
                else:
                    msg = "Fixture fixtureLock Fail!"
                    self.handleMsgBox(msg, 0)
            else:
                ret = self.fixture.fixtureLock("off")
                if ret:
                    self.handleMsgBox(str(ret, 'utf-8'))
                    if str(ret, 'utf-8') in "magnet control done":
                        self.Fixture_lock.setText("Magnet:OFF")
                        self.fixtureLockFlag = 0
                else:
                    msg = "Fixture fixtureLock Fail!"
                    self.handleMsgBox(msg, 0)
        else:
            msg = "Fixture not connected!"
            self.handleMsgBox(msg, 0)

    def choseIp(self):
        if self.Xavier1.isChecked() or self.Xavier2.isChecked():
            return self.ipConfig1 if self.Xavier1.isChecked() else self.ipConfig2
            # return "10.0.200.11" if self.Xavier1.isChecked() else "10.0.200.21"
        else:
            msg = "Please chose an ip address!"
            print(msg)
            self.handleDisplay(msg, 0)
            return ""

    def handleDisplay(self, msg, status=-1):
        if status == 0:
            msg = "<font color='red'>{}<font>".format(msg)
        elif status == 1:
            msg = "<font color='green'>{}<font>".format(msg)
        else:
            msg = "<font color='black'>{}<font>".format(msg)
        self.textBrowser.append(msg)

    def handleMsgBox(self, msg, status=-1):
        if status == 0:
            msg = "<font color='red'>{}<font>".format(msg)
        elif status == 1:
            msg = "<font color='green'>{}<font>".format(msg)
        else:
            msg = "<font color='black'>{}<font>".format(msg)
        self.MsgBox.append(msg)

    @QtCore.pyqtSlot()
    def on_bt_Update_clicked(self):
        ip = self.choseIp()
        if ip and self.textBrowser.filepath and self.textBrowser.fileName:
            self.XavierUpdateFlag = 1
            self.bt_Update.setEnabled(False)
            self.bt_Reboot.setEnabled(False)
            self.thread_upDate = UpDateThreadS(ip, self.textBrowser.filepath, self.textBrowser.fileName)
            self.thread_upDate._signalBtn.connect(self.set_bt_Update)
            self.thread_upDate._signalMsg.connect(self.handleDisplay)
            self.thread_upDate.start()
        else:
            self.handleDisplay("Please put the file to here first!", 0)

    def set_bt_Update(self):
        self.XavierUpdateFlag = 0
        self.bt_Update.setEnabled(True)
        self.bt_Reboot.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_bt_Ping_clicked(self):
        ip = self.choseIp()
        if ip:
            self.bt_Ping.setEnabled(False)
            self.thread_ping = Thread_ping(ip)
            self.thread_ping._signal.connect(self.set_bt_Ping)
            self.thread_ping._signal2.connect(self.handleDisplay)
            self.thread_ping.start()

    def set_bt_Ping(self):
        self.bt_Ping.setEnabled(True)

    # @QtCore.pyqtSlot()
    # def on_bt_getMix_clicked(self):
    #     ip = self.choseIp()
    #     if ip:
    #         self.bt_getMix.setEnabled(False)
    #         self.thread_4 = Thread_4(ip)
    #         self.thread_4._signal.connect(self.set_bt_getMix)
    #         self.thread_4._signalMsg.connect(self.handleDisplay)
    #         self.thread_4.start()

    def set_bt_getMix(self):
        self.bt_getMix.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_bt_setip_clicked(self):
        ip = self.choseIp()
        if ip:
            if self.line_ip.text():
                target = self.line_ip.text().strip()
                if check_ip_valid(target):
                    self.bt_setip.setEnabled(False)
                    self.thread_setIp = Thread_setIp(ip, target)
                    self.thread_setIp._signalBtn.connect(self.set_bt_setip)
                    self.thread_setIp._signalMsg.connect(self.handleDisplay)
                    self.thread_setIp.start()
                else:
                    self.handleDisplay("The IP address is invalid!", 0)
            else:
                msg = "Please enter an ip !"
                self.handleDisplay(msg, 0)

    def set_bt_setip(self):
        self.bt_setip.setEnabled(True)
        # self.textBrowser.append(str)

    @QtCore.pyqtSlot()
    def on_bt_Reboot_clicked(self):
        ip = self.choseIp()
        if ip:
            self.bt_Reboot.setEnabled(False)
            self.thread_mixReboot = Thread_mixReboot(ip)
            self.thread_mixReboot._signalBtn.connect(self.set_bt_Reboot)
            self.thread_mixReboot._signalMsg.connect(self.handleDisplay)
            self.thread_mixReboot.start()

    def set_bt_Reboot(self):
        self.bt_Reboot.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_bt_FwVersion_clicked(self):
        ip = self.choseIp()
        if ip:
            self.bt_FwVersion.setEnabled(False)
            self.thread_fwVersion = Thread_fwVersion(ip)
            self.thread_fwVersion._signalBtn.connect(self.set_bt_FwVersion)
            self.thread_fwVersion._signalMsg.connect(self.handleDisplay)
            self.thread_fwVersion.start()

    def set_bt_FwVersion(self):
        self.bt_FwVersion.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_bt_RestartServer_clicked(self):
        ip = self.choseIp()
        if ip:
            self.bt_RestartServer.setEnabled(False)
            self.bt_Update.setEnabled(False)
            self.thread_RestarServer = Thread_RestarServer(ip)
            self.thread_RestarServer._signalBtn.connect(self.set_bt_RestartServer)
            self.thread_RestarServer._signalMsg.connect(self.handleDisplay)
            self.thread_RestarServer.start()

    def set_bt_RestartServer(self):
        self.bt_RestartServer.setEnabled(True)
        self.bt_Update.setEnabled(True)

    def closeEvent(self, event):
        if self.XavierUpdateFlag == 1:
            QMessageBox.warning(self, "Warning", "<font color='red'>Xavier is updating, Don't close!<font>", QMessageBox.Cancel)
            event.ignore()
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = main()
    MainWindow.show()
    sys.exit(app.exec_())

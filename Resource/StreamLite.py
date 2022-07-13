from Resource.cfixture import *


class StreamLite:
    def __init__(self, strIP):
        self.strIp = strIP
        self.StreamLite = LibFixture(self.strIp)

    def __del__(self):
        self.StreamLite.delObj()

    def getConnectFlag(self):
        if self.StreamLite:
            strRecv = self.StreamLite.getConnectFlag()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def checkPositionSensor(self):
        if self.StreamLite:
            strRecv = self.StreamLite.checkPositionSensor()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def trayUp(self):
        if self.StreamLite:
            strRecv = self.StreamLite.trayUp()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def trayDown(self):
        if self.StreamLite:
            strRecv = self.StreamLite.trayDown()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def trayIn(self):
        if self.StreamLite:
            strRecv = self.StreamLite.trayIn()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def trayOut(self):
        if self.StreamLite:
            strRecv = self.StreamLite.trayOut()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def uut1Led(self, mode):
        if self.StreamLite:
            strRecv = self.StreamLite.uut1Led(mode)
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def uut2Led(self, mode):
        if self.StreamLite:
            strRecv = self.StreamLite.uut2Led(mode)
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def uut3Led(self, mode):
        if self.StreamLite:
            strRecv = self.StreamLite.uut3Led(mode)
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def uut4Led(self, mode):
        if self.StreamLite:
            strRecv = self.StreamLite.uut4Led(mode)
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def stateLed(self, mode):
        if self.StreamLite:
            strRecv = self.StreamLite.stateLed(mode)
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def checkDUTSensor(self):
        if self.StreamLite:
            strRecv = self.StreamLite.checkDUTSensor()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def fixtureLock(self, flag):
        if self.StreamLite:
            strRecv = self.StreamLite.fixtureLock(int(flag))
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def fixtureLock(self, state):
        if self.StreamLite:
            strRecv = self.StreamLite.fixtureLock(str(state))
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def setFanSpeed(self, nFanId, nSpeed):
        if self.StreamLite:
            strRecv = self.StreamLite.setFanSpeed(int(nFanId), int(nSpeed))
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def getFanSpeed(self, nFanId):
        if self.StreamLite:
            strRecv = self.StreamLite.getFanSpeed(int(nFanId))
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def initialFixture(self):
        if self.StreamLite:
            strRecv = self.StreamLite.initialFixture()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return strRecv

    def checkPositionSensor(self):
        if self.StreamLite:
            strRecv = self.StreamLite.checkPositionSensor()
        else:
            strRecv = "StreamLite Obj Didn't Create"
        return str(strRecv, 'utf-8')


if __name__ == '__main__':
    fixture = StreamLite("192.168.50.77")
    ret = fixture.checkDUTSensor()
    # ret = fixture.checkPositionSensor().split(";")
    print(str(ret, 'utf-8'))
    # print(ret)
    # print(fixture.setFanSpeed(1, 10))
    # print(fixture.getFanSpeed(1))
    # print(fixture.setFanSpeed(1, 50))
    # print(fixture.fixtureLock("ON"))

import ctypes
import os
import frozenPath

current_folder = os.path.abspath(os.path.dirname(__file__))
# FixturePluginPath = current_folder + '/libTestC.dylib'
app_path = frozenPath.app_path()
app_path = os.path.dirname(app_path)
FixturePluginPath = app_path + "/Frameworks/" + "libStreamLite.dylib"
# FixturePluginPath = "/Users/radish/Library/Caches/JetBrains/AppCode2021.1/DerivedData/StreamLite-bahsvlskcdwqemelworacmdnxqxp/Build/Products/Debug/libStreamLite.dylib"

libPy = ctypes.cdll.LoadLibrary(FixturePluginPath)

libPy.createStreamLiteDev.argtypes = [ctypes.c_char_p]
libPy.createStreamLiteDev.restype = ctypes.c_void_p

libPy.destroyStreamLiteDev.argtypes = [ctypes.c_void_p]

libPy.checkDUTSensor.argtypes = [ctypes.c_void_p]
libPy.checkDUTSensor.restype = ctypes.c_char_p

libPy.trayUp.argtypes = [ctypes.c_void_p]
libPy.trayUp.restype = ctypes.c_char_p

libPy.trayDown.argtypes = [ctypes.c_void_p]
libPy.trayDown.restype = ctypes.c_char_p

libPy.trayIn.argtypes = [ctypes.c_void_p]
libPy.trayIn.restype = ctypes.c_char_p

libPy.trayOut.argtypes = [ctypes.c_void_p]
libPy.trayOut.restype = ctypes.c_char_p

libPy.setIO.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
libPy.setIO.restype = ctypes.c_char_p

libPy.fixtureLock.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
libPy.fixtureLock.restype = ctypes.c_char_p

libPy.setFanSpeed.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
libPy.setFanSpeed.restype = ctypes.c_int

libPy.getFanSpeed.argtypes = [ctypes.c_void_p, ctypes.c_int]
libPy.getFanSpeed.restype = ctypes.c_char_p

libPy.initialFixture.argtypes = [ctypes.c_void_p]
libPy.initialFixture.restype = ctypes.c_bool

libPy.checkPositionSensor.argtypes = [ctypes.c_void_p]
libPy.checkPositionSensor.restype = ctypes.c_char_p

libPy.getConnectFlag.argtypes = [ctypes.c_void_p]
libPy.getConnectFlag.restype = ctypes.c_int


class LibFixture:
    """docstring for EowynDev"""

    def __init__(self, arg):
        arg = arg.encode("utf-8")
        self.Edev = libPy.createStreamLiteDev(arg)
        # print("Add StreamLiteDev Obj {}".format(self.Edev))

    def delObj(self):
        if self.Edev:
            libPy.destroyStreamLiteDev(self.Edev)
            return 1
        else:
            print("pyLibEdev.delObj Error")
            ret = -1
            return ret

    def getConnectFlag(self):
        if self.Edev:
            ret = libPy.getConnectFlag(self.Edev)
        else:
            print("pyLibEdev.fixtureLock Error")
            ret = -1
        return ret

    def checkDUTSensor(self):
        if self.Edev:
            ret = libPy.checkDUTSensor(self.Edev)
        else:
            print("pyLibEdev.checkDUTSensor Error")
            ret = -1
        return ret

    def trayUp(self):
        if self.Edev:
            ret = libPy.trayUp(self.Edev)
        else:
            print("pyLibEdev.trayUp Error")
            ret = -1
        return ret

    def trayDown(self):
        if self.Edev:
            ret = libPy.trayDown(self.Edev)
        else:
            print("pyLibEdev.trayDown Error")
            ret = -1
        return ret

    def trayIn(self):
        if self.Edev:
            ret = libPy.trayIn(self.Edev)
        else:
            print("pyLibEdev.trayIn Error")
            ret = -1
        return ret

    def trayOut(self):
        if self.Edev:
            ret = libPy.trayOut(self.Edev)
        else:
            print("pyLibEdev.trayOut Error")
            ret = -1
        return ret

    def setIO(self, io, state):
        if self.Edev:
            ret = libPy.setIO(self.Edev, io, state)
        else:
            print("pyLibEdev.setIO Error")
            ret = -1
        return ret

    # def trayOut(self):
    #     if self.Edev:
    #         libPy.trayOut(self.Edev)
    #         ret = 0
    #     else:
    #         print("pyLibEdev.trayOut Error")
    #         ret = -1
    #     return ret

    def fixtureLock(self, state):
        if self.Edev:
            state = state.encode("utf-8")
            ret = libPy.fixtureLock(self.Edev, state)
        else:
            print("pyLibEdev.fixtureLock Error")
            ret = -1
        return ret

    def setFanSpeed(self, nSpeed, nFanId):
        if self.Edev:
            # print("------setFanSpeed setFanSpeed setFanSpeed")
            ret = libPy.setFanSpeed(self.Edev, nSpeed, nFanId)
        else:
            print("pyLibEdev.setFanSpeed Error")
            ret = -1
        return ret

    def getFanSpeed(self, nFanId):
        if self.Edev:
            # print("------getFanSpeed---------")
            ret = libPy.getFanSpeed(self.Edev, nFanId)
        else:
            print("pyLibEdev.getFanSpeed Error")
            ret = -1
        return ret

    def initialFixture(self):
        if self.Edev:
            ret = libPy.initialFixture(self.Edev)
            # print(ret)
        else:
            print("pyLibEdev.initialFixture Error")
            ret = -1
        return ret

    def checkPositionSensor(self):
        if self.Edev:
            ret = libPy.checkPositionSensor(self.Edev)
        else:
            print("pyLibEdev.checkPositionSensor Error")
            ret = -1
        return ret

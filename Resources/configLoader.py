import configparser
import os

import frozenPath


def getIpConfig():
    app_path = frozenPath.app_path()
    app_path = os.path.dirname(app_path)
    configPath = app_path + "/Resources/" + "config.ini"
    if os.path.exists(configPath):
        config = configparser.ConfigParser()
        config.read(configPath)
        ipConfig1 = config.get("DATABASE", "fixture1")
        ipConfig2 = config.get("DATABASE", "fixture2")
    else:
        ipConfig1 = "10.0.200.11"
        ipConfig2 = "10.0.200.21"
    return ipConfig1, ipConfig2

import threading
from time import sleep
from dobot_utils import *

GlobalSpeed = 75  # Velocidad global del robot (0-100)

def DobotInit(ip: str, speed: int = GlobalSpeed):
    dashboard, move, feed = ConnectRobot(ip)
    dashboard.ClearError(); sleep(0.2)
    dashboard.EnableRobot()

    t_feed  = threading.Thread(target=GetFeed, args=(feed,), daemon=True)
    t_clear = threading.Thread(target=ClearRobotError, args=(dashboard,), daemon=True)
    t_feed.start(); t_clear.start()

    dashboard.SpeedFactor(speed)
    return dashboard, move, feed

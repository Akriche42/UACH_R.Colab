import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType,alarmAlarmJsonFile
from time import sleep
import numpy as np
import re

# Global variables (current coordinates)
current_actual = None
algorithm_queue = None
enableStatus_robot = None
robotErrorState = False
globalLockValue = threading.Lock()

def ConnectRobot(ip = "192.168.1.6"):
    try:
        #ip = "192.168.0.106" #cambie la IP
        dashboardPort = 29999
        movePort = 30003
        feedPort = 30004
        print("Establishing connection...")
        dashboard = DobotApiDashboard(ip, dashboardPort)
        move = DobotApiMove(ip, movePort)
        feed = DobotApi(ip, feedPort)
        print("Successful connection!")
        return dashboard, move, feed
    except Exception as e:
        print("Connection failed:")
        raise e

def MovLinear(move: DobotApiMove, point_list: list, verbose = True):  #Le cambie el nombre a MovLinear para no confundirlo con el MovL de DobotApiMove
    move.MovL(point_list[0], point_list[1], point_list[2], point_list[3])
    if verbose:
        print(f"Moving to point: {point_list}")

def MovJoint(move: DobotApiMove, point_list: list, verbose = True):  #Le cambie el nombre a MovLinear para no confundirlo con el MovL de DobotApiMove
    move.MovJ(point_list[0], point_list[1], point_list[2], point_list[3])
    if verbose:
        print(f"Moving to point: {point_list}")
        
def MovLinearSec(move: DobotApiMove, dashboard: DobotApiDashboard, point_list: list, z_secure = 170, verbose = True):
    initial_pose = getPoint(dashboard)
    move.MovL(initial_pose[0], initial_pose[1], z_secure, initial_pose[3])
    move.MovL(point_list[0], point_list[1], z_secure, point_list[3])
    move.MovL(point_list[0], point_list[1], point_list[2], point_list[3])
    if verbose:
        print(f"Moving to point with security: {point_list}") 
        
def RelMovLinear(move: DobotApiMove, point_list: list, verbose = True):  #Le cambie el nombre a RelMovLinear para no confundirlo con el RelMovL de DobotApiMove
    move.RelMovL(point_list[0], point_list[1], point_list[2], point_list[3])
    if verbose:
        print(f"Moving to point: {point_list}")

def limpiarEntradas(dashboard: DobotApiDashboard, numEntradas: int):
    for i in range(1, numEntradas + 1):
        dashboard.DO(i, 0)

def GetFeed(feed: DobotApi):
    global current_actual
    global algorithm_queue
    global enableStatus_robot
    global robotErrorState
    hasRead = 0
    while True:
        data = bytes()
        while hasRead < 1440:
            temp = feed.socket_dobot.recv(1440 - hasRead)
            if len(temp) > 0:
                hasRead += len(temp)
                data += temp
        hasRead = 0
        feedInfo = np.frombuffer(data, dtype=MyType)
        if hex((feedInfo['test_value'][0])) == '0x123456789abcdef':
            globalLockValue.acquire()
            # Refresh Properties
            current_actual = feedInfo["tool_vector_actual"][0]
            algorithm_queue = feedInfo['isRunQueuedCmd'][0]
            enableStatus_robot=feedInfo['EnableStatus'][0]
            robotErrorState= feedInfo['ErrorStatus'][0]
            globalLockValue.release()
        sleep(0.001)

def WaitArrive(point_list):
    while True:
        is_arrive = True
        globalLockValue.acquire()
        if current_actual is not None:
            for index in range(4):
                if (abs(current_actual[index] - point_list[index]) > 1):
                    is_arrive = False
            if is_arrive :
                globalLockValue.release()
                return
        globalLockValue.release()  
        sleep(0.001)

def ClearRobotError(dashboard: DobotApiDashboard):
    global robotErrorState
    dataController,dataServo =alarmAlarmJsonFile()    # 读取控制器和伺服告警码
    while True:
      globalLockValue.acquire()
      if robotErrorState:
                numbers = re.findall(r'-?\d+', dashboard.GetErrorID())
                numbers= [int(num) for num in numbers]
                if (numbers[0] == 0):
                  if (len(numbers)>1):
                    for i in numbers[1:]:
                      alarmState=False
                      if i==-2:
                          print("Machine alarm: machine collision", i)
                          alarmState=True
                      if alarmState:
                          continue                
                      for item in dataController:
                        if  i==item["id"]:
                            print("Machine alarm: Controller error id", i, item["en"]["description"])
                            alarmState=True
                            break 
                      if alarmState:
                          continue
                      for item in dataServo:
                        if  i==item["id"]:
                            print("Machine alarm: Controller error id", i, item["en"]["description"])
                            break  
                       
                    choose = input("Enter 1 to clear the error and let the machine continue running: ")
                    if  int(choose)==1:
                        dashboard.ClearError()
                        sleep(0.01)
                        dashboard.Continue()

      else:  
         if int(enableStatus_robot[0])==1 and int(algorithm_queue[0])==0:
            dashboard.Continue()
      globalLockValue.release()
      sleep(5)

def getPoint(dashboard: DobotApiDashboard):  #Esta curioso, porque el argumento es el objeto que tiene las funciones de movimiento, pero se usa GetPose que es del dashboard
    s = dashboard.GetPose()
    numeros_str = s[s.find("{")+1 : s.find("}")]
    lista = [int(round(float(x))) for x in numeros_str.split(",")[:4]]
    #lista = [int(x) for x in numeros_str.split(",")[:4]]
    return lista    
      
def main():
    dashboard, move, feed = ConnectRobot()
    print("Start enabling...")
    dashboard.EnableRobot()
    print("Complete enabling")
    feed_thread = threading.Thread(target=GetFeed, args=(feed,))
    feed_thread.daemon = True
    feed_thread.start()
    feed_thread1 = threading.Thread(target=ClearRobotError, args=(dashboard,))
    feed_thread1.daemon = True
    feed_thread1.start()

    dashboard.SpeedFactor(50)  #Velocidad al 100%

    #Limpieza antes de comenzar:

    for i in range(1,17):
        dashboard.DO(i,0)

    # 1. Obtener errores activos
    errors = dashboard.GetErrorID()
    if errors:
        # 2. Limpiar errores
        resp_clear = dashboard.ClearError()
        # 3. Habilitar robot
        dashboard.EnableRobot()
        sleep(2)


    p_inicial = getPoint(dashboard)
    print(getPoint(dashboard))
    #p_inicial = [55.56,286.13,-110,0]

    p_inicial[2] = -110
    p_final = [235,-255,-125,130]

    delta_xy = 63
    delta_z = 39
    delta_z2 = 1
    z_count = 0

    for i in range(2):
        for j in range(3):
            dashboard.DO(1,0)
            dashboard.DO(2,0)
            p_inicial_aux = [p_inicial[0] - delta_xy * j, p_inicial[1]+delta_xy*i, p_inicial[2]-delta_z2*j, p_inicial[3]]
            MovLinearSec(move, dashboard, p_inicial_aux, z_secure=50, verbose=True)
            WaitArrive(p_inicial_aux)
            dashboard.DO(1,1)
            dashboard.DO(2,0)
            sleep(0.5)
            p_final_aux = [p_final[0], p_final[1], p_final[2]+delta_z*z_count, p_final[3]]
            MovLinearSec(move, dashboard, p_final_aux, z_secure=125, verbose=True)
            WaitArrive(p_final_aux)
            dashboard.DO(1,0)
            dashboard.DO(2,1)
            sleep(0.5)
            z_count += 1

    dashboard.DO(1,0)
    dashboard.DO(2,0)
    RelMovLinear(move, [0, 0, 50, 0], verbose=True)
    z_count = 0
    p_final = p_final_aux

if __name__ == '__main__':
    main()
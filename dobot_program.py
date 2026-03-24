import threading
from time import sleep
from dobot_utils import *

#aqui se declaran todas las IPs de los robots a usar
IP1 = "192.168.2.5"
IP2 = "192.168.2.4"
IP3 = "192.168.2.3"
IP4 = "192.168.2.2"
IP5 = "192.168.2.1"


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

def routine1():
    dashboard, move, feed = DobotInit(IP1) #aqui se conecta al robot de la IP 192.168.2.5 (el dobot MG400 de la cinta transportadora)
    localSpeed = GlobalSpeed #se delcara la velocidad a la que se va a mover el robot
    #se declaran los puntos que se van a usar (si se puede usa el propio sistema de puntos de la aplicacion dobot para sacar los puntos rapido)
    Pi=[350,0,0,0]
    P1=[250,-242.7,-16.8,23.3]
    P2=[250.2,-242.7,138.6,23.3]
    P3=[256.28,0,138.61,25.543]
    P4=[249.99,0,-156.3,0]
    P5=[66.746,341.98,-151.5,90.732]
    P6=[66,341.98,138.61,25.543]
    P2=[250.2,-242.7,138.6,23.3]


    while True:

        limpiarEntradas(dashboard, 10) #limpia todas las salidas

        MovJoint(move, Pi) #se mueve con Joint al punto inicial (pi)
        WaitArrive(Pi) #espera a que llegue al punto inicial
        sleep(1) #espera un segundo despues de llegar

        while int(dashboard.DI(9)[3])==0: #espera hasta que el sensor del piston se encianda (esto con el propocito de que no haga nada hasta que tenga algo para poder sacar)
                                          #(numero de sensor)[indice del arreglo del que regresa el valor]
            dashboard.DO(9,0)#mantiene el output 9 apagado (piston)
            dashboard.DO(10,0)#mantiene el output 10 apagado (cinta)
        while int(dashboard.DI(10)[3])==0: #se repite mientras que este el sensor de la cinta apagado (con eso sabes maomeno a donde llega la ficha (la diferencia entre un punto y otro es milimetrico))
            dashboard.DO(9,1) #mantiene el output 9 encendido (piston)
            dashboard.DO(10,1) #mantiene el output 10 encendido (cinta)
        dashboard.DO(9,0) #apaga el output 9 (piston) apenas llega la ficha al sensor de la cinta
        dashboard.DO(10,0) #apaga el output 10 (cinta) apenas llega la ficha al sensor de la cinta
        sleep(1) #espera un segundo despues de llegar

        MovJoint(move, P2)
        WaitArrive(P2)
        sleep(1)

        MovJoint(move, P1)
        WaitArrive(P1)
        sleep(1)

        dashboard.DO(1,1) #enciende el output 1 (succion)
        sleep(1)

        MovJoint(move, P2)
        WaitArrive(P2)
        sleep(1)

        MovJoint(move, P6)
        WaitArrive(P6)
        sleep(1)

        MovJoint(move, P5)
        WaitArrive(P5)
        sleep(1)

        dashboard.DO(1,0)
        sleep(1)

        dashboard.DO(2,1)
        sleep(1)

        dashboard.DO(2,0)
        sleep(1)

        MovJoint(move, P6)
        WaitArrive(P6)
        sleep(1)

        MovJoint(move, Pi)
        WaitArrive(Pi)
        sleep(1)

        break

def routine3():
    dashboard, move, feed=DobotInit(IP4)
    localSpeed=GlobalSpeed

    Pi=[400,0,200,0]
    P1=[399.21,8.5712,154.56,93.823]
    P2=[244.86,-140.3,200,-74.94]
    P3=[244.86,-140.3,188.79,-74.94]
    P4=[9.2932,398.23,43.5,95.973]
    P5=[9.2932,398.23,102.55,95.973]

    MovJoint(move, Pi)
    WaitArrive(Pi)
    sleep(.5)

    while int(dashboard.DI(9)[3])==0: #(numero de sensor)[indice del arroglo del que regresa el valor]
        dashboard.DO(9,0)
        dashboard.DO(10,0)
    while int(dashboard.DI(10)[3])==0:
        dashboard.DO(9,1)
        dashboard.DO(10,1)
    dashboard.DO(9,0)
    dashboard.DO(10,0)
    sleep(1)

    MovJoint(move, P2)
    WaitArrive(P2)
    sleep(.5)

    MovJoint(move, P3)
    WaitArrive(P3)
    sleep(.5)

    dashboard.DO(8,1)
    sleep(2)

    MovJoint(move, P2)
    WaitArrive(P2)
    sleep(.5)

    MovJoint(move, Pi)
    WaitArrive(Pi)
    sleep(.5)

    MovJoint(move, P4)
    WaitArrive(P4)
    sleep(1.5)

    dashboard.DO(8,0)
    sleep(.5)

    dashboard.DO(7,1)
    sleep(1)

    dashboard.DO(7,0)
    sleep(0.5)

    MovJoint(move, P5)
    WaitArrive(P5)
    sleep(.5)

    MovJoint(move, Pi)
    WaitArrive(Pi)
    sleep(.5)



def routine2():
    dashboard, move, feed = DobotInit(IP2)
    localSpeed = GlobalSpeed
    #Aquí escribe la rtutina
    P1 = [-200,200,0,90.381]
    P2 = [234,-76.4,0,-3.773]
    P3 = [240,-76.4,-152.8,-3.773]
    P5 = [138.26,284.03,-162.8,77.106]
    P6 = [138.26,284.03,-38.06,77.106]

    while True:
        #print(f"{itsOn}")
        #dashboard.DO(3,itsOn)
        #sleep(0.5)

        limpiarEntradas(dashboard, 10)

        if int(dashboard.DI(1)[3])==1:

            dashboard.DO(3,1)
            sleep(0.5)

            routine1()

            MovJoint(move, P1)
            WaitArrive(P1)
            sleep(0.5)

            MovJoint(move, P2)
            WaitArrive(P2)
            sleep(0.5)

            MovJoint(move, P3)
            WaitArrive(P3)
            sleep(0.5)

            dashboard.DO(9,1)
            sleep(0.5)

            MovJoint(move, P2)
            WaitArrive(P2)
            sleep(0.5)

            MovJoint(move, P5)
            WaitArrive(P5)
            sleep(0.5)

            dashboard.DO(9,0)
            sleep(1)

            dashboard.DO(10,1)
            sleep(2)

            dashboard.DO(10,0)
            sleep(0.5)

            MovJoint(move, P6)
            WaitArrive(P6)
            sleep(0.5)

            MovJoint(move, P1)
            WaitArrive(P1)
            sleep(0.5)

            routine3()

            sleep(20)

            dashboard.DO(3,0)
            sleep(0.5)
        
if __name__ == "__main__":
    routine2()

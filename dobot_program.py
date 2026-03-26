import threading
from time import sleep
from dobot_utils import *
from DobotDemo import DobotDemo

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

def routine():
    dashboard1, move1, feed = DobotInit(IP1)
    localSpeed = GlobalSpeed
    dashboard2, move2, feed = DobotInit(IP2)
    localSpeed = GlobalSpeed
    dobot3 = DobotDemo(IP3)
    dobot3.start()
    sleep(2)
    dashboard4, move4, feed = DobotInit(IP4)
    localSpeed = GlobalSpeed
    dobot5 = DobotDemo(IP5)
    dobot5.start()
    sleep(2)
    

    Pi1=[350,0,0,0]
    P11=[250,-242.7,-16.8,23.3]
    P21=[250.2,-242.7,138.6,23.3]
    P31=[256.28,0,138.61,25.543]
    P41=[249.99,0,-156.3,0]
    P51=[66.746,341.98,-151.5,90.732]
    P61=[66,341.98,138.61,25.543]
    P21=[250.2,-242.7,138.6,23.3]

    P12 = [-200,200,0,90.381]
    P22 = [234,-76.4,0,-3.773]
    P32 = [240,-76.4,-152.8,-3.773]
    P52 = [138.26,284.03,-162.8,77.106]
    P62 = [138.26,284.03,-38.06,77.106]

    p13 = [-176.96, -208.99, 89.4272, 179.1183, -0.6229, 128.5592]
    p23 = [72.1463, -340.1630, 275.4693, -179.1450, 0.9245, -175.1831]
    p33 = [78.8526, -67.9921, 613.4407, -91.3329, -6.7666, 178.0634]
    p43 = [-176.96, -208.99, 297.6850, 179.1183, -0.6229, 128.5592]
    p53 = [73.5594, -334.0, 272.4303, -179.1450, 0.9245, -175.1831]
    p63 = [73.5594, -334.0, 250.4917, -179.1450, 0.9245, -175.1831]

    Pi4=[400,0,200,0]
    P14=[399.21,8.5712,154.56,93.823]
    P24=[244.86,-140.3,200,-74.94]
    P34=[244.86,-140.3,188.79,-74.94]
    P44=[9.2932,398.23,43.5,95.973]
    P54=[9.2932,398.23,102.55,95.973]

    p15 = [108.1967, -392.5636, 96.9418, 179.4769, 0.3314, -156.4647]
    p25 = [108.1967, -392.5636, 84.2425, 179.4769, 0.3314, -156.4647]
    p35 = [202.5460, 265.4626, 273.1837, -175.2105, 2.0367, -47.3313]
    p45 = [51.1504, 74.4889, 620.3330, -85.3803, -3.7876, -95.43]
    p55 = [205.4049, 272.1, 277.2, -177.7729, -2.1436, -47.4710]
    p65 = [108.7921, -394.2682, 96.9418, 179.4768, 0.3314, -156.4647]
    p75 = [108.7921, -394.2682, 84.8957, 179.4768, 0.3314, -156.4647]
    p85 = [205.4049, 272.1, 257.2868, -177.7729, -2.1436, -47.4710]


    limpiarEntradas(dashboard1, 10)
    limpiarEntradas(dashboard2, 10)
    limpiarEntradas(dashboard4, 10)

    MovJoint(move1, Pi1) #se mueve con Joint al punto inicial (pi)
    WaitArrive(Pi1) #espera a que llegue al punto inicial
    sleep(1) #espera un segundo despues de llegar

    MovJoint(move2, P12)
    WaitArrive(P12)
    sleep(0.5)

    try:
        dobot3.RunPoint(p33)
        sleep(.5)
    except Exception as e:
        print(f"Ocurrió un error durante la ejecución: {e}")

    try:
        dobot5.RunPoint(p45)
        sleep(.5)
    except Exception as e:
        print(f"Ocurrió un error durante la ejecución: {e}")

    MovJoint(move4, Pi4)
    sleep(.5)

    while True:
        dashboard2.DO(3,1)
        sleep(0.5)

        if int(dashboard2.DI(1)[3])==1:

            dashboard2.DO(3,0)
            sleep(0.5)

            dashboard2.DO(4,1)
            sleep(0.5)

            while int(dashboard1.DI(9)[3])==0: #espera hasta que el sensor del piston se encianda (esto con el propocito de que no haga nada hasta que tenga algo para poder sacar)
                                                #(numero de sensor)[indice del arreglo del que regresa el valor]
                dashboard1.DO(9,0)#mantiene el output 9 apagado (piston)
                dashboard1.DO(10,0)#mantiene el output 10 apagado (cinta)
            while int(dashboard1.DI(10)[3])==0: #se repite mientras que este el sensor de la cinta apagado (con eso sabes maomeno a donde llega la ficha (la diferencia entre un punto y otro es milimetrico))
                dashboard1.DO(9,1) #mantiene el output 9 encendido (piston)
                dashboard1.DO(10,1) #mantiene el output 10 encendido (cinta)
            dashboard1.DO(9,0) #apaga el output 9 (piston) apenas llega la ficha al sensor de la cinta
            dashboard1.DO(10,0) #apaga el output 10 (cinta) apenas llega la ficha al sensor de la cinta
            sleep(1) #espera un segundo despues de llegar

            MovJoint(move1, P21)
            WaitArrive(P21)
            sleep(1)

            MovJoint(move1, P11)
            WaitArrive(P11)
            sleep(1)

            dashboard1.DO(1,1) #enciende el output 1 (succion)
            sleep(1)

            MovJoint(move1, P21)
            WaitArrive(P21)
            sleep(1)

            MovJoint(move1, P61)
            WaitArrive(P61)
            sleep(1)

            MovJoint(move1, P51)
            WaitArrive(P51)
            sleep(1)

            dashboard1.DO(1,0)
            sleep(1)

            dashboard1.DO(2,1)
            sleep(1)

            dashboard1.DO(2,0)
            sleep(1)

            MovJoint(move1, P61)
            WaitArrive(P61)
            sleep(1)

            MovJoint(move1, Pi1)
            WaitArrive(Pi1)
            sleep(1)

            MovJoint(move2, P22)
            WaitArrive(P22)
            sleep(0.5)

            MovJoint(move2, P32)
            WaitArrive(P32)
            sleep(0.5)

            dashboard2.DO(9,1)
            sleep(0.5)

            MovJoint(move2, P22)
            WaitArrive(P22)
            sleep(0.5)

            MovJoint(move2, P52)
            WaitArrive(P52)
            sleep(0.5)

            dashboard2.DO(9,0)
            sleep(1)

            dashboard2.DO(10,1)
            sleep(2)

            dashboard2.DO(10,0)
            sleep(0.5)

            MovJoint(move2, P62)
            WaitArrive(P62)
            sleep(0.5)

            MovJoint(move2, P12)
            WaitArrive(P12)
            sleep(0.5)

            try:
                dobot3.RunPoint(p33)
                sleep(.5)

                dobot3.RunPoint(p43)
                sleep(.5)

                dobot3.RunPoint(p13)
                sleep(.5)
                
            
                print("Encendiendo herramienta...")
                dobot3.dashboard.ToolDOInstant(1, 1)
                sleep(1) # Espera opcional para asegurar la acción física

                dobot3.RunPoint(p43)
                sleep(.5)

                dobot3.RunPoint(p53)
                sleep(.5)

                dobot3.RunPoint(p63)
                sleep(.5)

                print("Encendiendo herramienta...")
                dobot3.dashboard.ToolDOInstant(1, 0)
                sleep(1) # Espera opcional para asegurar la acción física

                dobot3.RunPoint(p53)
                sleep(.5)

                dobot3.RunPoint(p33)
                sleep(.5)

            except Exception as e:
                print(f"Ocurrió un error durante la ejecución: {e}")

            while int(dashboard4.DI(9)[3])==0: #(numero de sensor)[indice del arroglo del que regresa el valor]
                dashboard4.DO(9,0)
                dashboard4.DO(10,0)
            while int(dashboard4.DI(10)[3])==0:
                dashboard4.DO(9,1)
                dashboard4.DO(10,1)
            dashboard4.DO(9,0)
            dashboard4.DO(10,0)
            sleep(1)

            MovJoint(move4, P24)
            WaitArrive(P24)
            sleep(.5)

            MovJoint(move4, P34)
            WaitArrive(P34)
            sleep(.5)

            dashboard4.DO(8,1)
            sleep(2)

            MovJoint(move4, P24)
            WaitArrive(P24)
            sleep(.5)

            MovJoint(move4, Pi4)
            WaitArrive(Pi4)
            sleep(.5)

            MovJoint(move4, P44)
            WaitArrive(P44)
            sleep(1.5)

            dashboard4.DO(8,0)
            sleep(.5)

            dashboard4.DO(7,1)
            sleep(1)

            dashboard4.DO(7,0)
            sleep(0.5)

            MovJoint(move4, P54)
            WaitArrive(P54)
            sleep(.5)

            MovJoint(move4, Pi4)
            WaitArrive(Pi4)
            sleep(.5)

            try:
                dobot5.RunPoint(p65)
                sleep(.5)

                dobot5.RunPoint(p75)
                sleep(.5)

                print("Encendiendo herramienta...")
                dobot5.dashboard.ToolDOInstant(1, 1)
                sleep(1)

                dobot5.RunPoint(p65)
                sleep(.5)

                dobot5.RunPoint(p45)
                sleep(.5)

                dobot5.RunPoint(p55)
                sleep(.5)

                dobot5.RunPoint(p85)
                sleep(.5)

                print("Encendiendo herramienta...")
                dobot5.dashboard.ToolDOInstant(1, 0)
                sleep(1)

                dobot5.RunPoint(p55)
                sleep(.5)

                dobot5.RunPoint(p45)
                sleep(.5)

            except Exception as e:
                print(f"Ocurrió un error durante la ejecución: {e}")

            dashboard2.DO(4,0)
            sleep(0.5)
        
if __name__ == "__main__":
    routine()
import threading
from time import sleep
import numpy as np
from dobot_api import MyType, DobotApiDashboard, DobotApiMove, DobotApi
from dobot_utils import ConnectRobot, MovLinear

class Dobot_Robot:
    def __init__(self, ip: str, speed: int = 50):
        self.ip = ip
        self.speed = speed
        self.dashboard = None
        self.move = None
        self.feed = None
        self.current_pose = None  # Coordenadas privadas de este robot
        self.connected = False
        self.lock = threading.Lock()

    def _feedback_loop(self):
        """Hilo privado para actualizar la posición de ESTE robot."""
        hasRead = 0
        while self.connected:
            try:
                data = bytes()
                while hasRead < 1440:
                    temp = self.feed.socket_dobot.recv(1440 - hasRead)
                    if len(temp) > 0:
                        hasRead += len(temp)
                        data += temp
                hasRead = 0
                feedInfo = np.frombuffer(data, dtype=MyType)
                if hex((feedInfo['test_value'][0])) == '0x123456789abcdef':
                    with self.lock:
                        # Guardamos solo la pose de este robot
                        self.current_pose = feedInfo["tool_vector_actual"][0]
                sleep(0.005)
            except:
                break

    def connect(self):
        try:
            self.dashboard, self.move, self.feed = ConnectRobot(self.ip)
            self.dashboard.ClearError()
            sleep(0.5)
            self.dashboard.Continue()
            self.dashboard.EnableRobot()
            self.dashboard.SpeedFactor(self.speed)
            self.connected = True
            
            # Iniciamos el feedback propio
            threading.Thread(target=self._feedback_loop, daemon=True).start()
            print(f"[{self.ip}] Conectado correctamente.")
        except Exception as e:
            print(f"[{self.ip}] Error de conexión: {e}")

    def wait_arrive(self, target, threshold=1):
        """Espera a que este robot específico llegue a su destino."""
        while True:
            with self.lock:
                if self.current_pose is not None:
                    # Comparamos X, Y, Z, R
                    dist = np.linalg.norm(self.current_pose[:4] - np.array(target))
                    if dist < threshold:
                        return
            sleep(0.01)

    def move_async(self, point):
        """Dispara el movimiento en un hilo independiente."""
        def task():
            print(f"[{self.ip}] Iniciando movimiento a {point}")
            MovLinear(self.move, point)
            self.wait_arrive(point)
            print(f"[{self.ip}] Movimiento completado.")

        t = threading.Thread(target=task)
        t.start()
        return t
    
    def wait_robot_sync(self):
        # Este comando le dice al controlador: "Dime cuando hayas terminado todo"
        return self.move.Sync()
    
    def wait_until_idle(self):
        """Bloquea el código hasta que el robot físico termine su trayectoria."""
        print(f"[{self.ip}] Esperando finalización de movimiento...")
        self.move.Sync()
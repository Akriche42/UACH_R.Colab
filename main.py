from DobotDemo import DobotDemo
import time

if __name__ == '__main__':
    # 1. Conectar al robot
    dobot = DobotDemo("192.168.2.3")
    dobot.start()
    
    # Esperar un poco a que el hilo de feedback se estabilice
    time.sleep(2)

    # 2. Definir los puntos (X, Y, Z, RX, RY, RZ)
    point_a = [88, -265, 286, 178, 1, 178]
    point_b = [83, -89, 610, -92, 8, -178]

    try:
        # --- MOVIMIENTO AL PUNTO A ---
        print("Moviendo a Punto A...")
        dobot.RunPoint(point_a)
        time.sleep(2)
        
        # --- ENCENDER HERRAMIENTA (DO Tool) ---
        # ToolDOInstant(index, status): index suele ser 1 para la herramienta, status 1 es ON
        print("Encendiendo herramienta...")
        dobot.dashboard.ToolDOInstant(1, 1)
        time.sleep(1) # Espera opcional para asegurar la acción física

        # --- MOVIMIENTO AL PUNTO B ---
        print("Moviendo a Punto B...")
        dobot.RunPoint(point_b)

        # --- APAGAR HERRAMIENTA ---
        print("Apagando herramienta...")
        dobot.dashboard.ToolDOInstant(1, 0)

    except Exception as e:
        print(f"Ocurrió un error durante la ejecución: {e}")
from dobot_robot import Dobot_Robot
from time import sleep
import threading

def mover_robots_sincronizados(lista_robots, lista_puntos, pausa_final=1.0):
    hilos = []

    # 1. Disparar el comando de movimiento a todos los robots al mismo tiempo
    for i, bot in enumerate(lista_robots):
        if bot.connected:
            # Usamos un hilo para enviar el comando MovL y luego el Sync
            def tarea_robot(b, p):
                b.move.MovL(p[0], p[1], p[2], p[3]) # Envía el movimiento
                b.wait_until_idle()                 # Bloquea ESTE hilo hasta que llegue
            
            t = threading.Thread(target=tarea_robot, args=(bot, lista_puntos[i]))
            t.start()
            hilos.append(t)

    # 2. BARRERA: El script principal se detiene aquí hasta que TODOS los hilos terminen
    for t in hilos:
        t.join() 

    print("Sincronización completa: Ambos robots se detuvieron.")
    
    # 3. PAUSA OPCIONAL: Si necesitas un respiro entre tareas
    if pausa_final > 0:
        print(f"Pausa de seguridad de {pausa_final}s...")
        sleep(pausa_final)

# --- Ejemplo de Ejecución ---
if __name__ == '__main__':
    bot1 = Dobot_Robot("192.168.2.4")
    bot2 = Dobot_Robot("192.168.2.5") # Supongamos un segundo robot
    
    bot1.connect()
    bot2.connect()

    # Definir destinos diferentes para cada uno
    punto_a = [275, 100, 10, 0]
    punto_b = [300, 0, 50, 0]

    # Ejecutar movimiento simultáneo
    while True:
        mover_robots_sincronizados([bot1, bot2], [punto_a, punto_b])
        mover_robots_sincronizados([bot1, bot2], [punto_b, punto_a])

import time
import sys
from coach import CoachAI

# Intentamos importar msvcrt (nativo de Windows para detectar teclas al instante)
try:
    import msvcrt
except ImportError:
    msvcrt = None

def correr_cronometro(minutos):
    """Ejecuta un cronómetro interactivo con Pausa, Reanudar y Finalizar."""
    # Convertimos los minutos a segundos para la simulación (1 min de rutina = 1 seg de reloj)
    segundos_totales = minutos 
    pausado = False
    
    print("\n" + "="*40)
    print("      ⏱️ ¡COMIENZA EL CRONÓMETRO!      ")
    print("="*40)
    print("Controles en tiempo real:")
    print(" ➔ Presioná [ P ] para Pausar")
    print(" ➔ Presioná [ R ] para Reanudar")
    print(" ➔ Presioná [ F ] para Finalizar antes")
    print("-" * 40 + "\n")
    
    while segundos_totales > 0:
        # Si no está pausado, el tiempo corre
        if not pausado:
            mins, secs = divmod(segundos_totales, 60)
            # Dibujamos el reloj en la misma línea de la consola usando \r
            sys.stdout.write(f"\r⏳ TIEMPO RESTANTE: {mins:02d}:{secs:02d} | [P] Pausar ")
            sys.stdout.flush()
            time.sleep(1)
            segundos_totales -= 1
        else:
            sys.stdout.write(f"\r⏸️ CRONÓMETRO PAUSADO | [R] Reanudar | [F] Terminar ")
            sys.stdout.flush()
            time.sleep(0.5)

        # Detectamos si el usuario presionó una tecla en Windows
        if msvcrt and msvcrt.kbhit():
            tecla = msvcrt.getch().decode('utf-8').lower()
            if tecla == 'p' and not pausado:
                pausado = True
            elif tecla == 'r' and pausado:
                pausado = False
            elif tecla == 'f':
                print("\n\n👋 Entrenamiento finalizado antes de tiempo por el usuario.")
                # Calculamos cuántos minutos reales hizo hasta la pausa
                minutos_hechos = minutos - segundos_totales
                return minutos_hechos if minutos_hechos > 0 else 1

    print("\n\n🎉 ¡TIEMPO COMPLETADO! Excelente entrenamiento. 🏃‍♂️💨")
    return minutos

# --- FLUJO PRINCIPAL ---

print("=== BIENVENIDO A COACH-AI LOCAL (CRONÓMETRO INTERACTIVO) ===")
nombre = input("¿Cómo te llamás?: ")
deporte = input("¿Qué deporte practicás?: ")

usuario = CoachAI(nombre, deporte)
print(f"\n¡Perfil creado! Hola {usuario.username}. Nivel: {usuario.level} | Puntos: {usuario.streak_points}\n")

while True:
    print("-" * 55)
    print("1. Pedir rutina a la IA e iniciar entrenamiento con reloj")
    print("2. Registrar un entrenamiento manual (Sin cronómetro)")
    print("3. Salir")
    opcion = input("Elegí una opción (1/2/3): ").strip()
    
    if opcion == "1":
        estado = input("\n¿Cómo te sentís hoy o qué limitaciones tenés?\n(Ej: 'Me duele la rodilla izquierda y tengo solo 20 minutos'):\n> ")
        
        # Extraemos el tiempo que pidió el usuario (por defecto 30 minutos)
        minutos_estimados = 30
        for palabra in estado.split():
            if palabra.isdigit():
                minutos_estimados = int(palabra)
                break

        print("\n🤖 El Coach de IA está diseñando tu rutina ideal...")
        rutina = usuario.generar_rutina_ia(estado)
        
        print("\n" + "="*45)
        print(rutina)
        print("="*45 + "\n")
        
        input("Presioná [ENTER] cuando estés listo para empezar el cronómetro... ")
        
        # Ejecutamos el reloj interactivo
        minutos_entrenados = correr_cronometro(minutos_estimados)
        
        # Una vez terminado el tiempo, se añaden los puntos automáticamente
        print("\n🏋️ Guardando entrenamiento en tu historial...")
        time.sleep(1)
        
        puntos_ganados = usuario.registrar_entrenamiento(minutos_entrenados)
        
        print(f"\n🎉 ¡Se registraron automáticamente {puntos_ganados} puntos de constancia!")
        print(f"📈 Tu nuevo estado: Nivel {usuario.level} | Total: {usuario.streak_points} puntos.")
            
    elif opcion == "2":
        try:
            minutos = int(input("¿Cuántos minutos entrenaste por tu cuenta?: "))
            puntos_ganados = usuario.registrar_entrenamiento(minutos)
            print(f"¡Excelente! Sumaste {puntos_ganados} puntos. Nivel actual: {usuario.level} ({usuario.streak_points} pts)")
        except ValueError as e:
            print(f"❌ Error: {e}")
            
    elif opcion == "3":
        print("\n¡Gracias por entrenar con CoachAI! ¡Seguí así!")
        break
    else:
        print("Opción inválida.")
import RPi.GPIO as GPIO
import time

# Configuración del modo de numeración de pines (BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definición de Pines según tu esquema
TRIG = 17
ECHO = 27
LED_D1 = 23
LED_D2 = 24
LED_D3 = 25

# Configurar pines de entrada y salida
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_D1, GPIO.OUT)
GPIO.setup(LED_D2, GPIO.OUT)
GPIO.setup(LED_D3, GPIO.OUT)

def calcular_distancia():
    # Asegurar que el Trigger empiece apagado
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    
    # Enviar un pulso de 10 microsegundos por el Trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    # Registrar el inicio y fin del pulso recibido en Echo
    inicio_pulso = time.time()
    fin_pulso = time.time()
    
    while GPIO.input(ECHO) == 0:
        inicio_pulso = time.time()
        
    while GPIO.input(ECHO) == 1:
        fin_pulso = time.time()
        
    # Calcular la duración del viaje de la onda
    duracion = fin_pulso - inicio_pulso
    
    # Multiplicar por la velocidad del sonido (34300 cm/s) y dividir entre 2
    distancia = (duracion * 34300) / 2
    return distancia

try:
    while True:
        dist = calcular_distancia()
        print(f"Distancia simulada: {dist:.2f} cm")
        
        # LÓGICA DE CONTROL DE LOS LEDS (Ejemplo basado en distancia):
        if dist < 10:
            # Muy cerca: Enciende D1 (Alerta máxima)
            GPIO.output(LED_D1, True)
            GPIO.output(LED_D2, False)
            GPIO.output(LED_D3, False)
        elif 10 <= dist < 30:
            # Distancia media: Enciende D2
            GPIO.output(LED_D1, False)
            GPIO.output(LED_D2, True)
            GPIO.output(LED_D3, False)
        else:
            # Distancia segura: Enciende D3
            GPIO.output(LED_D1, False)
            GPIO.output(LED_D2, False)
            GPIO.output(LED_D3, True)
            
        time.sleep(0.5) # Esperar medio segundo antes de la próxima lectura

except KeyboardInterrupt:
    GPIO.cleanup() # Limpiar pines al detener la simulación
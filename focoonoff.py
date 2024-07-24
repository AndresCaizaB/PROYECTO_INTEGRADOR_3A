import RPi.GPIO as GPIO
import time

# Configuración de los pines GPIO para el DIP switch
dip_pins = [17, 27, 22, 24]

# Configuración de los pines GPIO para el módulo relé
relay_pins = [5, 6, 13, 19]

# Configuración de la Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Configuración de los pines del DIP switch como entradas con resistencias pull-down
for pin in dip_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configuración de los pines del módulo relé como salidas
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Inicialmente, los relés están apagados

def read_dip_switch():
    """Lee el estado del DIP switch."""
    return [GPIO.input(pin) for pin in dip_pins]

def control_relays(dip_states):
    """Controla los relés según el estado del DIP switch."""
    for i, state in enumerate(dip_states):
        GPIO.output(relay_pins[i], GPIO.HIGH if state else GPIO.LOW)

try:
    while True:
        dip_states = read_dip_switch()
        control_relays(dip_states)
        time.sleep(0.1)  # Pequeño retraso para evitar un uso excesivo de la CPU

except KeyboardInterrupt:
    print("Programa terminado.")

finally:
    GPIO.cleanup()  # Limpieza de los pines GPIO

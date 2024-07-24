import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import subprocess
import os

# Configuración del sensor PIR
PIR_PIN = 23  # GPIO pin 16 en la Raspberry Pi

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def capturar_imagen(ruta_imagen):
    try:
        # Captura la imagen usando libcamera-still
        subprocess.run(['libcamera-still', '-o', ruta_imagen], check=True)
        print(f'Imagen capturada exitosamente: {ruta_imagen}')
    except subprocess.CalledProcessError:
        print('Error al capturar la imagen')
        return False
    return True

def enviar_correo(destinatario, asunto, mensaje, ruta_foto):
    remitente = 'andrescaizab@gmail.com'
    contrasena = 'pyvbohwfkzcqfnio'  # Asegúrate de que esta es la contraseña de aplicación sin espacios

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    # Adjuntar la foto
    try:
        with open(ruta_foto, 'rb') as archivo_foto:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(archivo_foto.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f'attachment; filename={os.path.basename(ruta_foto)}')
            msg.attach(parte)
    except FileNotFoundError:
        print(f'Error: El archivo {ruta_foto} no se encuentra.')
        return
    except Exception as e:
        print(f'Error: {e}')
        return

    try:
        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(remitente, contrasena)
            server.sendmail(remitente, destinatario, msg.as_string())
        print('Correo enviado exitosamente')
    except Exception as e:
        print(f'Error al enviar correo: {e}')

def main():
    print("Esperando detección de movimiento...")
    
    try:
        while True:
            if GPIO.input(PIR_PIN):
                print("Movimiento detectado!")
                ruta_imagen = 'imagen.jpg'
                if capturar_imagen(ruta_imagen):
                    enviar_correo('andyjhonson.caiza28@gmail.com', 'Alerta de Movimiento', 'El sensor PIR a detectado movimiento', ruta_imagen)
                # Esperar 60 segundos para evitar múltiples capturas en un corto período
                time.sleep(60)
            else:
                print("No hay movimiento detectado")
            time.sleep(1)  # Esperar 1 segundo antes de la próxima lectura
    except KeyboardInterrupt:
        print("Programa terminado")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()


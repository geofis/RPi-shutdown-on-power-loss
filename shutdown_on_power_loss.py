#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import threading
import subprocess
import sys
import os

# Configuración de ruta y valores por defecto
CONF_PATH = "/etc/shutdown_on_power_loss.conf"
DEFAULT_WAIT_SECONDS = 600
DEFAULT_GPIO_PIN = 26

apagado_pendiente = threading.Event()
apagado_en_proceso = threading.Event()

def leer_configuracion():
    tiempo_espera = DEFAULT_WAIT_SECONDS
    gpio_pin = DEFAULT_GPIO_PIN

    try:
        with open(CONF_PATH, "r") as f:
            for linea in f:
                if linea.startswith("USER_TIMEOUT="):
                    tiempo_espera = int(linea.strip().split("=")[1])
                elif linea.startswith("GPIO_PIN="):
                    gpio_pin = int(linea.strip().split("=")[1])
    except Exception as e:
        print(f"⚠️ No se pudo leer {CONF_PATH}: {e}")

    return tiempo_espera, gpio_pin

# Leer configuración
TIEMPO_ESPERA, PIN_PG = leer_configuracion()

def iniciar_temporizador_apagado():
    print(f"⚠️ Energía externa desconectada. Esperando {TIEMPO_ESPERA} segundos antes de apagar...")
    apagado_pendiente.set()
    tiempo_inicial = time.time()

    while time.time() - tiempo_inicial < TIEMPO_ESPERA:
        if GPIO.input(PIN_PG) == GPIO.LOW:
            print("✅ Energía externa restaurada. Cancelando apagado.")
            apagado_pendiente.clear()
            return
        time.sleep(5)

    if apagado_pendiente.is_set():
        print("🔻 Energía externa no regresó. Apagando Raspberry Pi.")
        apagado_en_proceso.set()
        subprocess.run(["sync"])
        time.sleep(2)
        subprocess.run(["systemctl", "poweroff"])

def manejar_evento(channel):
    if not apagado_en_proceso.is_set() and not apagado_pendiente.is_set():
        hilo = threading.Thread(target=iniciar_temporizador_apagado)
        hilo.start()

# Configurar pin con pull-up
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PG, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(PIN_PG, GPIO.RISING, callback=manejar_evento, bouncetime=1000)

# Evaluar estado inicial por si ya está en HIGH al arrancar (sin energía externa)
estado_inicial = GPIO.input(PIN_PG)
print(f"📈 Estado inicial de GPIO{PIN_PG}: {'HIGH (sin energía externa)' if estado_inicial == GPIO.HIGH else 'LOW (energía externa presente)'}")
if estado_inicial == GPIO.HIGH:
    print("⚠️ Energía externa ya está desconectada al iniciar. Iniciando temporizador.")
    manejar_evento(PIN_PG)

# Imprimir mensaje de monitoreo
print(f"🔌 Monitoreando PG (GPIO{PIN_PG})... Tiempo de espera: {TIEMPO_ESPERA} s")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("⛔ Cancelado por el usuario.")
finally:
    GPIO.cleanup()

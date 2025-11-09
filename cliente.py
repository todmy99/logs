import requests
import datetime
import random
import time

# Lista de servicios y sus tokens
SERVICES = {
    "servicio1": "TOKEN1",
    "servicio2": "TOKEN2",
    "servicio3": "TOKEN3"  # agregamos uno más para probar
}

# Lista de posibles niveles de severidad
SEVERITIES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Lista de mensajes de ejemplo
MESSAGES = [
    "Todo está funcionando",
    "Ocurrió un pequeño error",
    "Se perdió la conexión temporalmente",
    "Proceso completado correctamente",
    "Fallo crítico, atención!"
]

# Función para generar un log aleatorio
def generate_log(service_name):
    return {
        "timestamp": str(datetime.datetime.now()),
        "service": service_name,
        "severity": random.choice(SEVERITIES),
        "message": random.choice(MESSAGES)
    }

# URL del servidor
SERVER_URL = "http://127.0.0.1:5000/logs"

# Enviar 3 logs por servicio
for service_name, token in SERVICES.items():
    for i in range(3):  # <- cambiar 3 por la cantidad que quieras
        log = generate_log(service_name)
        headers = {"Authorization": f"Token {token}"}
        try:
            response = requests.post(SERVER_URL, json=log, headers=headers, timeout=5)
            print(f"[{service_name} #{i+1}] {response.json()}")
        except Exception as e:
            print(f"[{service_name} #{i+1}] Error enviando log: {e}")
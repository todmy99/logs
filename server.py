from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__) #indico que es mi app principal

# Diccionario de tokens válidos
VALID_TOKENS = {"servicio1": "TOKEN1", "servicio2": "TOKEN2"}

# Crear la tabla logs si no existe
def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        service TEXT,
        severity TEXT,
        message TEXT,
        received_at TEXT
    )
    """)
    conn.commit()
    conn.close()


init_db() #inicializamos la base de datos

# POST /logs: recibir y guardar logs
@app.route("/logs", methods=["POST"])
def receive_logs():
    token_header = request.headers.get("Authorization", "") #header contiene informacion
    token = token_header.replace("Token ", "") #eliminamos la palabra Token
    
    if token not in VALID_TOKENS.values():
        return jsonify({"error": "Quién sos, bro?"}), 401

    data = request.json

    # Guardar log en SQLite
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (timestamp, service, severity, message, received_at) VALUES (?, ?, ?, ?, ?)",
        (data["timestamp"], data["service"], data["severity"], data["message"], str(datetime.datetime.now()))
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "log recibido"})

# GET /logs: consultar logs con filtros opcionales
@app.route("/logs", methods=["GET"])
def get_logs():
    ts_start = request.args.get("timestamp_start")
    ts_end = request.args.get("timestamp_end")
    received_start = request.args.get("received_at_start")
    received_end = request.args.get("received_at_end")

    query = "SELECT * FROM logs WHERE 1=1" #permite concatenar "AND ..." sin errores de sintaxis
    params = [] #se insertan valores para reemplanzar ????

    if ts_start: #podemos filtrar por hora de envio u hora de recibo
        query += " AND timestamp >= ?"
        params.append(ts_start)
    if ts_end:
        query += " AND timestamp <= ?"
        params.append(ts_end)
    if received_start:
        query += " AND received_at >= ?"
        params.append(received_start)
    if received_end:
        query += " AND received_at <= ?"
        params.append(received_end)

    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    logs_list = []
    for row in rows: #recorremos cada log o fila
        log = {
            "id": row[0],
            "timestamp": row[1],
            "service": row[2],
            "severity": row[3],
            "message": row[4],
            "received_at": row[5]
        }
        logs_list.append(log)

    return jsonify(logs_list) #formato JSON para que el cliente entienda

if __name__ == "__main__": #solo si este archivo se está ejecutando directamente
    app.run(debug=True) #muestra errores si los hay, recarga el server si hay cambios
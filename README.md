Servicio de Logging Distribuido

Sistema simple de recolección y consulta de logs entre múltiples servicios usando Flask y SQLite.

🚀 Descripción

Varios servicios simulados generan logs y los envían en formato JSON al servidor central.
El servidor valida un token de autenticación, guarda los logs en la base de datos y permite consultarlos filtrando por fechas.

⚙️ Endpoints

POST /logs → recibe uno o varios logs.

Header: Authorization: Token TU_TOKEN

Body JSON:
```
{
  "timestamp": "2025-11-06T14:30:00",
  "service": "auth_service",
  "severity": "ERROR",
  "message": "Usuario no autenticado"
}
```

GET /logs → devuelve logs almacenados, con filtros opcionales:
```
/logs?timestamp_start=2025-11-01T00:00:00&timestamp_end=2025-11-05T23:59:59
```
🧩 Tecnologías

-Python + Flask
-SQLite (base de datos local)

🧪 Pruebas rápidas

Podés probarlo con:
```
curl -X GET "http://127.0.0.1:5000/logs"
```

o usando Postman con los headers y parámetros adecuados.

# API de Incidentes

Una API RESTful desarrollada con Flask y PostgreSQL para la gestión de incidentes.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Contribución](#contribución)

## Requisitos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona el repositorio o descarga el código fuente:

```bash
git clone https://github.com/tu-usuario/api-incidentes.git
cd api-incidentes
```

2. Crea un entorno virtual y actívalo:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

Si no tienes un archivo requirements.txt, puedes instalarlo con:

```bash
pip install flask flask-sqlalchemy psycopg2-binary
```

## Configuración

1. Crea una base de datos PostgreSQL:

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear la base de datos (dentro de psql)
CREATE DATABASE "Primera API";
```

2. Actualiza la configuración de la base de datos en `app.py` según tus credenciales:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:contraseña@localhost:5432/Primera API'
```

Reemplaza `usuario` y `contraseña` con tus credenciales de PostgreSQL.

## Ejecución

1. Ejecuta la aplicación:

```bash
python app.py
```

2. La API estará disponible en `http://localhost:4000`

## Estructura del Proyecto

```
api-incidentes/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

## API Endpoints

### Obtener todos los incidentes

- **URL**: `/incidentes`
- **Método**: `GET`
- **Respuesta exitosa**:
  - **Código**: 200
  - **Contenido**: Array de objetos incidente
  ```json
  [
    {
      "id": 1,
      "name": "Incidente 1",
      "reporte": "Descripción del incidente",
      "status": "Abierto",
      "fecha": "2024-04-03"
    }
  ]
  ```

### Crear un nuevo incidente

- **URL**: `/incidentes`
- **Método**: `POST`
- **Datos**: 
  ```json
  {
    "name": "Incidente 2",
    "reporte": "Otro reporte",
    "status": "En progreso",
    "fecha": "2024-04-04"
  }
  ```
- **Respuesta exitosa**:
  - **Código**: 201
  - **Contenido**: `{ "message": "Incidente creado" }`

### Actualizar un incidente por ID

- **URL**: `/incidentes/{id}`
- **Método**: `PUT`
- **Datos**: 
  ```json
  {
    "name": "Nuevo nombre",
    "reporte": "Nuevo reporte",
    "status": "Cerrado",
    "fecha": "2024-04-05"
  }
  ```
- **Respuesta exitosa**:
  - **Código**: 200
  - **Contenido**: `{ "message": "Incidente actualizado" }`
- **Respuesta de error**:
  - **Código**: 404
  - **Contenido**: `{ "error": "Incidente no encontrado" }`

### Eliminar un incidente por ID

- **URL**: `/incidentes/{id}`
- **Método**: `DELETE`
- **Respuesta exitosa**:
  - **Código**: 200
  - **Contenido**: `{ "message": "Incidente eliminado" }`
- **Respuesta de error**:
  - **Código**: 404
  - **Contenido**: `{ "error": "Incidente no encontrado" }`

## Ejemplos de Uso

### Usando curl

#### Obtener todos los incidentes:
```bash
curl http://localhost:4000/incidentes
```

#### Crear un nuevo incidente:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Error 500","reporte":"Servidor caído","status":"Abierto","fecha":"2024-04-03"}' http://localhost:4000/incidentes
```

#### Actualizar un incidente:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Error 500","reporte":"Servidor reiniciado","status":"Cerrado","fecha":"2024-04-03"}' http://localhost:4000/incidentes/1
```

#### Eliminar un incidente:
```bash
curl -X DELETE http://localhost:4000/incidentes/1
```

### Usando Python Requests

```python
import requests
import json

# URL base
BASE_URL = "http://localhost:4000"

# Obtener todos los incidentes
response = requests.get(f"{BASE_URL}/incidentes")
print(response.json())

# Crear un nuevo incidente
data = {
    "name": "Fallo Sistema",
    "reporte": "Sistema no responde",
    "status": "Abierto",
    "fecha": "2024-04-03"
}
response = requests.post(f"{BASE_URL}/incidentes", json=data)
print(response.json())

# Actualizar incidente
data = {
    "status": "Cerrado",
    "reporte": "Sistema reparado"
}
response = requests.put(f"{BASE_URL}/incidentes/1", json=data)
print(response.json())

# Eliminar incidente
response = requests.delete(f"{BASE_URL}/incidentes/1")
print(response.json())
```

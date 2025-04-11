from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS


# Estados válidos permitidos (ajustados según la documentación)
ESTADOS_PERMITIDOS = {"Abierto", "En progreso", "Cerrado"}

app = Flask(__name__)
CORS(app) 

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1999@localhost:5432/Primera API'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla "incidentes"
class Incidente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reporte = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

# Crear la base de datos (ejecutar solo una vez)
with app.app_context():
    db.create_all()

# Función para validar formato de fecha
def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Ruta GET para obtener todos los incidentes
@app.route('/incidentes', methods=['GET'])
def get_incidentes():
    # Obtener parámetros de consulta opcionales
    status = request.args.get('status')
    fecha_desde = request.args.get('fecha_desde')
    
    # Crear consulta base
    query = Incidente.query
    
    # Aplicar filtros si existen
    if status:
        query = query.filter(Incidente.status == status)
    if fecha_desde and validar_fecha(fecha_desde):
        query = query.filter(Incidente.fecha >= fecha_desde)
    
    incidentes = query.all()
    return jsonify([{
        "id": inc.id,
        "name": inc.name,
        "reporte": inc.reporte,
        "status": inc.status,
        "fecha": inc.fecha
    } for inc in incidentes])

# Ruta GET por ID
@app.route('/incidentes/<int:id>', methods=['GET'])
def get_incidente_by_id(id):
    incidente = Incidente.query.get(id)
    if not incidente:
        return jsonify({'error': f'No se encontró el incidente con ID {id}'}), 404
    return jsonify({
        "id": incidente.id,
        "name": incidente.name,
        "reporte": incidente.reporte,
        "status": incidente.status,
        "fecha": incidente.fecha
    }), 200

# Ruta POST
@app.route('/incidentes', methods=['POST'])
def create_incidente():
    datos = request.get_json()
    
    # Verificar campos requeridos
    if 'name' not in datos or 'reporte' not in datos:
        return jsonify({"error": "Se requieren los campos 'name' y 'reporte'"}), 400
    
    # Validar y establecer valores predeterminados
    status = datos.get('status', 'Abierto')
    if status not in ESTADOS_PERMITIDOS:
        return jsonify({"error": f"Estado no válido. Debe ser {', '.join(ESTADOS_PERMITIDOS)}"}), 400
    
    # Validar formato de fecha
    fecha = datos.get('fecha', datetime.now().strftime('%Y-%m-%d'))
    if not validar_fecha(fecha):
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    nuevo_incidente = Incidente(
        name=datos['name'],
        reporte=datos['reporte'],
        status=status,
        fecha=fecha
    )
    db.session.add(nuevo_incidente)
    db.session.commit()
    
    # Devolver mensaje e ID como en la documentación
    return jsonify({
        "message": "Incidente creado",
        "id": nuevo_incidente.id
    }), 201

# Ruta PUT
@app.route('/incidentes/<int:id>', methods=['PUT'])
def update_incidente(id):
    incidente = Incidente.query.get(id)
    if not incidente:
        return jsonify({'error': f'No se encontró el incidente con ID {id}'}), 404

    datos = request.get_json()

    if 'status' in datos:
        if datos['status'] not in ESTADOS_PERMITIDOS:
            return jsonify({"error": f"Estado no válido. Debe ser {', '.join(ESTADOS_PERMITIDOS)}"}), 400
        incidente.status = datos['status']

    if 'name' in datos:
        incidente.name = datos['name']
    if 'reporte' in datos:
        incidente.reporte = datos['reporte']
    if 'fecha' in datos:
        if not validar_fecha(datos['fecha']):
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
        incidente.fecha = datos['fecha']

    db.session.commit()
    return jsonify({
        "message": "Incidente actualizado",
        "id": incidente.id
    }), 200

# Ruta DELETE
@app.route('/incidentes/<int:id>', methods=['DELETE'])
def delete_incidente(id):
    incidente = Incidente.query.get(id)
    if not incidente:
        return jsonify({'error': f'No se encontró el incidente con ID {id}'}), 404

    db.session.delete(incidente)
    db.session.commit()
    return jsonify({"message": "Incidente eliminado"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=4000)
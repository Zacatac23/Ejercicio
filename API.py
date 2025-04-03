from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1999@localhost:5432/Primera API'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definimos el modelo de la tabla "incidentes"
class Incidente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reporte = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

# Crear la base de datos (Ejecutar una sola vez)
with app.app_context():
    db.create_all()

# Ruta GET para obtener todos los incidentes
@app.route('/incidentes', methods=['GET'])
def get_incidentes():
    incidentes = Incidente.query.all()
    return jsonify([{
        "id": inc.id,
        "name": inc.name,
        "reporte": inc.reporte,
        "status": inc.status,
        "fecha": inc.fecha
    } for inc in incidentes])

# Ruta POST para crear un nuevo incidente
@app.route('/incidentes', methods=['POST'])
def create_incidente():
    datos = request.get_json()
    nuevo_incidente = Incidente(
        name=datos['name'],
        reporte=datos['reporte'],
        status=datos['status'],
        fecha=datos['fecha']
    )
    db.session.add(nuevo_incidente)
    db.session.commit()
    return jsonify({"message": "Incidente creado"}), 201

# Ruta PUT para actualizar un incidente por ID
@app.route('/incidentes/<int:id>', methods=['PUT'])
def update_incidente(id):
    incidente = Incidente.query.get(id)
    if not incidente:
        return jsonify({'error': 'Incidente no encontrado'}), 404

    datos = request.get_json()
    incidente.name = datos.get('name', incidente.name)
    incidente.reporte = datos.get('reporte', incidente.reporte)
    incidente.status = datos.get('status', incidente.status)
    incidente.fecha = datos.get('fecha', incidente.fecha)

    db.session.commit()
    return jsonify({"message": "Incidente actualizado"}), 200

# Ruta DELETE para eliminar un incidente por ID
@app.route('/incidentes/<int:id>', methods=['DELETE'])
def delete_incidente(id):
    incidente = Incidente.query.get(id)
    if not incidente:
        return jsonify({'error': 'Incidente no encontrado'}), 404

    db.session.delete(incidente)
    db.session.commit()
    return jsonify({"message": "Incidente eliminado"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=4000)

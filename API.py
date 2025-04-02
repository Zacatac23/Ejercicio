from flask import Flask, request, jsonify
from Incidentes import incidentes  # Asegúrate de que este módulo define 'incidentes' como una lista

app = Flask(__name__)

# Ruta GET para obtener todos los incidentes
@app.route('/incidentes', methods=['GET'])
def get_incidentes():
    return jsonify(incidentes)

# Ruta POST para crear un nuevo incidente
@app.route('/incidentes', methods=['POST'])
def create_incidente():
    nuevo_incidente = request.get_json()
    
    # Validamos si los datos son correctos
    if 'name' not in nuevo_incidente or 'reporte' not in nuevo_incidente or 'status' not in nuevo_incidente or 'fecha' not in nuevo_incidente or 'id' not in nuevo_incidente:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400
    
    incidentes.append(nuevo_incidente)
    return jsonify(nuevo_incidente), 201

# Ruta PUT para actualizar un incidente por ID
@app.route('/incidentes/<string:id>', methods=['PUT'])
def update_incidente(id):
    nuevo_incidente = request.get_json()
    
    for incidente in incidentes:
        if incidente['id'] == id:  # Ahora la comparación es válida
            incidente.update(nuevo_incidente)
            return jsonify(incidente), 200
    
    return jsonify({'error': 'Incidente no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=4000, use_reloader=True)

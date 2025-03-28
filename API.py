from flask import Flask, request, jsonify

app = Flask(__name__)
from Incidentes import incidentes

# Ruta GET para obtener todos los incidentes
@app.route('/incidentes', methods=['GET'])
def get_incidentes():
    return jsonify(incidentes)

# Ruta POST para crear un nuevo incidente
@app.route('/incidentes', methods=['POST'])
def create_incidente():
    # Obtenemos los datos JSON del cuerpo de la solicitud
    nuevo_incidente = request.get_json()
    
    # Validamos si los datos son correctos
    if 'name' not in nuevo_incidente or 'reporte' not in nuevo_incidente or 'status' not in nuevo_incidente or 'fecha' not in nuevo_incidente:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400
    
    # Agregamos el nuevo incidente a la lista
    incidentes.append(nuevo_incidente)
    
    # Devolvemos una respuesta de éxito
    return jsonify(nuevo_incidente), 201

if __name__ == '__main__':
    app.run(debug=True, port=4000)

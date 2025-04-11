// URL base de la API
const apiUrl = 'http://127.0.0.1:4000/incidentes';

// Función para obtener todos los incidentes (GET)
function getIncidentes() {
    console.log('Intentando obtener incidentes...');
    mostrarMensaje('Cargando incidentes...', 'success');
    
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Incidentes obtenidos:', data);
            mostrarIncidentes(data);
            mostrarMensaje('Incidentes cargados correctamente', 'success');
        })
        .catch(error => {
            console.error('Error al obtener incidentes:', error);
            mostrarMensaje('Error al obtener los incidentes: ' + error.message, 'error');
        });
}

// Función para mostrar los incidentes
function mostrarIncidentes(incidentes) {
    const listado = document.getElementById('listado-incidentes');
    if (!listado) {
        console.error('No se encontró el elemento listado-incidentes');
        mostrarMensaje('Error: No se encontró el elemento listado-incidentes', 'error');
        return;
    }
    
    listado.innerHTML = '';
    if (incidentes.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No hay incidentes registrados';
        listado.appendChild(li);
        return;
    }

    incidentes.forEach(incidente => {
        const li = document.createElement('li');
        li.textContent = `ID: ${incidente.id} - ${incidente.name} - ${incidente.status} - ${incidente.fecha}`;
        listado.appendChild(li);
    });
}

// Función para crear un nuevo incidente (POST)
function crearIncidente() {
    const nombre = document.getElementById('nombre').value.trim();
    const reporte = document.getElementById('reporte').value.trim();

    if (!nombre || !reporte) {
        mostrarMensaje('Por favor, complete todos los campos', 'error');
        return;
    }

    const nuevoIncidente = {
        name: nombre,
        reporte: reporte,
        status: 'Abierto',
        fecha: new Date().toISOString().split('T')[0]
    };

    console.log('Creando nuevo incidente:', nuevoIncidente);
    mostrarMensaje('Creando incidente...', 'success');

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nuevoIncidente)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Incidente creado:', data);
            mostrarMensaje('Incidente creado exitosamente', 'success');
            getIncidentes();
            // Limpiar campos
            document.getElementById('nombre').value = '';
            document.getElementById('reporte').value = '';
        })
        .catch(error => {
            console.error('Error al crear incidente:', error);
            mostrarMensaje('Error al crear el incidente: ' + error.message, 'error');
        });
}

// Función para actualizar el estatus de un incidente (PUT)
function actualizarIncidente(id) {
    if (!id) {
        mostrarMensaje('Por favor, ingrese un ID válido', 'error');
        return;
    }

    const nuevoEstatus = document.getElementById('nuevo-estatus').value.trim();
    if (!nuevoEstatus) {
        mostrarMensaje('Por favor, ingrese un nuevo estatus', 'error');
        return;
    }

    // Validar que el estado sea uno de los permitidos
    const estadosPermitidos = ['Abierto', 'En progreso', 'Cerrado'];
    if (!estadosPermitidos.includes(nuevoEstatus)) {
        mostrarMensaje('Estado no válido. Debe ser: Abierto, En progreso o Cerrado', 'error');
        return;
    }

    const datosActualizados = {
        status: nuevoEstatus
    };

    console.log('Actualizando incidente:', id, datosActualizados);
    mostrarMensaje('Actualizando incidente...', 'success');

    fetch(`${apiUrl}/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datosActualizados)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Incidente actualizado:', data);
            mostrarMensaje('Incidente actualizado exitosamente', 'success');
            getIncidentes();
            // Limpiar campos
            document.getElementById('id-incidente').value = '';
            document.getElementById('nuevo-estatus').value = '';
        })
        .catch(error => {
            console.error('Error al actualizar incidente:', error);
            mostrarMensaje('Error al actualizar el incidente: ' + error.message, 'error');
        });
}

// Función para eliminar un incidente (DELETE)
function eliminarIncidente(id) {
    if (!id) {
        mostrarMensaje('Por favor, ingrese un ID válido', 'error');
        return;
    }

    if (!confirm('¿Está seguro que desea eliminar este incidente?')) {
        return;
    }

    console.log('Eliminando incidente:', id);
    mostrarMensaje('Eliminando incidente...', 'success');

    fetch(`${apiUrl}/${id}`, {
        method: 'DELETE'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Incidente eliminado:', data);
            mostrarMensaje('Incidente eliminado exitosamente', 'success');
            getIncidentes();
            // Limpiar campo
            document.getElementById('id-incidente-eliminar').value = '';
        })
        .catch(error => {
            console.error('Error al eliminar incidente:', error);
            mostrarMensaje('Error al eliminar el incidente: ' + error.message, 'error');
        });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM cargado, inicializando eventos...');
    
    const btnCrear = document.getElementById('btn-crear');
    const btnActualizar = document.getElementById('btn-actualizar');
    const btnEliminar = document.getElementById('btn-eliminar');
    const btnRecargar = document.getElementById('btn-recargar');

    if (btnCrear) {
        btnCrear.addEventListener('click', crearIncidente);
        console.log('Evento de crear incidente registrado');
    }

    if (btnActualizar) {
        btnActualizar.addEventListener('click', () => {
            const id = document.getElementById('id-incidente').value;
            actualizarIncidente(id);
        });
        console.log('Evento de actualizar incidente registrado');
    }

    if (btnEliminar) {
        btnEliminar.addEventListener('click', () => {
            const id = document.getElementById('id-incidente-eliminar').value;
            eliminarIncidente(id);
        });
        console.log('Evento de eliminar incidente registrado');
    }

    if (btnRecargar) {
        btnRecargar.addEventListener('click', getIncidentes);
        console.log('Evento de recargar incidentes registrado');
    }

    // Cargar incidentes iniciales
    console.log('Cargando incidentes iniciales...');
    getIncidentes();
});

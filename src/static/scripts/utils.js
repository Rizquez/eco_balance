// ------------------------------------------------------------------------------------------------------------------------------------------------
// LIBRERIAS - APIs NECESARIAS
// ------------------------------------------------------------------------------------------------------------------------------------------------

// ------------------------------------------------------------------------------------------------------------------------------------------------

// addSpecies() - Añade dinamicamente un nuevo grupo de seleccion de especies al contenedor en la interfaz de usuario.
// Este metodo utiliza un contador global para asegurar la unicidad de los identificadores de los elementos DOM involucrados.
let speciesCount = 0 
function addSpecies() {
    var container = document.getElementById('container-div')
    var newDiv = document.createElement('div')

    speciesCount++
    var especieSelectId = `especie-select-${speciesCount}`
    var cantidadId = `cantidad-${speciesCount}`
    var totalAbsorcionId = `total-absorcion-${speciesCount}`

    newDiv.className = 'species-group'

    newDiv.innerHTML = `
        <div class="space-div">
            <label for="${especieSelectId}">Seleccione una especie:</label>
            <select id="${especieSelectId}" onchange="updateAbsorcion('${especieSelectId}', '${cantidadId}', '${totalAbsorcionId}')">
                <option value="" disabled selected>Especies</option>
                ${dct_tress.map(row => `<option value="${row.absorcion_anual}">${row.especie}</option>`).join('')}
            </select>
        </div>
        <div class="space-div">
            <label for="${cantidadId}">Cantidad:</label>
            <input type="number" id="${cantidadId}" name="cantidad" min="1" step="1" oninput="updateAbsorcion('${especieSelectId}', '${cantidadId}', '${totalAbsorcionId}')" required/>
        </div>
        <div class="space-div">
            <label>Total Absorción Anual (tn/CO<sub>2</sub>):</label>
            <input type="text" id="${totalAbsorcionId}" readonly/>
            <button class="space-btn-trash" type="button" onclick="removeSpecies(this)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
            </svg>
            </button>
        </div>
    `
    container.appendChild(newDiv)

    updateButtonVisibility()
}


// updateAbsorcion() - Calcula y actualiza el total de absorcion de CO2 para un grupo especifico de especies basado en la cantidad especificada.
// Esta funcion tambien llama a updateCO2Compensation() para actualizar el total global de compensacion de CO2.
function updateAbsorcion(especieSelectId, cantidadId, totalAbsorcionId) {
    var absorcion = parseFloat(document.getElementById(especieSelectId).value)
    var cantidad = parseInt(document.getElementById(cantidadId).value) || 0 
    var total = absorcion * cantidad

    document.getElementById(totalAbsorcionId).value = isNaN(total) ? '0' : total.toFixed(4)

    updateCO2Compensation()
}


// removeSpecies() - Elimina el grupo de especies especificado y actualiza los totales de arboles y absorcion de CO2.
// Esta funcion se activa desde un boton dentro de cada grupo de especies.
function removeSpecies(button) {
    var parentContainer = button.closest('.species-group')
    var especieSelect = parentContainer.querySelector('select').id
    var cantidadInput = parentContainer.querySelector('input[type="number"]').id
    var totalAbsorcionInput = parentContainer.querySelector('input[type="text"]').id

    updateAbsorcion(especieSelect, cantidadInput, totalAbsorcionInput)

    parentContainer.remove()

    updateTotalTrees()
    updateCO2Compensation()
    updateButtonVisibility()
}


// updateCO2Compensation() - Suma todas las absorciones de CO2 listadas y actualiza la visualizacion del total a compensar.
function updateCO2Compensation() {
    var absorptionInputs = document.querySelectorAll('input[type="text"][id^="total-absorcion"]')
    var totalAbsorbed = 0

    absorptionInputs.forEach(function(input) {
        totalAbsorbed += parseFloat(input.value) || 0
    })

    var currentCO2ToCompensate = parseFloat(totalAbsorbed).toFixed(4)
    document.getElementById('co2ToCompensateDisplay').textContent = `${currentCO2ToCompensate} tn`
}


// updateTotalTrees() - Recuenta y muestra el numero total de arboles seleccionados en todos los grupos de especies.
function updateTotalTrees() {
    let totalTrees = 0

    const inputs = document.querySelectorAll('input[type="number"][name="cantidad"]')
    inputs.forEach(input => {
        const value = parseInt(input.value, 10) || 0
        totalTrees += value
    })

    const totalTreesElement = document.getElementById('totalArboles')
    totalTreesElement.textContent = `Total arboles: ${totalTrees} ud`
}


// updateButtonVisibility() - Verifica la existencia de divs con la clase species-group. Si hay al menos uno, se asegura de que exista 
// un boton en button-container para descargar el grupo.
// Si no hay divs con esa clase, elimina el boton si existe. Esto mantiene el boton adecuadamente sincronizado con la presencia de grupos de especies.
function updateButtonVisibility() {
    const speciesGroups = document.querySelectorAll('.species-group')
    const buttonContainer = document.getElementById('button-container')

    if (speciesGroups.length > 0) {
        if (!buttonContainer.querySelector('button')) {
            const button = document.createElement('button')
            button.textContent = 'Descargar grupo'
            button.id = 'dynamicButton'
            buttonContainer.appendChild(button)
            button.onclick = sendGroupData //asdfasdfasdjfñlaskdjfñlaskdjfñalskdjfñalsdkfj
        }
    } else {
        const existingButton = buttonContainer.querySelector('button')
        if (existingButton) {
            buttonContainer.removeChild(existingButton)
        }
    }
}


// sendGroupData() - Esta funcion recoge todos los valores de los inputs y selects de los elementos con la clase species-group para luego 
// enviarlos al servidor, especificamente a la ruta download-group mendiante AJAX, generando asi el documento para su descarga.
function sendGroupData() {
    var speciesGroups = document.querySelectorAll('.species-group')
    var dataToSend = []

    speciesGroups.forEach(group => {
        var selectElement = group.querySelector('select')
        var especie = selectElement.options[selectElement.selectedIndex].text
        var absorcion = selectElement.value
        var cantidad = group.querySelector('input[type="number"]').value
        var totalAbsorcion = group.querySelector('input[type="text"]').value

        var especieInfo = dct_tress.find(item => item.especie === especie)
        
        if (especie && absorcion && cantidad && totalAbsorcion) {
            dataToSend.push({
                especie: especie,
                absorcion_anual: absorcion,
                cantidad: cantidad,
                absorcion_anual_arbol: totalAbsorcion,
                max_altura_m: especieInfo.max_altura_m, 
                necesidad_hidrica: especieInfo.necesidad_hidrica, 
                tipo: especieInfo.tipo 
            })
        }
    })

    if (dataToSend.length > 0) {
        fetch('/download-group', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "Grupo de plantaciones monoespecificas.xlsx";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
    } else {
        showAlert('Complete todos los campos requeridos en al menos un grupo de especie antes de descargar el grupo 📜')
    }
}


// showAlert(), closeAlert(), submitForm() - Funciones para la gestion de alertas de usuario, envio de datos y manejo de mensajes.
// Estas funciones manejan interacciones mas especificas en el DOM basadas en eventos o acciones del usuario.
function showAlert(msg) {
    document.getElementById('text-alert').textContent = msg
    document.getElementById('customized-alert').style.display = 'block'
}

window.closeAlert = function() {
    document.getElementById('customized-alert').style.display = 'none'
}

function submitForm() {
    document.getElementById('json-data').value = JSON.stringify(dct_tress)
    document.getElementById('downloadForm').submit()
}


// Eventos de DOMContentLoaded - Diversos comportamientos se inician cuando se carga el documento,
// incluyendo la gestion de mensajes de alerta y la navegacion automatica hacia ciertas partes del DOM.
document.addEventListener("DOMContentLoaded", function() {
    if (message != "None" && message) {
        showAlert(message)
    }
})

document.addEventListener("DOMContentLoaded", function() {
    var tableResult = document.getElementById("table-result")
    if (tableResult) {
        tableResult.scrollIntoView({ behavior: "smooth" })
    }
})

document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('container-div')
    container.addEventListener('input', function(event) {
        if (event.target.type === 'number' && event.target.name === 'cantidad') {
            updateTotalTrees()
        }
    })
})

// ------------------------------------------------------------------------------------------------------------------------------------------------
// FIN DEL FICHERO
// ------------------------------------------------------------------------------------------------------------------------------------------------
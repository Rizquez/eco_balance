// ------------------------------------------------------------------------------------------------------------------------------------------------
// LIBRERIAS - APIs NECESARIAS
// ------------------------------------------------------------------------------------------------------------------------------------------------

// ------------------------------------------------------------------------------------------------------------------------------------------------

// Funcion para mostrar en pantalla un mensaje a usuario
function showAlert(msg) {
    document.getElementById('text-alert').textContent = msg
    document.getElementById('customized-alert').style.display = 'block'
}

// Asignacion de la funcion closeAlert al window para que tenga alcance global
window.closeAlert = function() {
    document.getElementById('customized-alert').style.display = 'none'
}

// Extraemos del fichero HTML la variable con el mensaje para verificar si debemos activar el alert
document.addEventListener("DOMContentLoaded", function() {
    if (message != "None" && message) {
        showAlert(message);
    }
});

// Entramos en el DOM, capturamos el ID de la seccion del HTML a donde nos queramos mover y nos dirigimos ahi
document.addEventListener("DOMContentLoaded", function() {
    var tableResult = document.getElementById("table-result");
    if (tableResult) {
        tableResult.scrollIntoView({ behavior: "smooth" });
    }
});

// ------------------------------------------------------------------------------------------------------------------------------------------------
// FIN DEL FICHERO
// ------------------------------------------------------------------------------------------------------------------------------------------------
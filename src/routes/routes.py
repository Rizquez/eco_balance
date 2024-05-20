# -------------------------------------------------------------------------------------------------------------------------------------------------
# IMPORTACION DE LIBRERIAS

from flask import Flask, render_template, redirect, request
# -------------------------------------------------------------------------------------------------------------------------------------------------

# Instanciamos la app
app = Flask(__name__, template_folder='../templates', static_folder='../static')


# Ruta raiz para el calculo
@app.route('/', methods=['GET', 'POST'])
def home():

    # Verificamos si se enviaron datos
    if request.method == 'POST':

        # Extraemos los datos de la peticion 
        co2_capture = request.form.get('co2-capture')
        tree_number = request.form.get('tree-number')

        return render_template('index.html', co2_capture=co2_capture, tree_number=tree_number)
    
    # Si no es POST, simplemente cargamos la pagina sin datos de resultado
    return render_template('index.html')

# Manejador de errores mas comunes
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    return redirect('/error')


# Ruta para la salida de errores
@app.route('/error')
def error():
    return render_template("page_error.html")

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------
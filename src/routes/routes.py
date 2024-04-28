# -------------------------------------------------------------------------------------------------------------------------------------------------
# IMPORTACION DE LIBRERIAS

from flask import Flask, render_template, redirect
# -------------------------------------------------------------------------------------------------------------------------------------------------

# Instanciamos la app
app = Flask(__name__, template_folder='../templates', static_folder='../static')


# Ruta raiz para el calculo
@app.route('/', methods=['GET'])
def home():
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
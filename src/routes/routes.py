# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
from ..models import obtain_trees
from flask import Flask, render_template, redirect, request
# -------------------------------------------------------------------------------------------------------------------------------------------------

# Instanciamos la app
app = Flask(__name__, template_folder='../templates', static_folder='../static')


# Ruta raiz para el calculo
@app.route('/', methods=['GET', 'POST'])
def home():
    # Verificamos si se enviaron datos
    if request.method == 'POST':

        # Extraemos los datos de la peticion aplicando un casting
        co2_capture = float(request.form.get('co2-capture'))
        tree_number = int(request.form.get('tree-number'))

        # Llamamos al metodo para realizar el filtrado sobre los datos introducidos por el usuario
        dct_tress = obtain_trees(tree_number, co2_capture)

        # Verificamos si dct_tress se encuentra vacio, esto indica que no hay arboles para la cantidad de 
        # CO2 señalada y crearemos un mensaje para el usuario, en caso contrario instanciamos la variable a None
        message = "Se recomienda agregar más unidades arbóreas para suplir las necesidades de captura indicadas 🌱" if not dct_tress else None

        # Renderizamos el template index con los datos a insertar
        return render_template('index.html', table_data=dct_tress, tree_number=tree_number, co2_capture=co2_capture, message=message)
    
    # Si no es POST, simplemente cargamos la pagina sin datos de resultado
    return render_template('index.html', table_data=None, tree_number=None, co2_capture=None, message=None)


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
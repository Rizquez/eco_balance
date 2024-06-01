# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import json
import pandas as pd
from io import BytesIO
from ..models import obtain_trees
from ..utils import create_xlsx_file, format_dataframe
from flask import Flask, render_template, redirect, request, send_file
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
        return render_template('index.html', dct_tress=dct_tress, tree_number=tree_number, co2_capture=co2_capture, message=message)
    
    # Si no es POST, simplemente cargamos la pagina sin datos de resultado
    return render_template('index.html', dct_tress=None, tree_number=None, co2_capture=None, message=None)


# Ruta para descargar los documentos
@app.route('/download', methods=['GET', 'POST'])
def download_file():
    # Constantes de calculo
    NAME_FILE = 'Calculador de Carbono Capturado.xlsx'
    NAME_SHEET = 'Arbolado'
    NAME_TABLE = 'Especies_Captura_Carbono'
    FLOAT_FORMAT = '%.4f'

    # Primero que nada vamos a extraer el diccionario con los datos de los arboles filtrados
    request_data = request.form.get('data')
    dct_tress = json.loads(request_data)

    # Creamos un DataFrame de pandas con los datos de la tabla
    df = pd.DataFrame(dct_tress)

    # Formateamos el dataframe antes de almacenarlo
    df = format_dataframe(df)

    # Instanciamos y escribimos los datos en la ruta de salida que nos pasan como parametro
    # Usando un buffer en memoria para guardar el archivo Excel
    # Almacenando el dataframe con los diferentes parametros que nos interesan
    excel_file = BytesIO()
    create_xlsx_file(excel_file, NAME_TABLE, NAME_SHEET, df, 'w', FLOAT_FORMAT)

    # Movemos el puntero al inicio del buffer
    excel_file.seek(0)

    return send_file(
        excel_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=NAME_FILE
        )


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
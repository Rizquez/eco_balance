# -------------------------------------------------------------------------------------------------------------------------------------------------
# IMPORTACION DE LIBRERIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import os
import time
import pandas as pd
import openpyxl
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
load_dotenv(override=False)
# -------------------------------------------------------------------------------------------------------------------------------------------------

class MySQLDataManager():
    """
    Apply:
    ------
    CLASE PARA GESTIONAR LAS FUNCINES QUE REALIZAR CONSULTAS EN LA BBDD DE MYSQL. 

    Notes:
    ------
    - No es necesario instanciar un objeto para utilizar los metodos de esta clase.
    - La información detallada acerca del alcance de aplicación de cada método público se encuentra internamente en su respectiva documentación.

    Parameters:
    -----------
    - None.

    Public Methods:
    -----------------
    - `create_engine_mysql`
    - `table_query`
    """

    @classmethod
    def create_engine_mysql(self, max_retries=10, delay=30):
        """
        Apply:
        ------
        Método para realizar la conexión a la base de datos MySQL utilizando SQLAlchemy.

        Parameters:
        -----------
        max_retries: `int`
            Default: `10`
                Cantidad máxima de veces que se desea realizar los intentos de conexión.

        delay: `int`
            Default: `30`
                Tiempo (en segundos) que esperará el método para reintentar cada conexión en caso de que no se haya logrado.

        Returns:
        --------
        - Objeto SQLAlchemy.Engine de la librería SQLAlchemy.
        """
        # Extraemos los datos de conexión de las variables de entorno
        db = os.getenv('MYSQL_DB')
        host = os.getenv('MYSQL_HOST')
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')

        # Creamos la URL de conexion
        url_connection = URL.create(
            drivername='mysql+pymysql',
            username=user,
            password=password,
            host=host,
            database=db
        )

        # Vamos a realizar un bucle for sobre la cantidad de intentos maximos requeridos
        for attempt in range(max_retries):
            try:
                # Probamos crear el engine con la URL de conexion y retornarlo
                return create_engine(url_connection)

            # En caso contrario reintentamos la conexion hasta el maximo de intentos y luego retornamos un error
            except OperationalError:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise

    @classmethod
    def table_query(self, engine, consulta, params=None):
        """
        Método para realizar una consulta sobre una BBDD MySQL y devolver un DataFrame de pandas.

        Parameters:
        -----------
        engine: `SQLAlchemy.Engine`
            Objeto engine de la librería SQLAlchemy generado mediante el método `create_engine_mysql`.

        consulta: `str`
            Consulta en SQL para realizar sobre la base de datos en la cual se generó el objeto engine.

        params: `dict`
            Default: None
            Diccionario que sirve para indicar el valor de los parámetros que son necesarios para la ejecución de la consulta de SQL.

        Returns:
        --------
        - DataFrame con la tabla o el conjunto de datos de la tabla que se quiso extraer de la base de datos.
        """
        with engine.begin() as connection:
            df = pd.read_sql_query(text(consulta), connection, params=params)
            return df


def format_dataframe(df):
    """
    Apply:
    ------
    Metodo para darle formato al dataframe que se quiera almacenar en Excel para posterior descarga por parte del usuario.

    Parameters:
    -----------
    df: ``pd.core.frame.Dataframe``
        Dataframe al que se le quiere dar formato.

    Returns:
    --------
    - Dataframe formateado para su almacenado en Excel.
    """
    # Instaciamos el diccionario para mapear el nombre de las columnas
    dct_remane = {
        'especie': 'Especie',
        'max_altura_m': 'Máxima Altura (m)',
        'necesidad_hidrica': 'Necesidad Hídrica',
        'tipo': 'Tipo',
        'absorcion_anual':'Absorción Anual(ton/CO2 - Árbol)',
        'absorcion_anual_arbol':'Absorción Anual(ton/CO2 - Arbolada)'				
    }

    # Instanciamos el diccionario para mapear el tipo de dato de las columnas
    dct_data =  {
        'max_altura_m': 'int64',
        'absorcion_anual':'float64',
        'absorcion_anual_arbol':'float64'	
    }

    # Vamos a dar formato a las columnas con los numeros flotantes
    df = df.astype(dct_data)

    # Renombramos las columnas
    df.rename(dct_remane, axis=1, inplace=True)

    # Ahora reordenamos las columnas y retornamos el dataframe
    return df.reindex(list(dct_remane.values()), axis=1)


def create_xlsx_file(file_name, tbl_name, sheet_name, df, mode, float_format, styletbl='TableStyleMedium14'):
    """
    Apply:
    ------
    Metodo para crear o añadir una tabla de datos por cada hoja sobre una ficha de excel.

    Parameters:
    -----------
    file_name: ``str``
        Ruta absoluta para el guardado de la ficha excel.

    tbl_name: ``str``
        Nombre que se desea posea la tabla.

    sheet_name: ``str``
        Nombre que se desea posea la hoja.

    df: ``pd.core.frame.Dataframe``
        Dataframe con el que se creara la tabla en la ficha excel.

    mode: ``str``
        Tipo de guardado, puede ser escritura ``w`` o añadidura ``a``.

    float_format: ``str``
        Formato que tendran los numero decimales.

    styletbl: ``str``
        Default: ``TableStyleMedium9``
            Estilo que se le desea aplicar a la tabla que se va a crear en el Excel.

    Returns:
    --------
    - None.
    """
    # Generamos el estilo de las tablas que contendra el fichero .xlsx
    estiloTabla = openpyxl.worksheet.table.TableStyleInfo(name=styletbl, showFirstColumn=False, showLastColumn=False)

    # Instanciamos y escribimos los datos en la ruta de salida que nos pasan como parametro
    with pd.ExcelWriter(file_name, mode=mode) as writer:

        # Almanecamos el df con los diferentes parametros que nos interesan
        df.to_excel(writer, sheet_name=sheet_name, index=False, float_format=float_format)

    # Movemos el puntero al inicio del buffer
    file_name.seek(0)

    # Abrimos el workbook
    wb = openpyxl.load_workbook(filename=file_name)

    # Dimensionamos las tablas con los respectivos df
    dimenTbl = f'A1:{openpyxl.utils.get_column_letter(df.shape[1])}{len(df)+1}'
    tabla = openpyxl.worksheet.table.Table(displayName=tbl_name, ref=dimenTbl)

    # Asignamos el estilo a las tablas
    tabla.tableStyleInfo = estiloTabla

    # Asignamos las tablas a cada hoja correspondiente
    wb[sheet_name].add_table(tabla)

    # Ajustamos las columnas
    wb = _adjust_excel_columns(wb, sheet_name)

    # Para finalizar guardamos el workbook
    file_name.seek(0)
    wb.save(file_name)
    

def _adjust_excel_columns(wb, sheet_name, h='center'):
    """
    Apply:
    ------
    Esta funcion ajusta las columnas de todas las tablas en una hoja de excel.
    
    Parameters:
    -----------
    wb: ``Openpyxl.Woorkbook``
        Objeto de la libreria Openpyxl.

    sheet_name: ``str``
        Nombre de la hoja donde se encuentra la tabla.

    h: ``str``
        Default ``center``
            Tipo de justificacion que se requiere en la tabla, por defecto sera centrado.
    
    Returns:
    --------
    - Retorna el mismo objeto workbook pero con las columnas y sus datos centrados en todas las tablas 
    contenidas en la hoja indicada.
    """
    PLUS_LENGTH = 8
    for column in wb[sheet_name].columns:   
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
                cell.alignment = openpyxl.styles.Alignment(horizontal=h)
            except AttributeError:
                pass
        adjusted_width = (max_length + PLUS_LENGTH)
        wb[sheet_name].column_dimensions[column[0].column_letter].width = adjusted_width
    return wb

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------
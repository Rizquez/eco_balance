# -------------------------------------------------------------------------------------------------------------------------------------------------
# IMPORTACION DE LIBRERIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import os
import time
import pandas as pd
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

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import os
import binascii
# -------------------------------------------------------------------------------------------------------------------------------------------------

class Config(object):
    """
    Apply:
    ------
    ESTA ES LA CLASE BASE DE CONFIGURACIÓN Y ACTUA COMO UNA PLANTILLA PARA TODAS LAS DEMAS CONFIGURACIONES.

    AQUI SE DEFINEN LAS CONFIGURACIONES QUE SON COMUNES A TODOS LOS ENTORNOS DE LA APP.
    """
    # Configuramos el rastreo de modificaciones sobre SQLAlchemy para optimizar recursos
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Apply:
    ------
    ESTA CLASE HEREDA A CONFIG Y SE UTILIZA ESPECIFICAMENTE PARA DEFINIR LA CONFIGURACOIN EL ENTORNO DE DESARROLLO.
    """
    # Aqui vamos a configurar el entorno como desarrollo, activamos el modo depuracion y el modo testing.
    ENV = 'development'
    HOST = '127.0.0.1'
    PORT = '5000'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """
    Apply:
    ------
    ESTA CLASE HEREDA A CONFIG Y SE UTILIZA ESPECIFICAMENTE PARA DEFINIR LA CONFIGURACOIN EL ENTORNO DE PRODUCCION.
    """
    # Aqui vamos a configurar el entorno como produccion, desactivamos el modo depuracion y el modo testing.
    # Ademas de creamos una clave secreta que sera utilizada por Flask para realizar tareas de seguridad.
    SECRET_KEY = binascii.hexlify(os.urandom(48)).decode()
    ENV = 'production'
    HOST = '0.0.0.0'
    PORT = '5000'
    DEBUG = False
    TESTING = False

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------
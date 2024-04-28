# -------------------------------------------------------------------------------------------------------------------------------------------------

# Las diferentes clases almacenadas en este fichero sirven de base para la configuracion de la APP segun el entorno 
# en donde se este ejecutando.

# Leer el fichero main.py para saber sobre la configuracion por defecto.

# Para saber como seleccionar el tipo de configuracion se invita a leer el fichero README.md

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(Config):
    APP_ENV = 'local'
    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    APP_ENV = 'development'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    SECRET_KEY = '6Hasb94fjzDTGqd3WBMxVmmcByXYbsgIFEApss8vLJHDx1wJmp2RZmztMJAF7vQh'
    APP_ENV = 'production'
    DEBUG = False
    TESTING = False

# Diccionario para recoger las diferentes clases bases de configuracion de la API
dct_config = {
    'development': DevelopmentConfig,
    'local': LocalConfig,
    'production': ProductionConfig
}

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------
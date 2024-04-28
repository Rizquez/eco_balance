# -------------------------------------------------------------------------------------------------------------------------------------------------
# IMPORTACION DE LIBRERIAS

import os
from config import config
from src.routes import app
# -------------------------------------------------------------------------------------------------------------------------------------------------

# OPERATIVO
# -------------------------------------------------------------------------------------------------------------------------------------------------

# Por defecto siempre vamos a instanciar la API en modo de desarrollo, en caso de que no se indique otro modo de ejecucion
env = os.getenv('FLASK_ENV', 'development')

# Aplicamos las diferentes configuraciones sobre una APP
app.config.from_object(config[env])

# Una vez realizada toda la configuracion, iniciamos la app.
if __name__ == '__main__':
    app.run()

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------
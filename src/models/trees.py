# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
from ..utils import MySQL
# -------------------------------------------------------------------------------------------------------------------------------------------------

def obtain_trees(tree_number, co2_capture):
    """
    Apply:
    ------
    Método para realizar la conexión a la base de datos MySQL utilizando SQLAlchemy.

    Parameters:
    -----------
    tree_number: `float`
        Cantidad de arboles que se desean plantar.

    co2_capture: `float`
        Cantidad de CO2 que se desea capturar al año.

    Returns:
    --------
    - Diccionario con los datos filtrados del dataframe en funcion de la solicitud del cliente.
    """
    # Instanciamos la lista con las columnas que vamos a extraer para llevar a la app
    lst_columns = [
        'especie',
        'max_altura_m',
        'necesidad_hidrica',
        'tipo',
        'absorcion_anual',
        'absorcion_anual_arbol'
        ]

    # ---------------------------------------------------------------------------------------------------------------------------------------------
    # *** EXTRACCION DE DATOS SOBRE LOS ARBOLES DISPONIBLES EN LA BBDD ***
    engine = MySQL.create_engine_mysql()
    df_trees = MySQL.table_query(engine, "SELECT * FROM especie_arboles")
    engine.dispose()

    # ---------------------------------------------------------------------------------------------------------------------------------------------
    # *** CALCULOS Y FILTRADOS ***

    # La columna de absorcion extraida de la bbdd es la cantidad que absorbe cada especie durante los primeros 20 años de vida 
    # pero necesitamos la absorcion anual
    df_trees['absorcion_anual'] = df_trees['absorcion']/20

    # Ahora con la cantidad de arboles que se quieren plantar vamos a calcular cuanto seria la absorcion anual de dicha cantidad
    df_trees['absorcion_anual_arbol'] = df_trees['absorcion_anual'] * tree_number

    # Por ultimo con la cantidad de CO2 que se quiere absorber se filtran todos los arboles que puedan cumplir con esta condicion
    df_filter = df_trees.loc[df_trees['absorcion_anual_arbol'] >= co2_capture, lst_columns].reset_index(drop=True)

    # Verificamos si el dataframe tiene datos para redondear los valores numericos y almacenarlos
    if not df_filter.empty:

        # Redondeamos los valores decimales hasta un maximo de 4 decimales
        df_filter = df_filter.applymap(lambda row: f'{row:.4f}' if type(row) == float else row)

        # Y por ultimos extraemos el conjunto de datos del dataframe
        dct_tress = df_filter.to_dict(orient='records')

    # En caso de que no haya datos se retornara un None
    else:
        dct_tress = None
    
    return dct_tress
    
# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------
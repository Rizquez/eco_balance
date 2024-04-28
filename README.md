# La ciudad como sumidero de Carbono

## Descripcion del proyecto
Este proyecto desarrolla una interfaz de usuario que permite calcular la emisión de carbono de los proyectos de edificación. La herramienta proporciona análisis detallados sobre cómo diferentes especies de plantas y árboles pueden ser utilizados para mitigar estas emisiones, contribuyendo así a la lucha contra el cambio climático y promoviendo la sostenibilidad urbana.

## Contexto
La mayor reserva de carbono biológicamente activo de los ecosistemas terrestres se encuentra en los primeros dos metros de suelo. En un contexto de cambio climático intensificado, es crucial entender y mitigar las emisiones de carbono en ambientes urbanos. El carbono orgánico del suelo juega un papel fundamental en la regulación del clima, el suministro de agua, y la biodiversidad, ofreciendo servicios esenciales para el bienestar humano.

## Objetivo
El objetivo de esta herramienta es doble:
1. Analizar y detectar interferencias en el ciclo de carbono dentro de entornos urbanos, considerando factores como suelos, vegetación, pavimentación y edificación.
2. Investigar y aplicar técnicas efectivas para la captación y retención de CO2, incluyendo:
   - Técnicas edafológicas.
   - Uso estratégico de vegetación.
   - Innovaciones tecnológicas.

## Funcionalidad
La interfaz permite a los usuarios:
- Calcular las emisiones de carbono específicas de proyectos de edificación.
- Recibir recomendaciones sobre tipos de plantas y técnicas para mitigar las emisiones detectadas.
- Visualizar la distribución efectiva de especies vegetales en planos y elevaciones para maximizar la captura de carbono.

## Estructura del proyecto
```
├── config
│   └── config.py
├── src
│   ├── routes
│   ├── static
│   ├── templates
│   └── utils
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

> [!NOTE]
> Todo el proyecto esta desarrollado en el Framework `Flask` de `Python`.

## Creacion del entorno de virtual
Se necesitara tener instalada previamente la libreria 'virtualenv', en caso contrario se podra instalar ejecutando el siguiente comando:
```
pip install virtualenv
```

Una vez instalada, para crear un entorno de desarrollo se debe ejecutar:
```
virtualenv venv
```

> [!TIP]
Se recomienda la creación de un entorno virtual para optimizar el desarrollo y la ejecución del proyecto.

## Dependencias
Comando para instalar las dependencias necesarias sobre este proyecto:
```
pip install -r requirements.txt
```

Comando para crear o actualizar el archivo txt que almacena las dependencias del proyecto:
```
pip freeze > requirements.txt  
```

## Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor haz un 'fork' del repositorio, crea una rama con tus mejoras y envía un 'pull request'.

## Licencia
Este proyecto está bajo la Licencia `GPL-3.0`, lo que permite el uso, distribución y modificación del software bajo ciertas condiciones. Consulta el archivo LICENSE para más detalles.
# BKLibOra

BKLibOra es una librería Python para facilitar la conexión, gestión y modelado de datos en bases de datos Oracle. Utiliza `SQLAlchemy`, `oracledb` y `cx_Oracle` para ofrecer una forma robusta, reutilizable y organizada de trabajar con Oracle Database en proyectos personales o educativos.

## Estructura del Proyecto

```
BKLibOra
│   config.py
│   __init__.py
│
├───BKOraConnect
│       BKOraConnect.py
│       __init__.py
│
├───BKOraManager
│       BKOraManager.py
│       BKOraManagerDB.PY
│       __init__.py
│
└───BKOraModel
    │   BKOraModel.py
    │   BKOraModelDB.py
    │   __init__.py
    │
    └───BKOraModel_utils
            BKOraColums.py
            __init__.py
```


## Características

- Conexión flexible a Oracle mediante `oracledb` y/o `cx_Oracle`.
- Gestor centralizado de consultas SQL.
- Modelado de resultados tipo ORM sin usar mapeo completo (ligero y funcional).
- Separación clara de responsabilidades en módulos.
- Enfoque educativo y reutilizable para pruebas o desarrollos personales.

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tu_usuario/BKLibOra.git
cd BKLibOra
```

2. Instala las dependencias:

```pip
pip install -r requirements.txt
```

## Uso basico

```python
from BKLibOra.BKOraConnect.BKOraConnect import BKOraConnect
from BKLibOra.BKOraManager.BKOraManager import BKOraManager
from BKLibOra.BKOraModel.BKOraModel import BKOraModel

# Conexión
connector = BKOraConnect(user='usuario', password='clave', service_name='XEPDB1')
session = connector.get_session()

# Manager
manager = BKOraManager(session)
resultado = manager.execute_query("SELECT * FROM empleados")

# Modelado
modelo = BKOraModel(resultado)
data = modelo.as_dict_list()
print(data)
```

## Dependencias

- SQLAlchemy
- oracledb
- cx_Oracle

## Estado del Proyecto

Este proyecto está en desarrollo activo y se encuentra en fase de pruebas educativas. No se recomienda su uso en entornos de producción.

## Licencia

Este proyecto se distribuye bajo licencia MIT. Libre para usar con fines educativos y de prueba.
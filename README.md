# BKLibOra

**BKLibOra** es una librería/API en Python diseñada para simplificar la conexión, ejecución de consultas y modelado de datos en bases de datos **Oracle**. Está pensada para proyectos personales, educativos o de prueba, ofreciendo una estructura reutilizable y ligera basada en `SQLAlchemy`, `oracledb` y `cx_Oracle`.

---

## 🚀 Características principales

- ✅ Conexión sencilla y flexible a Oracle.
- ✅ Ejecución centralizada de consultas SQL.
- ✅ Modelado ligero de resultados tipo ORM (sin necesidad de definir clases por tabla).
- ✅ Separación clara de responsabilidades (conexión, gestión, modelado, utilidades).
- ✅ Ideal para uso **educativo**, pruebas o scripts internos.

---

## 📁 Estructura del proyecto

```
BKLibOra
│   config.py                 # Configuración común
│   utils.py                  # Funciones auxiliares generales
│
├───BKOraConnect              # Módulo de conexión
│       BKOraConnect.py
│
├───BKOraDatabaseInfo         # Consultas específicas sobre metadatos y estado de Oracle
│   ├───MgrdbAllPrimaryKey
│   ├───MgrdbAllSequences
│   ├───MgrdbAllSessionActive
│   ├───MgrdbAllTableDependencies
│   ├───MgrdbCurrentExecuteQuery
│   ├───MgrdbJobScheduler_DetailsWithProgramAndSchedule
│   ├───MgrdbJobScheduler_StatusWithErrorInfo
│   ├───MgrdbSessionLock
│   └───MgrdbTableStructure
│
├───BKOraManager              # Gestión y ejecución de consultas
│       BKOraManager.py
│       BKOraManagerDB.py
│       BKOraManager_utils.py
│       BKOraQueryBuilder.py
│
└───BKOraModel                # Transformación de resultados a objetos
        BKOraColums.py
        BKOraDataType.py
        BKOraModel.py
        BKOraModelComplex.py
        BKOraModelDB.py
```

---

## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/BKLibOra.git
cd BKLibOra
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## 🧪 Ejemplo de uso básico

```python
from BKLibOra.BKOraConnect.BKOraConnect import BKOraConnect
from BKLibOra.BKOraManager.BKOraManager import BKOraManager
from BKLibOra.BKOraModel.BKOraModel import BKOraModel

# Establecer conexión
connector = BKOraConnect(user='usuario', password='clave', service_name='XEPDB1')
session = connector.get_session()

# Ejecutar consulta
manager = BKOraManager(session)
resultado = manager.execute_query("SELECT * FROM empleados")

# Convertir a lista de diccionarios
modelo = BKOraModel(resultado)
data = modelo.as_dict_list()

print(data)
```

---

## 📦 Dependencias

- [`SQLAlchemy`](https://www.sqlalchemy.org/)
- [`oracledb`](https://oracle.github.io/python-oracledb/)
- [`cx_Oracle`](https://cx-oracle.readthedocs.io/)

---

## 📌 Estado del proyecto

Este proyecto está en desarrollo activo y se encuentra en fase de validación educativa.  
**No se recomienda su uso en entornos de producción.**

"""
Módulo BKOraModel
-----------------

Este módulo proporciona la clase base `BKOraModel`, pensada para representar objetos de modelo compatibles con estructuras
de bases de datos, permitiendo una conversión sencilla entre diccionarios y objetos Python.

La clase está diseñada para ser utilizada con el gestor `BKOraManagerDB`, permitiendo que las consultas SQL
puedan ser representadas como listas de objetos de modelo.

Clases:
    BKOraModel
"""


class BKOraModel:
    """
    Clase base para modelos que representan filas de una tabla de base de datos.

    Esta clase permite la conversión bidireccional entre diccionarios y objetos, lo cual facilita la interacción
    con los resultados de consultas SQL y operaciones CRUD.

    Métodos:
        from_dict(data_dict): Crea una instancia del modelo a partir de un diccionario.
        from_list(data_list): Crea una lista de instancias del modelo a partir de una lista de diccionarios.
        to_dict(): Convierte la instancia del modelo en un diccionario.
    """

    def __init__(self, **kwargs):
        """
        Inicializa una instancia del modelo asignando dinámicamente los atributos proporcionados como argumentos clave-valor.

        Args:
            **kwargs: Claves y valores que se asignarán como atributos del objeto.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, data_dict):
        """
        Crea una instancia del modelo a partir de un diccionario.

        Args:
            data_dict (dict): Diccionario con claves correspondientes a atributos del modelo.

        Returns:
            BKOraModel: Instancia de la clase modelo.
        """
        return cls(**data_dict)

    @classmethod
    def from_list(cls, data_list):
        """
        Crea una lista de instancias del modelo a partir de una lista de diccionarios.

        Args:
            data_list (list[dict]): Lista de diccionarios.

        Returns:
            list[BKOraModel]: Lista de instancias del modelo.
        """
        return [cls.from_dict(item) for item in data_list]

    def to_dict(self):
        """
        Convierte la instancia actual del modelo en un diccionario.

        Returns:
            dict: Diccionario con los atributos del objeto.
        """
        return self.__dict__

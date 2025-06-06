from typing import Union

def get_byte_size(data: Union[str, bytes, None], encoding='utf-8') -> int:
    """
    Devuelve la cantidad de bytes utilizados por el dato proporcionado.

    Esta función calcula el tamaño en bytes de una entrada que puede ser una cadena de texto,
    una secuencia de bytes o `None`. Si se proporciona una cadena (`str`), se codificará 
    usando la codificación especificada (por defecto 'utf-8') antes de calcular su tamaño.

    Args:
        data (Union[str, bytes, None]): El dato cuya cantidad de bytes se desea medir.
            - Si es `str`, se codificará antes de medir.
            - Si es `bytes`, se devolverá su longitud directamente.
            - Si es `None`, se devuelve 0.
        encoding (str, opcional): Codificación a usar si `data` es una cadena. 
            Por defecto se utiliza 'utf-8'.

    Returns:
        int: La cantidad de bytes que ocupa la entrada.

    Raises:
        TypeError: Si el tipo de dato no es `str`, `bytes` ni `None`.

    Ejemplos:
        >>> get_byte_size("Hola")
        4

        >>> get_byte_size("á")
        2

        >>> get_byte_size(b"abc")
        3

        >>> get_byte_size(None)
        0
    """
    if data is None:
        return 0
    elif isinstance(data, bytes):
        return len(data)
    elif isinstance(data, str):
        return len(data.encode(encoding))
    else:
        raise TypeError("Solo se aceptan valores de tipo str, bytes o None.")

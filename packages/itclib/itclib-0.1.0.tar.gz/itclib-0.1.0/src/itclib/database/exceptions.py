"""
Módulo de definición de excepciones personalizadas.
"""


class NullsDataframe(Exception):
    """
    Excepción lanzada cuando se detectan valores nulos en un DataFrame.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class FormatPointlist(Exception):
    """
    Excepción lanzada cuando hay problemas de formato en una lista de puntos.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EmptyPointlist(Exception):
    """
    Excepción lanzada cuando una lista de puntos está vacía.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CustomError(Exception):
    """
    Excepción genérica para manejar errores personalizados.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

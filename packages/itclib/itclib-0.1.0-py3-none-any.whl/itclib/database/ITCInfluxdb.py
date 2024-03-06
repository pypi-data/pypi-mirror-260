"""
Script que define la clase InfluxDBClientITC para facilitar las tareas relacionadas
con la ejecución de acciones en una base de datos del tipo InfluxDB.
"""

import logging
import sys
from typing import List, Literal, Optional, Union

import exceptions as exc
import numpy as np
import pandas as pd
from dateutil.parser import parse
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError


class ITCInfluxDB:
    """
    Clase para interactuar con una base de datos InfluxDB.

    Permite la conexión y la interacción con una base de datos InfluxDB.

    :param host: La dirección IP o el nombre de dominio del host de InfluxDB.
    :type host: str
    :param port: El puerto de conexión a InfluxDB. Por defecto es 8086.
    :type port: int, optional
    :param timeout: El tiempo de espera en segundos para las solicitudes a InfluxDB. Por defecto es 10 segundos.
    :type timeout: int, optional
    :param verbose: Indica si se deben imprimir mensajes informativos durante la ejecución. Por defecto es True.
    :type verbose: bool, optional
    """

    def __init__(
        self,
        host: str,
        port: int = 8086,
        timeout: int = 10,
        verbose: bool = True,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase ITCInfluxDB.

        Establece una conexión con el servidor de InfluxDB especificado y comprueba la conexión.

        :param host: La dirección IP o el nombre de dominio del host de InfluxDB.
        :type host: str
        :param port: El puerto de conexión a InfluxDB. Por defecto es 8086.
        :type port: int, optional
        :param timeout: El tiempo de espera en segundos para las solicitudes a InfluxDB. Por defecto es 10 segundos.
        :type timeout: int, optional
        :param verbose: Indica si se deben imprimir mensajes informativos durante la ejecución. Por defecto es True.
        :type verbose: bool, optional
        :raises ConnectionError: Si no se puede establecer una conexión con el servidor InfluxDB.
        """

        if verbose:
            # Configurar el nivel de registro a INFO y establecer el formato
            logging.basicConfig(
                level=logging.INFO,
                format="[%(asctime)s] [%(levelname)s]: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

        self.host = host
        self.port = port
        self.client = InfluxDBClient(host=self.host, port=self.port, timeout=timeout)

        # Comprobar conexión satisfactoria con el servidor InfluxDB
        try:
            self.client.ping()
            logging.info("Conexión satisfactoria con el servidor InfluxDB.")
        except ConnectionError:
            msg_error = f"Servidor InfluxDB no disponible con IP {self.host}."
            logging.error(msg_error)
            # Cierra el cliente antes de lanzar la excepción para asegurar la limpieza
            self.client.close()
            # Detiene la ejecución del programa
            sys.exit(1)

    def __parser_datetime(
        self,
        datetime_string: str,
        format_string: str = "%Y-%m-%dT%H:%M:%SZ",
    ) -> Union[str, None]:
        """
        Parsea una cadena de fecha y hora en el formato especificado.

        :param datetime_string: La cadena de fecha y hora a parsear.
        :type datetime_string: str
        :param format_string: El formato de la cadena de fecha y hora. Por defecto: "%Y-%m-%dT%H:%M:%SZ".
        :type format_string: str
        :return: La fecha y hora parseada en el formato especificado.
        :rtype: str
        """
        try:
            parsed_datetime = parse(datetime_string)
            formatted_datetime = parsed_datetime.strftime(format_string)
            return formatted_datetime
        except TypeError:
            # Si se produce un TypeError, significa que el formato de la cadena de fecha y hora no es válido para parsear.
            # En este caso, podemos devolver un mensaje de error indicando que ha habido un problema con el formato de entrada.
            error_message = f"Error: No se pudo parsear la cadena '{datetime_string}' con el formato '{format_string}'."
            return error_message

    def build_query(
        self,
        measurement: str,
        variables: Optional[List[str]] = None,
        start_datetime: Optional[str] = None,
        end_datetime: Optional[str] = None,
        group_by: Optional[str] = None,
    ) -> str:
        """
        Construye una consulta para obtener datos de una base de datos.

        :param measurement: La medida de la base de datos de la cual se obtendrán los datos.
        :type measurement: str
        :param variables: Las variables que se desean obtener.
        :type variables: List[str], optional
        :param start_datetime: La fecha y hora de inicio del intervalo de tiempo de los datos (opcional).
        :type start_datetime: str, optional
        :param end_datetime: La fecha y hora de finalización del intervalo de tiempo de los datos (opcional).
        :type end_datetime: str, optional
        :param group_by: La ventana de tiempo para agrupar los datos (opcional).
        :type group_by: str, optional
        :return: La consulta construida.
        :rtype: str

        :example:
        >>> client = ITCInfluxDB(host="example.com", port=8086, verbose=True)
        >>> query = client.build_query(
        ...     measurement="weather_data",
        ...     variables=["temperature", "humidity"],
        ...     start_datetime="2023-01-01T00:00:00Z",
        ...     end_datetime="2023-01-02T00:00:00Z",
        ...     group_by="1h",
        ... )
        >>> print(query)
        SELECT temperature, humidity FROM weather_data WHERE time >= '2023-01-01T00:00:00Z' AND time <= '2023-01-02T00:00:00Z' GROUP BY time(1h)
        """
        query_datetime = ""

        if isinstance(start_datetime, str) and isinstance(end_datetime, str):
            # Si se proporcionan tanto la fecha de inicio como la de finalización, construir una consulta para el intervalo de tiempo especificado
            start_datetime_iso = self.__parser_datetime(start_datetime)
            end_datetime_iso = self.__parser_datetime(end_datetime)
            query_datetime = (
                f"WHERE time >= '{start_datetime_iso}' AND time <= '{end_datetime_iso}'"
            )
        elif isinstance(start_datetime, str) and not isinstance(end_datetime, str):
            # Si solo se proporciona la fecha de inicio, construir una consulta desde la fecha de inicio hasta "now()"
            start_datetime_iso = self.__parser_datetime(start_datetime)
            query_datetime = f"WHERE time >= '{start_datetime_iso}' AND time <= now()"
        elif not isinstance(start_datetime, str) and isinstance(end_datetime, str):
            # Si solo se proporciona la fecha de finalización, construir una consulta desde el principio hasta la fecha de finalización
            end_datetime_iso = self.__parser_datetime(end_datetime)
            query_datetime = f"WHERE time <= '{end_datetime_iso}'"

        # Construir parte de la consulta para agrupar los datos si se especifica
        query_group_by = (
            f"GROUP BY time({group_by})" if isinstance(group_by, str) else ""
        )

        # Construir parte de la consulta para seleccionar las variables
        if variables:
            if group_by:
                query_params = ", ".join(
                    [f'MEAN("{col}") AS "{col}"' for col in variables]
                )
            else:
                query_params = ", ".join([f'"{item}"' for item in variables])
        else:
            query_params = "*"

        # Construir la consulta completa
        query = f"SELECT {query_params} FROM {measurement} {query_datetime} {query_group_by}".strip().replace(
            "  ", " "
        )

        return query

    def get_data(
        self,
        database: str,
        query: str,
        format_data: Literal["DATAFRAME", "LIST"] = "DATAFRAME",
    ) -> Union[pd.DataFrame, List[dict]]:
        """
        Obtiene datos de una base de datos según la consulta proporcionada.

        :param database: La base de datos de la cual se obtendrán los datos.
        :type database: str
        :param query: La consulta a ejecutar en la base de datos.
        :type query: str
        :param format_data: El formato en el que se desea retornar los datos. Puede ser "DATAFRAME" o "LIST". Por defecto es "DATAFRAME".
        :type format_data: Literal["DATAFRAME", "LIST"]
        :return: Los datos recuperados de la base de datos.
        :rtype: Union[DataFrame, List[dict]]
        """
        # Realizar consulta
        data_raw = self.client.query(query=query, database=database)
        # Obtener los datos de interés del diccionario
        data = list(data_raw.get_points())

        if format_data == "DATAFRAME":
            # Si el formato deseado es un DataFrame, convertir los datos en un DataFrame de pandas
            data = pd.DataFrame(data=data)
            data.set_index(pd.to_datetime(data["time"]), inplace=True)
            data.drop(columns="time", inplace=True, axis=1)

        return data

    def write_data(
        self,
        database: str,
        measurement: str,
        data: Union[dict, pd.DataFrame],
        timezone: str = "UTC",
        clean_nan_dataframe: bool = False,
        create_database: bool = True,
    ) -> None:
        """
        Escribe datos en una base de datos InfluxDB.

        :param database: Nombre de la base de datos en la que se escribirán los datos.
        :type database: str
        :param measurement: Nombre de la medida en la que se registrarán los datos.
        :type measurement: str
        :param data: Los datos que se van a escribir en la base de datos. Puede ser un diccionario o un DataFrame de pandas.
        :type data: Union[dict, pd.DataFrame]
        :param timezone: Zona horaria para indexar los datos, por defecto "UTC".
        :type timezone: str, optional
        :param clean_nan_dataframe: Indica si se deben eliminar las filas con valores NaN del DataFrame, por defecto False.
        :type clean_nan_dataframe: bool, optional
        :param create_database: Indica si se debe crear la base de datos si no existe, por defecto True.
        :type create_database: bool, optional
        :raises NullsDataFrameError: Si se encuentran valores nulos en el DataFrame y no se permite limpiarlos.
        :raises FormatPointListError: Si ocurre un error al formatear la lista de puntos.
        :raises EmptyPointlist: Si ocurre un error por intentar escribir datos a partir de un elemento vacío.
        :raises CustomError: Si ocurre otro tipo de error no contemplado.

        :example:

        Suponiendo que 'client' es una instancia de InfluxDBWriter y 'data' es un DataFrame de ejemplo:

        >>> client = InfluxDBWriter()
        >>> data = pd.DataFrame({"A": [1, 2, None, 4], "B": [None, 5, 6, 7], "C": [8, 9, 10, 11]})
        >>> client.write_data(database="my_database", measurement="my_measurement", data=data)
        """
        if isinstance(data, pd.DataFrame):
            # Comprobar si hay valores nulos y limpiar el DataFrame si es necesario
            data_with_nulls = data.isnull().any().any()
            if data_with_nulls:
                if not clean_nan_dataframe:
                    # Si hay valores nulos y no se permite limpiarlos, se lanza un error
                    mask_data_null = data.isnull().any(axis=1)
                    data_null = (
                        data[mask_data_null]
                        .head(10)
                        .to_string(index=False, na_rep="NaN")
                    )
                    error_msg = f"Hay valores nulos en los datos proporcionados (muestra de 10):\n{data_null}"
                    raise exc.NullsDataframe(error_msg)
                else:
                    # Si hay valores nulos y se permite limpiarlos, se limpia el DataFrame
                    data.dropna(inplace=True)
                    logging.info("Valores nulos eliminados correctamente")

            # Convertir cada fila del DataFrame en un punto
            point_list = []
            for index, row in data.iterrows():
                # Reemplazar NaN con None en la fila
                cleaned_row = row.replace({np.nan: None}).to_dict()
                # Comprobar si el índice tiene información de zona horaria y formatearlo adecuadamente
                time = (
                    index.tz_localize(timezone).isoformat()
                    if index.tzinfo is None
                    else index
                )
                # Generar punto individual
                point = {
                    "time": time,
                    "measurement": measurement,
                    "fields": cleaned_row,
                }
                # Añadir el punto a la lista de puntos
                point_list.append(point)
        else:
            # Asignar el diccionario de puntos a la variable point_list
            point_list = data

        # Comprobar si la lista de puntos está vacía
        if len(point_list) == 0:
            error_msg = "La lista de puntos se encuentra vacía."
            raise exc.EmptyPointlist(error_msg)

        # Crear la base de datos si es necesario
        if create_database:
            self.client.create_database(dbname=database)
            logging.info(f"Base de datos '{database}' creada/actualizada.")

        # Registrar datos en la base de datos
        try:
            self.client.write_points(
                points=point_list, database=database, batch_size=10000
            )
        except InfluxDBClientError as e:
            # Capturar errores del cliente InfluxDB y lanzar una excepción personalizada
            error_msg = f"Error del cliente InfluxDB no capturado: {e}"
            raise exc.CustomError(error_msg) from e
        except Exception as e:
            # Capturar otros errores de escritura y lanzar una excepción personalizada
            error_msg = f"Error de escritura general no capturado: {e}"
            raise exc.CustomError(error_msg) from e


# Ejemplo de uso
if __name__ == "__main__":
    delphos = ITCInfluxDB(host="10.142.150.64")

    delphos.build_query(
        "measurement", variables=["esta es mi variableee", "esta es mi otra variablee"]
    )

    # query = delphos.build_query(
    #     measurement="MonitoringLocalSide",
    #     variables=["consumo_casa"],
    #     start_datetime="15/12/2023",
    #     end_datetime="15/12/2023 01:00:00",
    # )

    # # data = delphos.get_data(database="DaniRPI_MGBlue", query=query)
    # test = pd.DataFrame(
    #     {"A": [1, 2, None, 4], "B": [None, 5, 6, 7], "C": [8, 9, 10, 11]}
    # )

    # delphos.write_data("Datos_AEMET", "test_class", [])

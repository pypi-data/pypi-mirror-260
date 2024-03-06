import json
import time
import inspect
try:
    import pyodbc
    _pyodbc_available = True
except ImportError:
    _pyodbc_available = False

from seCore import ODBCError
from seCore.CustomLogging import logger
from seCore.Exceptions import ODBCLoginFailed, ODBCInvalidOperation, ODBCDriverError
from seCore.Utilities import mask


def odbcLoaded(idx: int = -1) -> bool:
    """
    Checks if the ODBC driver is loaded

    :return: bool
    """
    try:
        if not _pyodbc_available:
            return False

        return True if type([item for item in pyodbc.drivers()][idx]) is str else False
    except IndexError:
        return False


def odbcDriver(idx: int = -1) -> str:
    """
    Returns the ODBC driver
    :return: str
    """
    try:
        return [item for item in pyodbc.drivers()][idx] if odbcLoaded() else "Error finding ODBC driver"
    except IndexError:
        return "Error finding ODBC driver"


class odbcEngine:

    def __init__(self, server: str, port: int, user: str, password: str, trust: str, db: str = ""):
        """
        Initialize the odbcEngine object
        """
        self.__connStr = {
            "driver": odbcDriver(),
            "server": server,
            "port": port,
            "database": db,
            "user": user,
            "password": password,
            "trust": trust
        }
        self.isConnected = False
        self.__cnxn = None

    def connect(self):
        """
        Connect to database using pyodbc and ODBC Driver 17 or 18 for SQL Server
        """
        start_time = time.time()

        match self.__connStr["trust"]:
            case "yes":
                connStr = f'DRIVER={{{self.__connStr["driver"]}}}; ' \
                          f'Server={self.__connStr["server"]},{self.__connStr["port"]}; ' \
                          f'DATABASE={self.__connStr["database"]}; ' \
                          f'UID={self.__connStr["user"]}; ' \
                          f'PWD={self.__connStr["password"]}; ' \
                          f'Trusted_Connection={self.__connStr["trust"]};'
            case _:
                connStr = f'DRIVER={{{self.__connStr["driver"]}}}; ' \
                          f'Server={self.__connStr["server"]},{self.__connStr["port"]}; ' \
                          f'DATABASE={self.__connStr["database"]}; ' \
                          f'UID={self.__connStr["user"]}; ' \
                          f'PWD={self.__connStr["password"]};'

        oJson = {
            f'odbc-{inspect.currentframe().f_code.co_name}': {
                'connection_ms': float(f'{0 * 1000:.2f}'),
                'connected': self.isConnected,
                'connStr': self.__connStr
            }}
        try:
            with pyodbc.connect(connStr, timeout=1) as cnxn:
                self.__cnxn = cnxn
                self.isConnected = True
                oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['connected'] = self.isConnected

        except pyodbc.Error as ex:
            oJson = {
                f'odbc-{inspect.currentframe().f_code.co_name}': {
                    'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                    'connected': self.isConnected,
                    'error': {}
                }
            }
            match f'{ODBCError.DefaultExceptionId(ex.args[1])}':
                case "18456":
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['code'] = f'{ODBCError.DefaultExceptionId(ex.args[1])}'
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "ODBCLoginFailed"
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = f'{ODBCError.DefaultException(ex.args[1])}'
                    raise ODBCLoginFailed(json.dumps(oJson))
                case "851968" | "1048576":
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['code'] = f'{ODBCError.DefaultExceptionId(ex.args[1])}'
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "ODBCInvalidOperation"
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = f'{ODBCError.DefaultException(ex.args[1])}'
                    raise ODBCInvalidOperation(json.dumps(oJson))
                case _:
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['code'] = f'{ODBCError.DefaultExceptionId(ex.args[1])}'
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "ODBCDriverError"
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = f'{ODBCError.DefaultException(ex.args[1])}'
                    raise ODBCDriverError(json.dumps(oJson))

        oJson = {
            f'odbc-{inspect.currentframe().f_code.co_name}': {
                'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                'connected': self.isConnected,
                'connStr': self.__connStr
            }}
        oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['connStr']['password'] = mask(oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['connStr']['password'])

        logger.info(json.dumps(oJson))

        return self.isConnected

    def query(self, query: str):
        if self.isConnected:
            start_time = time.time()
            try:
                with self.__cnxn.cursor() as cur:
                    cur.execute(query)
                    r = [dict((cur.description[i][0], value)
                              for i, value in enumerate(row)) for row in cur.fetchall()]

                    logger.info(json.dumps({
                        f'odbc-{inspect.currentframe().f_code.co_name}': {
                            'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                            'query': f'{query}'
                        }}))
                    return r
            except pyodbc.Error as e:
                logger.error(json.dumps({
                    f'odbc-{inspect.currentframe().f_code.co_name}': {
                        'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                        'query': f'{query}',
                        'error': f'{e}'
                    }}))

                return []

    @property
    def connectionString(self):
        return self.__connStr

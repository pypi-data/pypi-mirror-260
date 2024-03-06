from seCore.JDBC import jdbcLoaded, jdbcDriver, jdbcEngine
from seCore.ODBC import odbcLoaded, odbcDriver, odbcEngine
from seCore.CustomLogging import logger


class sql:
    def __init__(self, server: str, port: int, user: str, password: str, trust: str, db: str = "", trustServerCertificate: bool = True, driverOverride: str = "jdbc", enableLogging: bool = True):
        self.__isConnected = False
        self.__odbcLoaded = odbcLoaded()
        self.__odbcDriver = odbcDriver()
        self.__jdbcLoaded = jdbcLoaded()
        self.__jdbcDriver = jdbcDriver()
        self.__driverOverride = driverOverride.lower() if driverOverride.lower() in ["odbc", "jdbc"] else "odbc"
        self.__driver = self.__odbcDriver if self.__driverOverride == "odbc" else self.__jdbcDriver

        self.__connStr = {
            "driver": self.__driver,
            "server": server,
            "port": port,
            "database": db,
            "user": user,
            "password": password,
            "trust": trust,
            "trustServerCertificate": trustServerCertificate
        }

        if enableLogging:
            logger.info(f'ODBC Driver Loaded..: {"Yes" if self.__odbcLoaded else "No"}')
            logger.info(f'ODBC Driver.........: {self.__odbcDriver}')
            logger.info(f'JDBC Driver Loaded..: {"Yes" if self.__jdbcLoaded else "No"}')
            logger.info(f'JDBC Driver.........: {self.__jdbcDriver}')
            logger.info(f'{"":-<75}')
            logger.info(f'driverOverride......: {self.__driverOverride}')
            logger.info(f'driver..............: {self.__driver}')

        match self.__driverOverride:
            case "odbc":
                self.__cnxn = odbcEngine(
                    server=self.__connStr['server'],
                    port=self.__connStr['port'],
                    db=self.__connStr['database'],
                    user=self.__connStr['user'],
                    password=self.__connStr['password'],
                    trust=self.__connStr['trust']
                )

                try:
                    self.__cnxn.connect()
                    self.__isConnected = self.__cnxn.isConnected
                except Exception as e:
                    logger.error(e)

            case _:
                self.__cnxn = jdbcEngine(
                    server=self.__connStr['server'],
                    port=self.__connStr['port'],
                    user=self.__connStr['user'],
                    password=self.__connStr['password'],
                    trustServerCertificate=self.__connStr['trustServerCertificate']
                )

                try:
                    self.__cnxn.connect()
                    self.__isConnected = self.__cnxn.isConnected

                except Exception as e:
                    logger.error(e)

    def query(self, query: str):
        return self.__cnxn.query(query)

    @property
    def isConnected(self) -> bool:
        return self.__isConnected


if __name__ == "__main__":
    oSql = sql(
        server='SQL5101.site4now.net',
        port=1433,
        db='db_a82904_cybernetic',
        user='db_a82904_cybernetic_admin',
        password='tb7qiwqer8mee68',
        trust='no',
        driverOverride='jdbc'
    )

    if oSql.isConnected:
        oSql.query("SELECT @@version as version")
        # oResults = oSql.query("SELECT TOP 1 * FROM [db_a82904_cybernetic].[dbo].[LP_Audit]")
        # logger.info(f'{len(oResults[0]["lpJson"])}')




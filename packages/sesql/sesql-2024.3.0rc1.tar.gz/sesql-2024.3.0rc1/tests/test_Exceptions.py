from seCore.Exceptions import ODBCLoginFailed, JDBCSecureConnection, JDBCLoginFailed, JDBCConnectionTimeOut, JDBCConnectionReset, JDBCSQLServerDriver


def test_odbclogin_failed():
    try:
        raise ODBCLoginFailed('ODBCLoginFailed')
    except ODBCLoginFailed as e:
        print(e)
        assert e.message == 'ODBCLoginFailed'


def test_jdbcsecure_connection():
    try:
        raise JDBCSecureConnection('JDBCSecureConnection')
    except JDBCSecureConnection as e:
        print(e)
        assert e.message == 'JDBCSecureConnection'


def test_jdbclogin_failed():
    try:
        raise JDBCLoginFailed('JDBCLoginFailed')
    except JDBCLoginFailed as e:
        print(e)
        assert e.message == 'JDBCLoginFailed'


def test_jdbcconnection_time_out():
    try:
        raise JDBCConnectionTimeOut('JDBCConnectionTimeOut')
    except JDBCConnectionTimeOut as e:
        print(e)
        assert e.message == 'JDBCConnectionTimeOut'


def test_jdbcsqlserver_driver():
    try:
        raise JDBCSQLServerDriver('JDBCSQLServerDriver')
    except JDBCSQLServerDriver as e:
        print(e)
        assert e.message == 'JDBCSQLServerDriver'

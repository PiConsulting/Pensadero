import os
import urllib


PROD = os.environ.get('PROD', False)
API_PORT = os.environ.get('PORT', 8080)

DB_SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DATABASE = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': DB_SERVER,
    'database': DATABASE,
    'username': DB_USERNAME,
    'password': DB_PASSWORD,
}

params = urllib.parse.quote_plus(f'DRIVER={DATABASE["driver"]};' +
                                 f'SERVER={DATABASE["server"]};' +
                                 f'DATABASE={DATABASE["database"]};' +
                                 f'UID={DATABASE["username"]};' +
                                 f'PWD={DATABASE["password"]}')

SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params

######
#
# CONFIG VARIABLES HERE
#
######

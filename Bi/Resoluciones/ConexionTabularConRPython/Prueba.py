#Importación de librerias
from sys import path
path.append('\\Program Files\\Microsoft.NET\\ADOMD.NET\\150')
from pyadomd import Pyadomd

#Declaro cadena de conexión
cnnstr = "DataSource = (local); provider=MSOLAP ; initial catalog =PruebaRPython"
query = """Evaluate DimCustomer"""

#Muestro Datos
with Pyadomd(cnnstr) as conn:
    with conn.cursor().execute(query) as cursor:
        print(cursor.fetchall())
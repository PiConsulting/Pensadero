
# A continuación se describen los niveles estándar y su aplicabilidad 
# (en orden creciente de gravedad):
#
#Nivel    valor numerico   Cuando es usado
#DEBUG         10          Información detallada, típicamente de interés sólo durante el diagnóstico de problemas.
#INFO          20          Confirmación de que las cosas están funcionando como se esperaba.
#WARNING       30          Un indicio de que algo inesperado sucedió, o indicativo de algún problema en el futuro 
#                          cercano (por ejemplo, «espacio de disco bajo»). El software sigue funcionando como se esperaba.
#ERROR         40          Debido a un problema más grave, el software no ha sido capaz de realizar alguna función.
#CRITICAL      50          Un grave error, que indica que el programa en sí mismo puede ser incapaz de seguir funcionando.

import logging

# La llamada a basicConfig() debería venir antes de cualquier llamada a debug(), info() etc. 
# 1- Cambiar el nivel para mostrar mensajes en consola
#logging.basicConfig(level=logging.DEBUG)    

# 2- Cambiar el formato en el que se muestran los mensajes
#logging.basicConfig(format='%(asctime)s %(message)s')

# 3- Guardar un archivo
#logging.basicConfig(filename='./example.log', filemode='w', level=logging.DEBUG)


# El mensaje INFO y DEBUG no aparecen porque el nivel por defecto es WARNING
logging.debug("A Debug Logging Message")  
logging.info("A Info Logging Message")    # will not print anything
logging.warning("A Warning Logging Message") # will print a message to the console
logging.error("An Error Logging Message")
logging.critical("A Critical Logging Message")

# Trabajar con variables
a = ':O'
logging.warning('A Warning Logging Message %s',a)  # will print a message to the console

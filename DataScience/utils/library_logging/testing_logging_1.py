#La biblioteca de logging adopta un enfoque modular y ofrece varias categorías de componentes:
# registradores, gestores, filtros y formateadores.
# Los registradores exponen la interfaz que el código de la aplicación utiliza directamente.
# Los gestores envían los registros de log (creados por los registradores) al destino apropiado.
# Los filtros proporcionan una instalación de grano más fino para determinar qué registros
# de log se deben producir.
# Los formatos especifican la disposición de los archivos de log en el resultado final.

import logging
import numpy as np
import time

# Crear logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.INFO)

# Crear console handler y setear como level "INFO"
ch_1 = logging.StreamHandler()
ch_1.setLevel(logging.INFO)
# Crear file handler y setear como level "WARNING"
ch_2 = logging.FileHandler('./warning.log', mode='w')
ch_2.setLevel(logging.WARNING)

# Crear formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
ch_1.setFormatter(formatter)
ch_2.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch_1)
logger.addHandler(ch_2)

# 'application' code

logger.info('Start process')

for i in np.arange(0,10,1):
    logger.info('Processing %s', str(i))
    if i % 2 == 0:
        logger.warning('Warning, the value %s is even', str(i))
    time.sleep(1)

logger.info('Finish process')
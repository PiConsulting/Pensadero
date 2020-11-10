# Batch inference models

Vamos a describir como poder poner un modelo en produccion que podamos ejecutar en lotes.

### Save model
Una vez que tenemos nuestro modelo entrenado y listo para usar en produccion, lo guardamos en un archivo binario
``` python
from sklearn.ensemble import RandomForestClassifier


# create and fit model
model = RandomForestClassifier(max_depth=2, random_state=0)
model.fit(X, y)

# save model as binary object
with open('rf.pk', 'wb') as fp:
    import pickle
    pickle.dump(model, fp)
```

### Create script to run inference
Con el modelo guardado creamos un script para realizar una inferencia sobre nuevos datos.

La forma de pasar informacion al script puede realizarce de muchas maneras, en este ejemplo usaremos 
el modulo [argparse](https://docs.python.org/3/library/argparse.html) que viene instalado con python

Otras formas de realizar esto podrian ser:
  * Variables de entorno
  * Archivo de configuracion
  * Funcion `input()`
  * Modulo sys


``` python
import os
import argparse
import pandas as pd


def pre_processing(X, y=None, **kwargs):
    """ This function should pre-process all data and return it ready for the model """
    import numpy as np
    X = np.sqrt(X)
    return X


# Esta linea permite ejecutar el codigo del if como un script
# o permite importar las funciones en el archivo desde otro
if __name__ == '__main__':

    # create args to recibe info need
    ap = argparse.ArgumentParser(description='Script to run model')

    ap.add_argument("model_path", type=str, help="absolute path to trained model")
    ap.add_argument("input_path", type=str, help="absolute path to csv for inference")
    ap.add_argument("output_path", type=str, help="absolute path to csv for results")
    ap.add_argument("-p", "--pre-processing", type=bool, default=False, help="Make pre-processing over input data")
    args = vars(ap.parse_args())

    # read data from file
    df = pd.read_csv(args['input_path'])

    if args['pre-processing']:
        X = pre_precessing(df)
   
    # load model
    with open('rf.pk', 'rb') as fp:
        import pickle
        model = pickle.load(fp)

    # make prediction
    y_pred = model.predict_proba(df.values)
    
    # save results 
    pd.Series(y_pred, name='y').to_csv(args['output_path'], index_label='id')
```


### Execute script
Con el script creado solo resta ejecutarlo. Para esto debemos tener en cuenta que el ambiente
donde nuestro script corra debe tener instaladas las librerias requeridas.

##### Veamos algunos caminos comunes de realizar esto:
  * **Ejecucion a mano**:
    Debemos tener entorno-virtual (virtualenv, anaconda, pyenv) con las libs instaladas
    Con el entorno activado y parados en la carpeta donde esta el script, ejecutamos en una consola:  
    `python script.py '~/rf.pk' '~/data.csv' '~/out.csv'`  

  * **Command line script**:  
    Podemos crear un script bash (o bat para windows), que nos permite en un solo comando 
    activar el entorno, ejecutar el script y desactivar el entorno. 
    ``` bash
    # run.sh
    . venv/bin/activate
    # las variables $1 $2... toman los args recibidos en el script
    python script.py $1 $2 $3
    deactivate
    ```
    Y luego ejecutarlo desde una consola:
    `./run.sh '~/rf.pk' '~/data.csv' '~/out.csv'`
   
  * **Docker**:
    Podemos generar una imagen docker con las libs requeridas y luego ejecutar el container
    
    Primero debemos armar un [Dockerfile](https://docs.docker.com/get-started/part2/)
    ``` dockerfile
    FROM python:3.8-alpine
    WORKDIR /app
    
    COPY requirements.txt ./
    RUN pip install --upgrade pip && pip install -r requirements.txt
    
    COPY script.py .
    
    ENTRYPOINT ["python", "./script.py"]
    ```
    Luego debemos armar (compliar) la imagen docker  
     `docker build -t batch_model .`  
     y ejecutarla  
    `docker run -v ~:/app batch_model '~/rf.pk' '~/data.csv' '~/out.csv'`  
    
    Nota:
      * Usamos la version [Alpine](https://hub.docker.com/_/alpine) de docker ya que solo ocupa 80MB
      * El arg `-v` en [docker run](https://docs.docker.com/engine/reference/run/) nos permite montar carpetas dentro del docker, sino los datos no estaran disponibles
      * El archivo **requirements.txt** debe tener en formato pip todas las lib utilizadas (podemos cambiar esto a la version de conda)


# Delta Tables - Importar Delta Tables de Databricks en Power BI  - Parte 1 

Hace tiempo se viene utilizando el delta lake como formato de almacenamiento y capa de gestión de transacciones reemplazando al antiguo Apache parquet, si bien tienen similitudes, no son lo mismo.

En este post veremos como cargar un archivo .CSV desde un Azure datalake Gen 2, transformarlo en databricks y guardarlo en una tabla delta, finalmente, lo tomaremos en Power BI desde el server de Databricks y en otro post, veremos como tomarlo desde el mismo datalake.

Consideraciones:<br />
-Contar con un workspace de Databricks. <br/>
-Contar con un blob storage.<br/>
-Contar con un punto de montaje realizado en Databricks. <br/>
-Contar con recursos de Databricks  y Data lake Gen 2 creados en Azure.<br/>
-Contar con un cluster o unidad de computación configurada en Databricks.
<br /> 


<br />
-Comenzamos: <br />
<br />
Nos dirigimos al portal Azure y hacemos el login en https://portal.azure


![Foto modelo](captura8.png)


Buscamos nuestro Storage account, en nuestro caso "mvpdemos"

![Foto modelo](captura9.png)


Nos dirigimos a Containers, una vez dentro, buscaremos landing que contiene nuestro archivo (Este mismo proceso se puede hacer desde la herramienta Azure Storage Explorer)

![Foto modelo](captura11.png)

Una vez dentro de landing, podemos ver nuestro archivo "Movies_data.csv"

![Foto modelo](captura10.png)

Una vez verificado nuestro archivo, iremos a nuestro recurso Azure databricks que lo lanzaremos desde el portal Azure.


![Foto modelo](captura12.png)

Una vez dentro de Databricks, crearemos un notebook que tomará  el archivo csv alojado en el datalake y comenzaremos a transformarlo con PySpark.

![Foto modelo](captura13.png)

Importamos todas las funciones necesarias, declaramos el path de source, el path de destination y leemos el archivo csv, finalmente hacemos un display() para mostrarlo.

<pre><code>
import pyspark
from pyspark.sql.functions import *
from pyspark.sql.functions import col
from pyspark.sql.types import *
import re
from pyspark.sql.functions import monotonically_increasing_id
import pyspark.sql.functions as F  
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType

#Declaración del path del datalake en una variable 

FullSource = '/mnt/landing/Pruebas/movies_data.csv'
FullDestination = '/mnt/landing/Pruebas/DeltaTables/Movies'
#Lectura del path con PySpark

DF_Movies = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferSchema", "true") \
                .option("delimiter", ",") \
                .load(FullSource)

display(DF_Movies)

</code></pre>


![Foto modelo](captura14.png)

Resultado del display().

![Foto modelo](captura15.png)

Luego, continuamos tomando solo las columnas que necesitamos.

![Foto modelo](captura16.png)

Aparecen caracteres especiales en la columna Director, por lo que, utilizamos la función regexp para reemplazar estos caracteres.


![Foto modelo](captura17.png)

Luego, borramos los espacios en blanco de las columnas.


![Foto modelo](captura18.png)

Definimos el diccionario de datos de las columnas con el nombre final y mostramos el dataframe.

![Foto modelo](captura19.png)

Vemos el resultado del dataframe.

![Foto modelo](captura20.png)

Verificamos el schema con sus columnas y tipos de datos.

![Foto modelo](captura21.png)

Ahora, de los pasos mas importantes, creamos el esquema dentro del Catálogo de Databricks que va a direccionar la ruta del lake.

![Foto modelo](captura22.png)

Finalmente, guardamos nuestro dataframe en una tabla delta.

![Foto modelo](captura23.png)

Ahora vamos al catálogo y verificamos que nuestra tabla existe.

![Foto modelo](captura24.png)

Podemos ver en los detalles de la tabla que nuestra tabla delta está almacenada en el datalake en la ruta que especificamos.

![Foto modelo](captura25.png)


# Cómo importamos estos datos en Power BI?

Abrimos Power BI Desktop --> iremos a Get Data y seleccionamos el origen "Azure Databricks" 

Aquí, debemos ingresar el Server Hostname y el HTTP Path que lo obtenemos en el cluster de Databricks.

![Foto modelo](captura5.png)

Aquí buscamos nuestra tabla delta.

![Foto modelo](captura6.png)

Vemos que tiene sus datos correctos y realizamos la importación a Power BI.

![Foto modelo](captura7.png)

Finalmente, vemos nuestra tabla delta en una tabla de Power BI.

![Foto modelo](captura26.png)

# Síntesis

En resumen, lo que hicimos fue, cargar un archivo en el blob storage landing, este archivo csv lo leímos en databricks (cabe destacar que ya teníamos el lake montado) y comenzamos a transformarlo como un dataframe, y luego lo guardamos en una tabla delta que redirecciona al datalake, esto en cuanto a transformación.<br/><br/>
Finalmente, para cargarlo en Power BI, utilizamos el server y el http name de Databricks para poder tomar nuestra tabla delta.

Por qué no lo hicimos desde el mismo datalake si lo guardamos ahí?
Es correcto, este caso apunta a traer la data almacenada en el datalake y consumirla desde databricks solamente, en el próximo post veremos como tomarlo desde el mismo datalake.

Podríamos automatizar este proceso si tengo que hacer varias cargas?
Claro! Utilizando Data Factory podemos crear pipelines que realicen este mismo proceso para una secuencia de archivos determinada o indeterminada.

Diferencia de Delta con Parquet?
Parquet es un formato de archivo de almacenamiento sin capacidades de transacción o control de versiones. <br/>Delta es una capa de almacenamiento que extiende Parquet con funcionalidades como las ACID transactions, control de versiones y el almacenamiento de grandes volumenes de data.


</br>

# Bibliografía

https://app.powerbi.com/

https://www.databricks.com

https://portal.azure

https://blog.fabric.microsoft.com/es-AR/blog/

https://learn.microsoft.com/en-us/azure/databricks/partners/bi/power-bi

https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction

---

By **Facundo Montenegro**

# DataEngineering
Repository of code snippets for usual data engineering stuff.
---
**Limpieza de datos en SELECT (Oracle)**
```
- Uso: Limpieza de datos en el select de un query, ideal para cuando el output es un CSV y algunos caracteres pueden interferir en la posterior lectura del CSV.
- Palabras clave: query, oracle, datafactory, csv
- Lenguaje: PL/SQL (Oracle SQL), Python
 - Autor: Julian Biltes 
```
``` sql
SELECT REPLACE(REPLACE(REPLACE(REPLACE(table.columnName,',',''),'"',''),CHR(13),''),CHR(10),'')
FROM tableName table
WHERE rownum <= 10 

--NOTAS:
--REPLACE: funcion que reemplaza un valor por otro, en este caso la coma, comillas dobles, CHR(13) y CHR(10) por nada ('')
--CHR(10) y CHR(13): saltos de linea
-- rownum <= 10: retorna hasta 10 registros
--Consideraciones: No aplicar para campos datetime, int ni float debido a que convierte a varchar y luego aplica las funciones, en esta conversión puede alterar el formato o generar resultados no deseados.

``` 
```
- Script en python para generar las queries
```
``` python
fields = ['columnName1', 'columnName2','columnName3']
excludeField = ['columnName2']
flags = []

for pos in range(0, len(fields)):
    if fields[pos] in excludeField:
        flags.append(True)
    else:
        flags.append(False)
        
query = 'select '
for pos in range(0, len(fields)):
    if not flags[pos]:
        query += "replace(replace(replace(replace(" + fields[pos] + ",'|',''),'¬',''),chr(13),''),chr(10),'') " + fields[pos] + ", "
    else:
        query += fields[pos] + ", "
        
query = query[:-1] + " from dbo.tableName  where rownum <= 10 "  

print(query)

""" Print

SELECT REPLACE(REPLACE(REPLACE(REPLACE(columnName1,',',''),'"',''),CHR(13),''),CHR(10),''),
columnName2,
REPLACE(REPLACE(REPLACE(REPLACE(columnName3,',',''),'"',''),CHR(13),''),CHR(10),'')
FROM dbo.tableName table
WHERE rownum <= 10 
"""

```
---

-----------------
**Comandos útiles databricks**

	- Uso: comandos varios utilizados para tareas de ETL

	- Palabras clave: Data Bricks, Python, Pyspark.

	- Lenguaje: Python.
	
	- Autor: Efrain Diaz.
```	
Comandos útiles

####Ver listado de archivos de un directorio del datalake
%fs ls "dbfs:/mnt/raw-data/.../..."

#### Crear una vista para luego manejarla con el comando %sql y querys de DDBB
df.createOrReplaceTempView("df_view")

%sql
select  count(1) from df_view
 
#### Crear un dataframe apartir de una vista
df_subset = spark.sql("SELECT * from df_view ORDER BY ID")

#### Borrar una columna de un dataframe
df = df.drop("<column>")

#### Ver esquema de un dataframe
df.printSchema()
df.dtypes()

#### Unir datasets
df_3 = df_1.union(df_2)

#### Castear campos de un dataset
from pyspark.sql.types import *
df = df.withColumn("<field>", df["<field>"].cast(TimestampType()))
df = df.withColumn("<field>", df["<field>"].cast(IntegerType()))
df = df.withColumn("<field>", df["<field>"].cast(DoubleType()))

#### Transformar todas las columnas decimal a tipo int (para evitar ID =  1.00000, 2.00000,...)
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType
decimalCols = [item[0] for item in df.dtypes if item[1].startswith('decimal')]
for i in decimalCols:
df = df.withColumn(i, df[i].cast(IntegerType()))

#### Réplica de CASE-WHEN
df = df.withColumn("new_column",when(df.column_A.isNull(),df.column_B).otherwise(df.column_A))

#### Réplica de WHERE
df = df.where(condition) ## condition = df.field_A >  100 for example

#### Réplica de REPLACE's (comillas dobles, punto y coma, salto de line y carrie)
from pyspark.sql.functions import *
stringcols = [item[0] for item in df.dtypes if item[1].startswith('string')] ## obtengo todos los campos tipo nvarchar
for i in stringcols:
#The function withColumn is called to add (or replace, if the name exists) a column to the data frame.
#The function regexp_replace will generate a new column by replacing all substrings that match the pattern.
df = df.withColumn(i, regexp_replace(regexp_replace(regexp_replace(i, '"', ''),';',''),'[\\r\\n]',''))
```

**Merge/Upsert databricks**

	- Uso: comandos varios utilizados para tareas de ETL

	- Palabras clave: Data Bricks, Python, Pyspark, Merge, Upsert.

	- Lenguaje: Python.
	
	- Autor: Efrain Diaz.
 
```
#Hacer un Merge/Upsert en Pyspark
# https://dwgeek.com/sql-merge-operation-using-pyspark-upsert-example.html/
# https://gustavosaidler.com/data%20analysis/pyspark-upsert/

## Importo librerías necesarias
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import row_number, desc

## Leo el nuevo parquet que surge del pipeline de datafactory de carga incremental
df_new_records = spark.read.parquet(path) 

## Leo la tabla dim o fact que quiero actualizar del adw (tener definida previamente las configuraciones de conexion)
df_historical = spark.read.format("com.databricks.spark.sqldw").option("url", jdbcUrl).option("tempDir", "wasbs://raw-data@datalakeanalitica.blob.core.windows.net/DIP/GDA/.../temp") \
  .option("forwardSparkAzureStorageCredentials", "true").option("user", username).option("password", password).option("dbTable", schema_table_final).load()

## Genero un nuevo dataframe con data de ambos df
df_upsert = df_historical.union(df_new_records)

## Si tengo que hacer una limpieza o casteo, la hago sobre df_upsert

## Genero una nueva columna con la MÁXIMA fecha de modificación ya que solo viene una sola columna con fecha (FECHA_INSERT o FECHA_UPDATE) y la otra con null, para manejarme con un unico campo
df_upsert = df_upsert.withColumn("last_modified_date", when(df_upsert.FECHA_INSERT.isNull(), df_upsert.FECHA_UPDATE).otherwise(df_upsert.FECHA_INSERT))

## Defino un arreglo de campo/s PK  ['id1','id2','id3']
primary_keys = ['id']

## Particiono el dataset por las PK y lo ordeno por el campo de fecha descendientemente
## Este paso, agrupará los ID duplicados, poniendo más arriba el registro más actual(el nuevo, a mantener)
w = Window.partitionBy(*primary_keys).orderBy(desc('last_modified_date'))

## Creo una columna temporaria en base a la agrupación anterior
df_upsert = df_upsert.withColumn("_row_number", row_number().over(w))

## Mantengo sólo los registros nuevos (id==1) y borro luego la columna temporal
df_upsert = df_upsert.where(df_upsert._row_number == 1).drop("_row_number")

## Acá tambien puedo verificar si el df_upsert necesita alguna limpieza o transformación más , como por ejemplo agregarle un timestamp, informacion de log, a que archivo del lake pertenece, etc

## Una vez listo el df, lo inserto en la tabla dim/fact con el modo OVERWRITE (por detrás lo que hace Spark es dropear la tabla y volverla a crear, llenándola con los registros de df_upsert)
df_upsert.write.mode("overwrite").format("com.databricks.spark.sqldw").option("url", jdbcUrl).option("forwardSparkAzureStorageCredentials", "true").option("tempDir", "wasbs://raw-data@datalakeanalitica.blob.core.windows.net/DIP/GDA/.../temp").option("user", username).option("password", password).option("dbTable", schema_table_final).option("maxStrLength", "3500").save()

```

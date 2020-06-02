# DataEngineering
Repository of code snippets for usual data engineering stuff.
-----------------
**Cargar datos en CosmoDB (Spark y Python)**

	- Uso: Cargar datos en un container de CosmoDB

	- Palabras clave: Databricks, CosmoDB, Spark, python, container, coleccion, item, SQL API

	- Lenguaje: Python, Spark.
	
	- Autor: Julian Biltes

PYTHON 
``` python
#pip install --pre azure-cosmos 
#(importante el --pre !!!)
from azure.cosmos import exceptions, CosmosClient, PartitionKey

# Initialize the Cosmos client
endpoint = "llenar" #desde el panel del recurso
key = 'llenar' #desde el panel del recurso, en keys

# <create_cosmos_client>
client = CosmosClient(endpoint, key)
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database_name = 'llenar'
database = client.create_database_if_not_exists(id=database_name)
# </create_database_if_not_exists>

# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = 'llenar'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/llenar"),
    offer_throughput=400
)
# </create_container_if_not_exists>

 # <create_item>
for jsonData in arrayJson:
    container.create_item(body=jsonData)
# </create_item>

```

SPARK 
``` python
import uuid
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

uuidUdf= udf(lambda : str(uuid.uuid4()),StringType())

pathJson = 'LLENAR"
df = spark.read.option("multiline", "true").json(pathJson)
df = AsApplied.withColumn("id",uuidUdf())
#display(AsApplied.select("id"))


# Write configuration
writeConfig = {
 "Endpoint" : "llenar",
 "Masterkey" : "llenar",
 "Database" : "llenar",
 "Collection" : "llenar,
 "Upsert" : "true"
}

# Write to Cosmos DB from the flights DataFrame
AsApplied.write.format("com.microsoft.azure.cosmosdb.spark").mode("append").options(**writeConfig).save()

```
**Volcar datos en ADL y ADW (Spark y Python)**

	- Uso: Escribir datos en un datalake o en un datawarehouse

	- Palabras clave: Databricks, Spark, python, escribir, overwrite, append, datalake, datawarehouse

	- Lenguaje: Python, Spark.
	
	- Autor: Efrain Diaz

PYTHON 
``` 
#Escribir en el storage: Datalake <-- Dataframe
(df
 .coalesce(1) ## Sirve para que solo cree una particion, investigar acerca de particiones de parquet's
 .write
 .parquet(path, mode="modo") ## path = "mnt/trusted-data/..."  modo = "overwrite" o "append", segun necesidad
)

#Escribir en el adw: Datawarehouse <-- Dataframe
## Default setting:
jdbcHostname = "serversqls21-analitica.database.windows.net"
jdbcDatabase = "warehouseanalitica"
jdbcUrl = "jdbc:sqlserver://{0};database={1}".format(jdbcHostname, jdbcDatabase)
spark.conf.set("fs.azure.account.key.datalakeanalitica.blob.core.windows.net","nZBTj4zDX2m6mAkV7Ya0ntk4H7DrnepqKEbKka11hljaepvX54dYNClnxwRjcR01CBzh4U4G2cXZwp5+ZI3vhA==")

## Custom setting:
username = 'analiticauser'
password = 'Pa$$w0rd1'
schema_table_final = 'esquema.tabla'

(df_hoy_subset.write
 .mode("overwrite") ## Overwrite sobreescribe, Append inserta al final de todo
 .format("com.databricks.spark.sqldw")
 .option("url", jdbcUrl)
 .option("forwardSparkAzureStorageCredentials", "true") ## Polybase
 .option("tempDir", "wasbs://raw-data@datalakeanalitica.blob.core.windows.net/DIP/GDA/.../temp")
 .option("user", username)
 .option("password", password)
 .option("dbTable", schema_table_final) ## ó .option("query", "select <fields> from <table> where <conditions>")
 .option("maxStrLength", "3500") ## para forzar el maximo length de los campos string
 .save()
)

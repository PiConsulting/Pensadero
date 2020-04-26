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


# DataEngineering

Configuraciones de cosas tediosas que podamos automatizar.


-----------------
**Ejecutar pipeline de Data Factory**

	- Uso: llama un pipeline de data factory con parametros, logueando como usuario o como service principal

	- Palabras clave: Data Factory, Azure, Pipeline, Parameters.

	- Lenguaje: Python.
	
	- Autor: Martin Zurita.
	
``` python
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.common.credentials import UserPassCredentials #To login with user and pass, use this.
from azure.common.credentials import ServicePrincipalCredentials #To login with service principal (appid and client secret) use this

subscription_id = "subsID"

#Use only one of these, depending on how you want to login.
credentials = UserPassCredentials(username="user@yourdomain.com", password="yourpass") #To login with user and pass
credentials = ServicePrincipalCredentials(client_id='appid', secret='client secret', tenant='tenantid') #To login with serv ppal

adf_client = DataFactoryManagementClient(credentials, subscription_id)


rg_name = "resource group name"
df_name = "data factory name"
p_name = "pipeline name"
params = {
    "Param1":"value1",
    "Param2":"value2"
}

adf_client.pipelines.create_run(rg_name, df_name, p_name, params)
```

---------------------

**Encriptar y desencriptar con Fernet en Python**

	- Uso: paso a paso que permite crear un archivo .bin que guardará datos de usuario y contraseña encriptados. Brinda una función para luego desencriptar dichos datos y devolverlos como String. Adaptable para encriptar y desencriptar más de dos datos.

	- Palabras clave: Encriptar, Encriptación, Fernet, Script.

	- Lenguaje: Python.

	- Autor: Iván Ingaramo.


``` python
from cryptography.fernet import Fernet

# Ejecutar Paso a Paso la primera vez. Seguir las instrucciones.

# Paso 1: Genero una Key

key = Fernet.generate_key()
print(key)

# Paso 2: Copiar del print(key) anterior la key y guardarla en una variable, sino el desencriptar no funcionará después

key = b'jbf43TF4f45%GFDE¨*[tr4--#dDE' # Key de ejemplo, debe mantener la b'' inicial ya que debe ser tipo bytes

# Paso 3: Este paso se ejecuta solo la primera vez. Encripto las credenciales y las guardo en el archivo .bin.
# Nótese el salto de linea \n entre el usuario y el pass. Esto es para más adelante leer por lineas el archivo.

ciphered_suite = Fernet(key)
ciphered_cred = ciphered_suite.encrypt(b'TU_USUARIO\nTU_PASSWORD')

with open(r'..\NOMBRE_DE_TU_ARCHIVO_A_ENCRIPTAR.bin', 'wb') as file_object:
    file_object.write(ciphered_cred)

# Paso 4: Borrar del script el Paso 1 y el Paso 3, sólo dejando de este último la linea ciphered_suite = Fernet(key), necesaria para desencriptar más adelante.

# Paso 5: Función para leer el archivo .bin y recuperar las credenciales encriptadas

def decrypt(nombreArchivoEncriptado):
    with open(r'..\\' + nombreArchivoEncriptado + '.bin', 'rb') as file_object:
	for line in file_object:
	    encryptedCred = line
	
	# Desencripto
	decryptedCred = (ciphered_suite.decrypt(encryptedCred))
	
	# Convierto a String
	decryptedCred = bytes(decryptedCred).decode("utf-8")
	
	# Recorro el string linea por linea y voy guardando el usuario y el password
	count = 0
	for line in decryptedCred.splitlines():
	    if count == 0:
	        user = line
	        count = count + 1
	    else:
	        pwd = line
	        
    return user, pwd

# Prueba

usuario, password = decrypt("NOMBRE_ARCHIVO_ENCRIPTADO")
```
---------------------

**Crear conexión a una BD SQL Server ocultando usuario y password**

```
- Uso: script que crea una conexión a una base de datos SQL Server sin mostrar las credenciales, usando la función decrypt() del script de Encriptación y Desencriptación con Cryptography Fernet.

- Palabras clave: conectar, conexión, sql, desencriptar, credenciales, password, ocultar.

- Lenguaje: Python.

- Autor: Iván Ingaramo.

```

``` python
# Se debe importar el script de Encriptar y Desencriptar con Fernet, el cual se encuentra en este mismo archivo Configuration.md
import decrypt as de
import pandas as pd
import sqlalchemy as sa
import urllib

# La función recibe el nombre de tu base de datos. Adaptar el nombre del driver de ser necesario.
def connect(nombreBD):
    user, pwd = de.decrypt(nombreBD)
    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                    r"SERVER=" + "tu_server" + ";"
                                    "DATABASE=" + nombreBD + ";"
                                    "UID=" + user + ";"
                                    "PWD=" + pwd)
    
    conn = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    return conn

```

---

**Login azure con service principal**

```
- Uso: script que permite loguear en azure con un Service Principal, despues de ejecutar estas lineas se pueden correr comandos de la libreria Az de PowerShell y estaran autenticados.

- Palabras clave: login, loguear, azure, powershell, service principal, Az.

- Lenguaje: PowerShell.

- Autor: Martin Zurita.

```

``` bash
$service_principal_key = "LLENAR"
$service_principal_appID = "LLENAR"
#Tenant id se consigue en azure yendo a Azure Active Directory, 
$tenant_ID = "LLENAR"

$secpasswd = ConvertTo-SecureString $service_principal_key -AsPlainText -Force

$creds = New-Object System.Management.Automation.PSCredential ($service_principal_appID, $secpasswd)

Login-AzAccount -Credential $creds -ServicePrincipal -TenantId $tenant_ID
```


---


**Enviar email con python**

```
- Uso: script que permite enviar un mail usando Sendgrid Mail (recurso de Azure).

- Palabras clave: email, mail, automatico, python, aviso, alertas.

- Lenguaje: Python.

- Autor: Julian Biltes

```

``` python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def img_pi():
    html = '<br><img src="data:image/png;base64,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"'
    return html

api_key_sendgrid = "llenar" #se obtiene del recurso SENDGRID
from_email = "llenar"
to_emails = ["llenar","llenar"]
subject = "llenar"
html_content = "llenar" #body email

message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content + img_pi()
        )   

#Send email
try:
	sg = SendGridAPIClient(api_key_sendgrid)
   	response = sg.send(message)
except Exception as e:
	print(e)

```
---


**Enviar email con powershell**

```
- Uso: script que permite enviar un mail usando el protocolo SMTP.

- Palabras clave: email, mail, automatico, powershell, SMTP, aviso, alertas.

- Lenguaje: PowerShell.

- Autor: Martin Zurita.

```

``` bash
$smtpServer = "smtp.sendgrid.net"
$smtpPort = '587'
$destinatarios = @("mzurita@piconsulting.com.ar", "ibarrau@piconsulting.com.ar")
$secpasswd = ConvertTo-SecureString "PasswordParaMail" -AsPlainText -Force
$mycreds = New-Object System.Management.Automation.PSCredential ("UsuarioParaMail", $secpasswd)

$mailParams = @{
    From = 'email@destinatario.com.ar'
    To = $destinatarios
    SmtpServer = $smtpServer
    Port = $smtpPort
    Credential = $mycreds
}

$mailContent = @{
            Subject = 'Algun subject para esto'
            Body = "Todo el body del mail" 
            }
			
Send-MailMessage @mailParams -UseSsl @mailContent


```

---
**Configurar conexión de Databricks con Azure Data Lake Gen 2**
```
- Uso: script que permite montar el Data lake gen 2. Se debe previamente crear un key vault scope en Databricks, el sp debe tener permisos de lectura sobre el Data Lake "Storage Blob Data Reader" 
- Palabras clave: keyvaul, Data Lake, Databricks, mount, montar.
- Lenguaje: Python 
 - Autor: Matías Deheza.
```
``` python
# Variable declarations. These will be accessible by any calling notebook.
keyVaultScope = "key-vault-secrets"
adlsGen2AccountName = dbutils.secrets.get(keyVaultScope, "ADLS-Gen2-Account-Name")
fileSystemName = "contosoauto"
abfsUri = "abfss://" + fileSystemName + "@" + adlsGen2AccountName + ".dfs.core.windows.net/"


# Add the required configuration settings for OAuth access to your ADLS Gen2 account.
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": dbutils.secrets.get(keyVaultScope, "ContosoAuto-SP-Client-ID"),
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(keyVaultScope, "ContosoAuto-SP-Client-Key"),
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/" + dbutils.secrets.get(keyVaultScope, "Azure-Tenant-ID") + "/oauth2/token"}


# Before you can access the hierarchical namespace in your ADLS Gen2 account, you must initialize a filesystem. To accomplish this, we will use the `fs.azure.createRemoteFileSystemDuringInitialization` configuration option to allow the filesystem to be created during our mount operation. We will set this value to `true` immediately before the accessing the ADLS Gen2 filesystem, and then back to `false` following the command.
spark.conf.set("fs.azure.createRemoteFileSystemDuringInitialization", "true")


# Mount the ADLS Gen2 filesystem.
dbutils.fs.mount(
  source = abfsUri,
  mount_point = "/mnt/" + fileSystemName,
  extra_configs = configs)


# Disable creation of the filesystem during initialization.
spark.conf.set("fs.azure.createRemoteFileSystemDuringInitialization", "false")

```
---
**Instalar chromium en Databricks para utilizar Selenium**
```
- Uso: script que instala el driver de chromium para luego poder ejecutar Selenium. Este codigo se ejecuta por unica vez en notebook de databricks y luego en el init script del cluster se debe indicar el nombre del script (chromedriver_linux64-install.sh) para que se ejecute cada vez que el cluster se encienda.
- Palabras clave: Selenium, Databricks, chromium, driver
- Lenguaje: Python 
 - Autor: Julian Biltes
```
``` python
script = """
  wget  https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip
  mkdir /tmp/chromedriver
  unzip /tmp/chromedriver_linux64.zip -d /tmp/chromedriver/
  sudo add-apt-repository ppa:canonical-chromium-builds/stage
  /usr/bin/yes | sudo apt update
  /usr/bin/yes | sudo apt install chromium-browser
"""

dbutils.fs.mkdirs("/databricks/webdriver")
dbutils.fs.put("/databricks/webdriver/chromedriver_linux64-install.sh", script, True)

```
---
**Instalar RStudio en Databricks**
```
- Uso: script que instala el RStudio en un cluster de Databricks. Este codigo se ejecuta por unica vez en notebook de databricks y luego en el init script del cluster se debe indicar el nombre del script (rstudio-install.sh) para que se ejecute cada vez que el cluster se encienda.
- Palabras clave: RStudio, Databricks, R
- Lenguaje: Python 
 - Autor: Julian Biltes (https://docs.databricks.com/spark/latest/sparkr/rstudio.html)
```
``` python
script = """#!/bin/bash

set -euxo pipefail

if [[ $DB_IS_DRIVER = "TRUE" ]]; then
  apt-get update
  apt-get install -y gdebi-core
  cd /tmp
  # You can find new releases at https://rstudio.com/products/rstudio/download-server/debian-ubuntu/.
  wget https://download2.rstudio.org/server/trusty/amd64/rstudio-server-1.2.5001-amd64.deb
  sudo gdebi -n rstudio-server-1.2.5001-amd64.deb
  rstudio-server restart || true
fi
"""

dbutils.fs.mkdirs("/databricks/rstudio")
dbutils.fs.put("/databricks/rstudio/rstudio-install.sh", script, True)
```
---
**Template para Azure Function (compatible con Datafactory)**
```
- Uso: Cuando se precisa crear una API de Azure Function llamable desde datafactory surgen algunos errores por el response, a continuacion se comparte un template 100% funcional. En este existe la function "write_http_response" que retorna un json con los valores necesarios para que datafactory lo procese sin errores.
- Palabras clave: Azure Function, API, Datafactory
- Lenguaje: Python 
 - Autor: Julian Biltes 
```
``` python
import logging
import os
import azure.functions as func
import json

#Function for construct response json, necessary if the API is called from Azure Data Factory
def write_http_response(status, body_dict):
    return_dict = {
        "status": status,
        "body": json.dumps(body_dict),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    return json.dumps(return_dict)

#Main API
def main(req: func.HttpRequest):
    logging.info('Python API function processed a request.')

    #Dict for build response
    res_body  = {}
    
    #Enviroment Variables
    EXAMPLE_VAR_ENVIROMENT = os.environ.get('EXAMPLE_ENVIROMENT')

    #get values with method GET
    called_from = req.params.get('called_from')
    example_param = req.params.get('example_param')

    #get values with method POST
    if not example_param:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            try:
                called_from = req_body.get('called_from')
                example_param = req_body.get('example_param')
                if not example_param or not called_from or not EXAMPLE_VAR_ENVIROMENT:
                    raise Exception('Una de las variables es nulo')
            except Exception as e:
                res_body['error'] = str(e)
                res_body['comment'] = "Error en request o variables de entorno"
                return write_http_response(400, res_body)

    #Logging called from
    logging.info('Called from: {}'.format(called_from))

    try:
        #DESARROLLO DE API ACA

        #RESPONSE OK
        #Build response body
        res_body['comment'] = "API executed OK"
        res_body['example'] = "mensaje generico"
        return write_http_response(200, res_body)
    #Error
    except Exception as e:
        #RESPONSE ERROR
        #Build response body
        res_body["comment"] = "API executed Failure. Check APIs, accounts/permissions and creds"
        res_body["exception"] = str(e)
        res_body['example'] = "mensaje generico"
        return write_http_response(400, res_body)

```
---
**Capturar log de errores de Azure Datafactory a través de API**
```
- Uso: Obtener log de errores de Datafactory a traves de las api de python
- Palabras clave: Datafactory, log, errores
- Lenguaje: Python 
 - Autor: Julian Biltes 
```
``` python
from azure.mgmt.datafactory import DataFactoryManagementClient as adf
import azure.mgmt.subscription as subs
import adal
from msrestazure.azure_active_directory import AdalAuthentication
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD
from datetime import datetime, timedelta
import os
 
TENANT_ID = os.environ.get('USR_AZURE_TENANT_ID')
CLIENT = os.environ.get('USR_AZURE_CLIENT_ID')
KEY = os.environ.get('USR_AZURE_KEY')
resource_group_name = os.environ.get('ADF_RESOURCE_GROUP_NAME')
adf_name = os.environ.get('ADF_NAME')

#Get credentials
def get_credentials():
    LOGIN_ENDPOINT = AZURE_PUBLIC_CLOUD.endpoints.active_directory
    RESOURCE = AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id

    context = adal.AuthenticationContext(LOGIN_ENDPOINT + '/' + TENANT_ID)
    credentials = AdalAuthentication(
        context.acquire_token_with_client_credentials,
        RESOURCE,
        CLIENT,
        KEY
    )
    return credentials

#Get logs
def activity_log(run_id, start_time, end_time, status='Failed'):
    try:
        credentials = get_credentials()
        # Obtenes subscriptioId
        su = subs.SubscriptionClient(credentials=credentials)
        subsList = [sub.as_dict() for sub in su.subscriptions.list()]
        subsID = subsList[0]['subscription_id']
        # Arma cliente de data factory
        adf_client = adf(credentials, subsID)
        # Obtener logs
        activities = list(adf_client.
                                activity_runs.
                                    list_by_pipeline_run(
                                                        resource_group_name, 
                                                        adf_name, 
                                                        run_id, 
                                                        datetime.strptime(start_time, '%m/%d/%Y %H:%M:%S'),
                                                        datetime.strptime(end_time, '%m/%d/%Y %H:%M:%S'), 
                                                        status )
                        )
        if activities:
            return activities.as_dict()
        else:
            return {"error": {"message_1_API": "No se ha podido obtener logs. Verificar logs en Data Factory."} }
    except Exception as e:
        return {"error": {"message_2_API": "Se ha producido un error al momento de recuperar logs. " + str(e)} }


```
**Script DDL para polybase en Azure Data Warehouse/Synapse Analytics Service**
```
- Uso: Crear los objetos para polybase con la configuracion recomendada (y testeada!)
- Palabras clave: Azure Data Warehouse, Synapse Analytics Service, polybase, sql-server
- Lenguaje: SQL 
 - Autor: Julian Biltes 
```
``` SQL

CREATE EXTERNAL DATA SOURCE [adl] WITH (TYPE = HADOOP, LOCATION = N'abfss://[llenar, endpoint datalake]', CREDENTIAL = [DataLakeV2Cred])
GO

CREATE EXTERNAL FILE FORMAT [CsvFileFormat] WITH (FORMAT_TYPE = DELIMITEDTEXT, FORMAT_OPTIONS (FIELD_TERMINATOR = N'|', STRING_DELIMITER = N'"', FIRST_ROW = 2, USE_TYPE_DEFAULT = True))
GO

CREATE SCHEMA ext
GO
CREATE EXTERNAL TABLE [ext].[TABLE_NAME]
(
	[COLUMN_NAME1] [numeric](15, 0) NOT NULL,
	[COLUMN_NAME2] [varchar](8) NOT NULL,
	[COLUMN_NAME3] [int] NOT NULL,
	[COLUMN_NAME4] [float] NULL,
	[COLUMN_NAME5] [datetime2](7) NULL
)
WITH (DATA_SOURCE = [adl],LOCATION = N'raw-data/example-path/',FILE_FORMAT = [CsvFileFormat],REJECT_TYPE = VALUE,REJECT_VALUE = 0)

GO
SELECT TOP 10 * FROM [ext].[TABLE_NAME]

```

-----------------
**Recibir parametros desde un pipeline de Data Factory**

	- Uso: recibir parametros de un pipeline de data factory, pasados en un notebookActivty

	- Palabras clave: Data Factory, Azure, Pipeline, Parameters.

	- Lenguaje: Python.
	
	- Autor: Efrain Diaz.
	
	- Source: https://bi64pro.com/using-parameters-with-azure-data-factory-and-databricks/?fbclid=IwAR2EVxiDZvrjr7CCZaf7RUR1jILcNS91LbRvfVSKwzf-HnY2DoLv44TEfvc

``` python	
tabla = getArgument("p_table")
fecha = getArgument("p_datetime")
file = tabla+"_"+fecha+".parquet"
```


-----------------
**Count de todas las tablas del Warehouse (Synapse)**

	- Uso: una query que devuelve el count de las filas que tiene cada tabla.

	- Palabras clave: T-SQL, Azure, Synapse, Tables.

	- Lenguaje: T-SQL.
	
	- Autor: Martin Zurita.
	
``` sql
select schema_name(tab.schema_id) + '.' + tab.name as [table],
       sum(part.rows) as [rows]
   from sys.tables as tab
        inner join sys.partitions as part
            on tab.object_id = part.object_id
where part.index_id IN (1, 0) -- 0 - table without PK, 1 table with PK
group by schema_name(tab.schema_id) + '.' + tab.name
order by sum(part.rows) desc
```
---------------------

**Distribucion en 60 instancias de Warehouse (Synapse)**

	- Uso: una query que nos dice como se distribuyen las filas para una tabla particular. Util para saber si esta causando un cuello de botella.

	- Palabras clave: T-SQL, Azure, Synapse, Tables.

	- Lenguaje: T-SQL.
	
	- Autor: Martin Zurita.

``` sql
DBCC PDW_SHOWSPACEUSED("schema.tabla")
```

---------------------

**Habilitar login por AD en Warehouse (Synapse)**

	- Uso: con este procedimiento se puede configurar usuarios de Active Directory (AD) para que puedan loguear sin la necesidad de tener un usuario de base de datos. Se debe utilizar la opcion "Azure Active Directory - Password".

	- Palabras clave: T-SQL, Azure, Synapse, Permisos.

	- Lenguaje: T-SQL.
	
	- Autor: Martin Zurita.

``` sql
Se hace basicamente en 2 pasos:
    1. Desde el portal, setear para el server de SQL un Active Directory Admin.
    2. Loguear a la BD con un usuario que tenga permisos de ALTER ANY USER y ejecutar la siguiente consulta:
    
   CREATE USER [user@dominio.com.ar] FROM EXTERNAL PROVIDER;

El usuario tambien puede ser reemplazado por un grupo de AD, lo cual facilita el control de permisos.
```

---------------------

**Habilitar firewall por IP en Azure SQL**

	- Uso: con esto logramos no depender del firewall del server, que habilita acceso a todas las bases de datos dentro de el. Con esto podemos habilitar una ip o un rango de ips solo para una BD dentro del server.

	- Palabras clave: T-SQL, Azure, Synapse, Permisos.

	- Lenguaje: T-SQL.
	
	- Autor: Martin Zurita.

``` sql
EXECUTE sp_set_database_firewall_rule N'Nombre Regla', '0.0.0.0', '0.0.0.0';  

La primera ip es la inicial, y la segunda es la del final del rango. Si se quiere habilitar una unica IP, escribirla como inicial y final.
```

---------------------

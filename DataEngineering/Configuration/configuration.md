
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

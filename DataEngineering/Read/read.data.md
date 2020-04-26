# DataEngineering
Repository of code snippets for usual data engineering stuff.
---
**Leer tabla de SQL SERVER desde Databricks**
```
- Uso: Obtener datos de una tabla a traves del conector JDBC
- Palabras clave: SQL-SERVER, Databricks, SQL
- Lenguaje: Python (Spark)
 - Autor: Julian Biltes 
```
``` python
#String connection
jdbcUrl = 'jdbc:sqlserver://[IP SERVER]:1433;database=[NAME DATABASE];user=[USER];password=[PASSWORD];encrypt=false;driver=com.microsoft.sqlserver.jdbc.SQLServerDriver;loginTimeout=30;'

#Connector Spark
df = spark.read.jdbc(jdbcUrl, "(SELECT TOP 10 * FROM TABLE) AS subq")

#Show data
display(df)
```
---
**Obtener el ultimo file de un lake desde Databricks**
```
- Uso: A veces precisamos obtener solo ultimo file de un lake (personas/2020/04/26/*.csv) y no todos (personas/*/*/*/*.csv).
Poder tener un script que identifique cual es el ultimo file para cada entidad o tabla en el lake puede significar un ahorro de procesamiento enorme si dentro del lake poseemos gran volumen de datos.
- Palabras clave: Databricks, Data lake
- Lenguaje: Python (Spark)
 - Autor: Julian Biltes 
```
``` python
import os

#Path donde se almacenan los csv
pathRoot = "/dbfs/mnt/test/raw-data/"
listLatestPath = []
#Se obtienen las tablas
for tabla in os.listdir(pathRoot):
  path = '{}/{}'.format(pathRoot, tabla)
  #Se obtiene el mayor año
  years = [ int(year) for year in os.listdir(path) ]
  maxYear = max(years)
  
  path = '{}/{}'.format(path, maxYear)
  #Se obtiene el mayor mes
  months = [ int(month) for month in os.listdir(path) ]
  maxMonth = max(months) if max(months) > 10 else '0' + str(max(months))
  
  path = '{}/{}'.format(path, maxMonth)
  #Se obtiene el mayor dia
  days = [ int(day) for day in os.listdir(path) ]
  maxDay = max(days) if max(days) > 10 else '0' + str(max(days))
  
  #Se agrega a la lista de paths
  path = '{}/{}/*.csv'.format(path, maxDay).replace("/dbfs",".")
  listLatestPath.append(path)

#Se crea un array de dataframe spark con los ultimos datos para cada tabla
listDf = []
for path in listLatestPath:
  df = spark.read.format("csv").option("header", "true").load(path)
  listDf.append(df)
```
---
**Scrapping tabla html con Selenium**
```
- Uso: Scrapea una tabla html de una pagina web. 
- Palabras clave: Selenium, Scrapping, Scrapeo
- Lenguaje: Python
 - Autor: Julian Biltes 
```
``` python
#Se utiliza selenium para dar click en el boton debido a que es una pagina dinamica
from selenium import webdriver
import pandas as pd
from lxml import html
import time

#Se levanda un webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_driver = "/tmp/chromedriver/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)

#Se ejecutan los pasos correspondientes para llegar a la tabla
driver.get('http://siga.inta.gov.ar/#/data')
#Se espera 5 segundos para que cargue la pagina
time.sleep(5)
driver.execute_script('document.getElementsByClassName("tabFont")[1].click();')
#Boton para descargar csv
#driver.execute_script('document.getElementById("btnDatosHorarios").click();')

#Luego de visualizar la tabla, se extrae el contenido html
page = html.fromstring(driver.page_source)
trs = page.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div/table//tr')
print(len(trs))
#Se procesa el html para convertir la tabla a un df
df = None
if trs:
    items = []
    for tr in trs[1:]:
        #print(tr.xpath('td[1]//text()'), len(trs))
        item = {
                        "Nombre": tr.xpath('td[1]//text()')[0] if tr.xpath('td[1]//text()') else None,
                        "Tipo": tr.xpath('td[2]//text()')[0] if tr.xpath('td[2]//text()') else None,
                        "Localidad": tr.xpath('td[3]//text()')[0] if tr.xpath('td[3]//text()') else None,
                        "Provincia": tr.xpath('td[4]//text()')[0] if tr.xpath('td[4]//text()') else None,
                        "Id Interno": tr.xpath('td[5]//text()')[0] if tr.xpath('td[5]//text()') else None,
                        "Desde": tr.xpath('td[6]//text()')[0] if tr.xpath('td[6]//text()') else None,
                        "Hasta": tr.xpath('td[7]//text()')[0] if tr.xpath('td[7]//text()') else None,
                        "Días": tr.xpath('td[8]//text()')[0] if tr.xpath('td[8]//text()') else None,
                    }
        items.append(item)


        df = pd.DataFrame(items, columns=['Nombre','Tipo','Provincia','Id Interno',
                    'Desde','Hasta','Días'])

#Se almacena como csv
df.to_csv([PATH])
```
---
**Scrapy sencillo pagina Web**
```
- Uso: Scrapy de datos en pagina web. 
- Nota: Para obtener el Xpath de un elemento especifico de una web realizar CTRL+SHIFT+U, click derecho en el elemento e ir a 'Copy -> Copy Xpath'. Mas info: https://blog.scrapinghub.com/2016/10/27/an-introduction-to-xpath-with-examples
- Palabras clave: Scrapy, Scrapping, Scrapeo
- Lenguaje: Python
 - Autor: Julian Biltes 
```
``` python
import pandas as pd
import requests
from lxml import html
url = '[URL PAGINA WEB]'
response = requests.get(url)
page = html.fromstring(response.text)

data = page.xpath('//html/body/text()')

print(data)
```
---
**Adivinador de tipados**
```
- Uso: Este script es util para cuando se procesa archivos json o datos de scrapping y es necesario identificar el tipo de dato.
- Palabras clave: Scrapy, Scrapping, Scrapeo, Json, tipo de datos
- Lenguaje: Python
 - Autor: Julian Biltes 
```
``` python
def RepresentsDate(s):
    if s.find("-") != -1:
        try: 
            #probar castear con formato conocido
            datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
            return [str(datetime), len(s)]
        except ValueError:
            try: 
                #probar castear con segundo formato conocido
                datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
                return [str(datetime), len(s)]
            except ValueError:
                return False
    else:
        #No es datetime o el formato no es identificado
        return False

def RepresentsIntOrFloat(s):
    try: 
        # cast, if this fails call except
        int(s) 
        # here did not fail
        # it's int or float, continue

        s = str(s) # it may be int or float but for float we need know its len
        posPoint =  s.find(".") # it's have a point?
        if posPoint != -1:
            # yes, it's a float
            return [str(float), [len(s[:posPoint]), len(s[posPoint+1:])]]
        else:
            # no, it's a int
            return [str(int), len(s)]
            
    except ValueError:
        #It isn't int or float
        return False

def get_type_value(value):
    if value == None:
        return [None, 0]
    
    represent = RepresentsIntOrFloat(value)
    if represent:
        return represent
    
    represent = RepresentsDate(value)
    if represent:
        return represent

    #Si no es nulo, int, float ni datetime asumimos str
    return [str(str), len(str(value))]
```
---

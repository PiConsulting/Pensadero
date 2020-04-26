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

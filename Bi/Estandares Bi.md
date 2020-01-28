
                                      ......                                     
                              `--oyhπ─π─π─π─hso--`                             
                           -+yπ─π─π─π─π─π─π─π─π─π─y+-                          
                        `+hπ─π─π─π─π─π─π─π─π─π─π─π─π─h+`                       
                      `π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─`                     
                     -π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─oh-                    
                   `sπ─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─s`                  
                  `yπ─π─π─π─π─oyo-------------+hπ─π─π─π─π─π─y`                 
                  sπ─π─π─π─π─+`     `````````  +π─π─π─π─π─π─os                 
                 :π─π─π─π─oh.  -y-  sπ─π─π─o+  +π─π─π─π─π─π─π─:                
                 yπ─π─π─π─o+  -π─-  sπ─π─π─o+  +π─π─π─π─π─π─π─s                
                `π─π─π─π─π─+  -π─-  sπ─π─π─o+  +π─π─π─π─π─π─π─o                
                .π─π─π─π─π─h.  -y-  sπ─π─π─o+  +π─π─π─π─π─π─π─o`               
                .π─π─π─π─π─π─+`     sπ─π─π─o+  +π─π─π─π─π─π─π─o`               
                 hπ─π─π─π─π─π─oyo.  sπ─π─π─o+  +π─π─π─π─π─π─π─y                
                 -π─π─π─π─π─π─π─o-  sπ─π─π─π─  -π─  π─π─π─π─π─:                
                  yπ─π─π─π─π─π─π─-  sπ─π─π─oh-  `  `yπ─π─π─π─s                 
                  .hπ─π─π─π─π─π─os:-hπ─π─π─π─os+--ohπ─π─π─π─y`                 
                   .yπ─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─y`                  
                    `π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─o+                    
                      -yπ─π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─s.                     
                        -π─π─π─π─π─π─π─π─π─π─π─π─π─π─π─.                       
                          `:shπ─π─π─π─π─π─π─π─π─π─ho:`                         
                              .-oshπ─π─π─π─π─hso-.                             
                                    `......`    


# Estandares de Power BI

Por cualquier duda técnica de como realizar algo que nunca se vio disponible, consultar a un compañero. No reinventar rueda.

## Formato
	
### Página	
- Toda página tiene un wallpaper/papel tapiz, caso de no saber que poner usar el gris antiguo de power bi con fondo sin transparencia.
- Toda página lleva título en cuadro de texto.
- Usar los colores de la marca para la cual se trabaja y agregar el logo de la misma en las páginas. Puede generarse un theme (.json) para ahorrar trabajo en dicha marca.
- Los filtros deben estar alineados en la misma ubicación de pantalla (no hay fijo si es izquierda, solo que sea igual en todas las páginas)

### Titulo
- Cuadro de Texto (Titulo de Pagina):  Colores de la empresa, letra 22.
- Graficos: Titulos letra 14 color máximo gris
- Tabla: Sin Titulo
- Filters: No usar Título. Modificar Nombre de columna y su label con letra 14 color máximo gris

### Data Labels
- Lineas y Barras: Activar valores como visibles, no vienen por defecto
- Torta: Categoría y valor, salvo que cliente quiera porcentaje

### Disposición Visual
- Mantener Filtros ecualitarios para todas las paginas, por ejemplo: Si se usan filtro de fecha en distintas páginas ubicarlo en mismo lugar
- Editar interacciones: Evitar las interacciones resaltadas (highlight) cuando el valor se hace imperceptible.

### Colores
- Usar colores de mandados por el cliente para visualizaciones
- Utilizar recuadro o fondo de un color deseado para los Labels

### Mapa
- Aumentar el tamaño de las burbujas por defecto

### Idioma
- Mantener siempre el idioma castellano, tanto para titulos como para meses

### Sugerencias
- Mantener 1-3 visualizaciones infográficas como máximo para no perder visibilidad de información ni agregar complejidad
- Utilizar Labels/Tarjetas en la mayoría de las pantallas para mantener información importante resaltada
- De ser posible evitar anillos y usar torta por barras (puesto que se pierde visibilidad de información a menos que sean menos de 3 categorías.)
- Evitar mapa de areas y usar el de circulos (más preciso)
- Formatear matriz y tabla con tamaño y colores agradables.


## Modelado

### Diseñar un modelo de estrella a partir del motor de BD y peor de los casos en Power Query (evitarlo si son millones de registros)
- Las dimensiones comenzarán con prefio D_[Nombre] y las tablas de hecho con F_[Nombre].
- En caso de contener tablas ajenas a la estrella que sean de soporte incluirán la A de auxiliar, ejemplo A_[Nombre]

### Power Query
- No incluir espacios en nombres de tabla
- Reducir los pasos a la menor cantidad posible evitando la redundancia de pasos iguales en cuanto sea posible. Ejemplo: no usar dos "Change Type" si se puede evitar
- Si la fuente de datos es una consulta y es posible mezclar/transformar datos en el origen, entonces prefiltrarla y cambiarle nombres para evitar pasos via Power Query
- Si es posible hacer multiples reemplazos de texto
- Siempre usar una tabla fecha, mientras más atrás pueda generarse mejor.
- Todo paso personalizado (Agregar y transformar columnas o funciones) deben estar comentadas en el editor avanzado.

### Numeros
- Hasta dos decimales
- No dejar columnas numéricas como texto a menos que se requiera.
- Siempre usar el punto en millones y miles "."
- Usar categorizaciones. Ejemplo valores monetarios y porcentaje cuando sea requerido.

### Texto (categórico)
- Evitar cadenas de números como texto porque utilizan más memoria
- Controlar y reemplazar valores con errores ortograficos o de espacios en power query
- Texto conjunto, concatenarlos en Edit Query vía Text.Combine o separandolos por &
- Utilizar "Nuevo Grupo" para categorizacion de Texto en el modelo aplicado

### DAX
- Código DAX NO formateado NO ES DAX. Formatearlo en https://www.daxformatter.com/ o a mano.
- Comentar medidas complejas. Llamese compleja cualquiera que incluya funciones ademas de la agregación (sum, count, etc).
- En caso que haya código repetido en la consulta utilizar variables para optimizar el uso de memoria.
- Utilizarlo para valores totales o complejos (matemática)
- Usar medidas para cálculos sencillos. SUM de una columna o COUNT de una columna con el formato y nombre adecuado.
- Deben crearse dentro de las tablas de hecho en lo posible.


## Actualizaciones programadas y gateway

- El Gateway siempre debe ser el On Premise Data Gateway empresarial (no el personal). 
- Conocer los origenes del empresarial vs personal para saber cuando implementar cada cual.
- Siempre utilizar de clave de recuperación la misma cadena de caracteres que el NOMBRE del gateway.
- Evitar usar gateway para fuentes en nube.
- Recuerde: Si hay fuentes nube y on premise activar opción correspondiente.
# Envío de Emails En Power BI - Parte 2


Te ha pasado que un gerente o un líder te pida un status diario por correo a las 8 am? Power BI provee esa posibilidad! Se puede programar envíos de dashboards de los reportes creados.
En la primera entrega hablamos de Envíos de mails con Power BI Service.<br />
En este caso, estaremos trabajando con un flujo de *Power Automate* para programar el envío de correos.

Consideraciones:<br />
-Contar con Power BI Desktop instalado. <br/>
-Contamos con un reporte creado.
<br /> 


<br />
-Comenzamos: <br />
<br />
Nos dirigimos a Power BI Desktop dónde tenemos un reporte abierto en un dashboard que tiene una tabla con distintos campos:


![Foto modelo](captura1.png)


Utilizaremos la visual de "Power Automate" que se encuentra en el menú de visualizaciones:


![Foto modelo](captura3.png)



Hacemos clic en el mismo para agregarlo al dashboard:
Veremos que se da un instructivo de cómo se debe utilizar esta visual.


![Foto modelo](captura4.png)

Lo primero que debe hacerse es, agregar los campos que queremos enviar por correo. Usaremos los mismos que están en la tabla del medio.

![Foto modelo](captura5.png)

Luego, se debe hacer clic en los "3 puntitos" de la visual y editarla.

![Foto modelo](captura6.png)

Luego se debe hacer clic en "New" y elegir la opción "Instant cloud flow" para crear  un nuevo flujo.

![Foto modelo](captura7.png)

Luego que está creado, lo primero que vemos es un paso por defecto de power BI, seguiremos creando un nuevo step.

![Foto modelo](captura8.png)

Escribimos en el campo de búsqueda de objetos "select" y seleccionamos el objeto select de "Data Operation"

![Foto modelo](captura9.png)

En el campo "From" buscamos seleccionar el componente dinámico "Power BI data"

![Foto modelo](captura10.png)

Luego, empezamos a mapear los campos de la tabla que necesitamos enviar por correo.

![Foto modelo](captura11.png)

Debería quedar algo así:

![Foto modelo](captura12.png)

Ya seleccionamos los datos, ahora pasamos a crear un nuevo paso.

![Foto modelo](captura13.png)

Buscamos la actividad "html table" y seleccionamos "Create HTML table"

![Foto modelo](captura14.png)

En el campo "From" seleccionamos el output que es el paso que corresponde a la actividad "select"

![Foto modelo](captura15.png)

Por último, creamos el cuarto paso.

![Foto modelo](captura16.png)

Buscamos la actividad "send an email" y seleccionamos "Send an email (V2)"

![Foto modelo](captura17.png)

Le damos formato al correo escribiendo la dirección del mail, el asunto y el body.

![Foto modelo](captura18.png)

Seleccionamos el output de la tabla HTML:

![Foto modelo](captura20.png)

Luego de finalizar dichos pasos, hacemos clic en "save" para guardar el flujo. 

![Foto modelo](captura21.png)

Luego que se guardó, hacemos clic en "Apply"

![Foto modelo](captura22.png)

El mensaje que debe aparecer es este en color verde informado que se ha creado el flujo de actividades con éxito:

![Foto modelo](captura23.png)

Ahora, si hacemos clic en "Back to report" podemos observar que nuestro botón cambió su presentación:

![Foto modelo](captura24.png)

![Foto modelo](captura25.png)

Si hacemos clic en dicho botón creado "Run Flow" veremos que se ejecuta y se envía correctamente:

![Foto modelo](captura26.png)

Si abrimos nuestro correo, veremos que llegó el correo exitosamente:

![Foto modelo](captura27.png)


*Importante:* Si se quiere programar el envío diario de correos como en el post anterior, es necesario utilizar Power Automate de manera independiente, desde la visual de Power BI NO puede hacerse ya que, Power BI se utiliza para interactuar con flujos existentes y mostrar información relevante en el informe.


Aclaraciones:
- Se puede personalizar el botón de flujo y controlar las ejecuciones históricas del flujo.
- Se puede formatear los campos de data que se envían en el correo.


# Bibliografía

https://app.powerbi.com/

https://learn.microsoft.com/en-us/power-automate/

https://learn.microsoft.com/en-us/power-automate/format-data-by-examples

---

By **Facundo Montenegro**

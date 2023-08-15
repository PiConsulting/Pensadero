# Power BI - Administrando roles con RLS


Te ha sucedido que un usuario te pide ver sólo la información que le corresponde? Cómo se pueden aplicar filtros para poder controlar la información que pueden ver determinados usuarios?

La respuesta es, con RLS, o mejor conocido Row Level Security (Seguridad a nivel de filas) y lo veremos aplicado con un simple ejemplo.


Consideraciones:<br />
-Contamos con un proyecto en Power BI Desktop.<br />
-Contamos con un reporte creado y un workspace configurado en Power BI Service.
<br /> 


<br />
-Comenzamos: <br />
<br />
Nos dirigimos a Power BI Desktop dónde tenemos nuestro proyecto desarrollado.

![Foto modelo](captura1.png)

Tenemos nuestro reporte con sus gráficos y sus funcionalidades pero... en el slicer "Seller" podemos ver a tres usuarios diferentes que son de distintos países. Cómo podemos hacer que vean por ejemplo, la información SÓLO de su país?

Se debe hacer clic en Modeling y luego en Manage roles.

![Foto modelo](captura2.png)

Luego definiremos la lógica a utilizar para lograr diferenciar a estos usuarios por países, en este caso, crearemos un rol por cada país.

![Foto modelo](captura3.png)

Creamos el primer rol y le agregamos un filtro por país.

![Foto modelo](captura4.png)

En la expresión, debemos cambiar el "Value" por el nombre del rol por el cuál vamos a filtrar, en este caso, "Argentina"

![Foto modelo](captura5.png)

![Foto modelo](captura6.png)

Entonces, continuamos con el siguiente país repitiendo la misma lógica.

![Foto modelo](captura7.png)

Agregamos el filtro por país.

![Foto modelo](captura8.png)

Y cambiamos el valor de la expresión por "Brasil"

![Foto modelo](captura9.png)

Lo siguiente es guardar los cambios.

![Foto modelo](captura10.png)

Ahora, podemos testear que efectivamente funcionen estas reglas creadas haciendo clic en el botón "View as"

![Foto modelo](captura11.png)

Elegimos uno de los roles para ver y hacemos clic en OK.

![Foto modelo](captura12.png)

Se puede ver perfectamente que la información está filtrada por los usuarios de un determinado país.

![Foto modelo](captura13.png)


Ahora podemos probar esto Power BI Service publicando los cambios.


![Foto modelo](captura15.png)

Se hace clic en "Save" para guardar los cambios.

![Foto modelo](captura16.png)

Elegimos el workspace dónde se publicará el reporte y publicamos.

![Foto modelo](captura17.png)

Ahora, nos dirigimos a la web app.powerbi.com e ingresamos nuestras credenciales de usuario.

![Foto modelo](captura18.png)

Una vez dentro de Power BI Service, buscamos nuestro workspace y el reporte que publicamos.

![Foto modelo](captura19.png)

Acercamos el cursor sobre "More options" y buscamos la opción "Security"

![Foto modelo](captura20.png)

Seleccionamos dicha opción.

![Foto modelo](captura21.png)

Ahí podremos ver los roles que creamos en Power BI Desktop y podremos agregarle los usuarios de cada rol, en este caso agregamos un usuario de Argentina.

![Foto modelo](captura22.png)

Guardamos los cambios.

![Foto modelo](captura23.png)

Ahora podremos probar el rol del usuario agregado en "More options"

![Foto modelo](captura24.png)

Seleccionamos la opción "Test as role"

![Foto modelo](captura25.png)

Y asi queda configurado el RLS por países.

![Foto modelo](captura26.png)

Se pueden seguir agregando filtros o definiendo nuevos roles para controlar el RLS de una manera más estricta y volver más complejo el dominio.

Se adjunta el archivo .pbix a la solución.


</br>

# Bibliografía

https://app.powerbi.com/

https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls


---

By **Facundo Montenegro**

# Docker for ML
Algunos dockerfiles listos para usar con diferentes librerias, basados en linux
- [Ubuntu](https://ubuntu.com/):
  Distro standard para dockers
- [Alpine](https://alpinelinux.org/): 
  Siempre que se pueda se recomienda usar esta distro ya que es muy liviana ~80Mb


# How to use
Se necesita una repositorio de dockers:
- [DockerHub](https://hub.docker.com/):
  Repositorio estandar que cualquiera puede usar, es donde estan las imagenes publicas comunes.
- [Azure Container Registry (ACR)](https://docs.microsoft.com/en-us/azure/container-registry/):
  Repositorio alojado en Azure que podemos crear para tener imagenes privadas de Docker
  
Veamos un ejemplo de como deployar una imagen docker con ACR:

Primero debemos [crear un ACR](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal#create-a-container-registry) en azure y habilitar el Admin user:
![image](https://docs.microsoft.com/en-us/azure/container-registry/media/container-registry-authentication/auth-portal-01.png)

- Compilamos la imagen pasando a -f el nombre del archivo Dockerfile y a -t el nombre que tendra nuestra imagen docker:
``` bash
docker build -f python.Dockerfile -t mi-docker . 
```
- Con las credenciales que obtenemos del ACR (username, server y password) nos logueamos con docker
```bash
docker login -u <username> <server.azurecr.io>
```
- Luego taggeamos la imagen y la enviamos al ACR
```bash
docker tag mi-docker:latest <server.azurecr.io>/mi-docker:latest
docker push <server.azurecr.io>/mi-docker:latest
```

### Usar nuestro docker en Data-Bricks

Podemos usar nuestro docker como base para el cluster de data bricks, ***esto nos permite instalar programas, librerias y drivers 
en la imagen docker y no tener que usar un init_script cada vez que el cluster inicia***, para esto:

- Habilitamos los [Azure Container Services](https://docs.microsoft.com/es-es/azure/databricks/administration-guide/clusters/container-services)
- Seleccionamos nuestro docker como en la siguiente imagen 
![image](https://docs.microsoft.com/es-es/azure/databricks/_static/images/clusters/custom-container-azure.png)
  En authentication seleccionamos user and pass y ponemos las mismas credenciales que nos da 
  el ACR (las que usamos para loguearnos con docker), y tendremos nuestro cluster con una imagen personalizada.
  

Good luck and bye!

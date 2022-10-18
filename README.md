# Aplicación de reseñas de juegos gratuidos
### Made by Brayan Espina y Esteban Garay

:hammer_and_pick:	Herramientas empleadas:
- Mysql
- Python
- Flask
- Docker
- Bootstap

Para comenzar, clone el repositorio:
```
git clone https://github.com/eltioantonioxd/rese-aT1.git
```
Levante el proyecto:
```
docker-compose up
```

Corrobore el estado de los contenedores:
```
docker ps
```

Para bajar la instancia utilice:

```
docker-compose down
```
*Recuerde emplear la rama master para clonar el repositorio, ya que es la más actualizada y funcional*

# Explicación de Dockerfile empleado

```
#Se selecciona la imagen de python, donde para obtener una versión más liviana del mismo se opta por alpine
FROM python:3.7-alpine

#Se establece un directorio de trabajo dentro del contenedor
WORKDIR /app

#Se copian los archivos asociados a la carpeta backend-flask hacia el contenedor
COPY ./backend-flask .

#Se instalan las dependencias necesarias para correr el proyecto; en este caso el archivo requirements.txt cuenta con los requerimientos
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
```

# Explicación de Docker-compose empleado

```
#Se declara la versión de docker-compose a emplear
version: '3.3'

#Se declaran los servicios a utilizar
services:

  #Configuración del servicio flask, donde se contruye la imagen a partir del Dockerfile que esta ubicado al mismo nivel que el compose
  flask: 
    build: .
    container_name: app_flask
    restart: always
    depends_on:
      - mysql
    ports:
      - "4000:4000"
    volumes:
      - ./backend-flask:/app

  #Configuración del servicio MYSQL, donde se utiliza la imagen de docker hub directamente
  mysql:
    image: 'mysql:5.7.13'
    container_name: mysql
    restart: always
    ports:
      - "3306:3306"
    volumes:
      -  ./bd-mysql:/var/lib/mysql
    env_file:
      - common.env
  ```


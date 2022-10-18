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

# Explicación de Dockerfile empleado en Flask

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




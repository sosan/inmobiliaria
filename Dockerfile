# Docker utiliza los contenedores como maquinas virtuales muy livianas y modulares, flexibles, open source. ibm, microsoft 
# acutalmente uno de los mecnisos son capaces de crear cocidgo de destribuirlo de forma sencilla sin quebraderes 
# solomon hykes creador

# paso a poso

FROM alpine:3.11.2

# instalar python 3 y la ultima version de pip

RUN apk add --no-cache python3-dev g++ gcc libxslt-dev && pip3 install --upgrade pip
#RUN apk --update add bash nano

# en terminal 

# docker build -t nombnreimagen . 
# docker build -t sosan/cheers2019 .
# docker build -t sosan/fedora-jboss:latest \
        # -t sosan/fedora-jboss:v2.1 .

# # contendor linux 
# docker run -it --rm sosan/cheers2019
# # instalar redis 
# docker run --name some-redis -d redis
# docker run -it nombreapp 

# crear una carpeta dentro de l sistema alpine para almacenar  nuesta app
WORKDIR /app

# copiar todos los archivos de esta capreta
COPY . /app

# instalar las dependencias
RUN pip3 --no-cache  install -r requirements.txt

# docker run -it --publish 7050:5000 nombreapp
# docker run -it -p 7050:5000 inmobiliaria

# lista de tareas pendientes
# CMD [ "python3", "main.py" ]
# CMD [ "SET FLASK APP", "main.py" ]
# las ips de entorno locla son diferentes a las ips de la imagen docker
ENV FLASK_APP=main.py:app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5100"]
# docker run --name=ho -p 80:5100 horoscopo_ima:v1 
# docker run --name=ho2 -p 80:5100 -v /mnt/hgfs/proyectospython/horoscopoprofe/horoscopoChino/src:/app/src horoscopo_ima:v1

# debug=True

# ejecutamos apllicacion de docker
#docker run -it -p 7050:5000 -d nombreapp

#docker
# docker container ls

# docker stop ids_del container


# docker build -t flask_new .


## 
##normalamente se explica para mostrar como 
#imagen cuando esta apagada
# docker run 

# docker exec cuando tenemos la imagen cargada
# docker ps
# docker run -it nomreapp /bin/sh  # se va ha abrir en shell
# cd src es donde esta totod el contentido
# main nos importa ...

# src
#   conexion.py
# conexiones 
# from flask import Flask

#Docckerfile
# cerrar la aimagne
# dodcker run -it -p 5050:5000 -d nombreapp

# volumenes dentro de docker
# docker exec -i -t id:iamgend  /bin/sh
# lo mas comane es hacer en caprta
# docker run -it -p 5100:5000 -v ruta_absoluta:carpeta_dentro_de_docker__/app/src -d nombre_docker

# docker run --name=mongoserv -d -v /opt/mongodb:/data/db  mongo # -p 27017
# docker exec -it mongoserv bash

# mongo # si hemos cambiado puerto: localhost:27017
# use dbtest
# for (var i = 0; i < 25; i++) { 
# db.testing.insertOne( { "hola" : "mundo" } )
# }
# db.testing.find()
# exit
# exit



# heroku => plataform
# doker => integracion y desarrollo
# 

# Docker esta especiializada en la construccion de estructuras en servidores
# Contendor es una agrupacion de procesos
# limite estricto de maquina virutal (no hay posibilidad de consumir mas)
# ejecutamos de forma nativa, delante del sistema operativo
# los contendiso con el unico sistema operativo que no tienen que hacer un prosces de virutlaizaicon linux
# carpetas /var/lib/docker/...

# dentor del contenedor se genera un unviersor completamente hermetico
# cada uno tiene un id compleemtne id unico y un nombre unico(hash)

#




# contenedor
# docker ps -a => log

# # imagen nos ayuda a crear el contenedor
# docker images => visualizar las imagenes


# # eleminar contendores
# docker rmi  
# docker rm cb173d505f04

# docker rm $(docker ps -aq)
# # comando -f forzar

# docker run ubuntu tail -f /dev/null


# funciona como s

# Imagen de docker
# Son plantillas de contenedores que a partir de ellas genermos contenedores que uno queira.

# Imagenes que no cambian. Distribucion muy simple atraves de docker run. dokcer pull <nombre imagen>
# docker pull ubuntu
# docker pull nombreusuario/nombre_imagen

# una imagen es un conjunto de capas (layers) siempre es necesario una capa base para aguantar las demas capas.
# normalmente suele ser un sistema operativo o bien lo lleva incorporado.
# Dockerfile define los layers, y cada cada es independiencte de las demas capas.
# docker image ls => listar todas las imagenes 
# Si no especificamos una etiqueta se entiende que es la version latest, pero quizas no sea la mas reciente.
# docker pull ubuntu:18.10 => coge la version  18.10 de ubuntu 

# como hacer nuestra propia imagen.
# ===========
# para hacer nuestra propia imagen, nevcesitamos un Dockerfile. y no es posible un Dockerfile  sin FROM *
# FLUJO DE TRABAJO
# dOCKERFILE => BUILD => IMAGEN => RUN => CONTENEDOR
# 
# docker push prueba:v1.5 => error => error
# docker tag prueba:v1.5 toniferra72/prueba:v1.5
# docker push toniferra72/prueba:v1.5 => subimos
# docker pull toniferra72/prueba:v1.5 => bajamos


# docker history mongo
# dive mongo 
# wget https://github.com/wagoodman/dive/releases/download/v0.9.1/dive_0.9.1_linux_amd64.deb
# sudo apt install ./dive_0.9.1_linux_amd64.deb

# no es posible volver a un layer anterior.
# en el momento que se hace ya no se puede tocar.


# docker build -t nodejs .

# docker run --rm -p 3000:3000 nodejs

# cache layers
# QUE HACE CUANDO CREA LOS layers
# es posible que ya una vez tengas instalado mongo por ejemplo, no pierde otra vez montando el layer.

# cada vez que haya un pequeño cambio, se tiene hacer todo el build de nuevo
# docker commit nombre_del_contendor
# cambio 
#copy

#  docker cp src ho2:/app
# docker run --name=horo_c -p 81:5100 -v /mnt/hgfs/proyectospython/horoscopoprofe/horoscopoChino/src:/app/src  horoscopo_ima:v1

# https://dzone.com/articles/docker-backup-your-data-volumes-to-docker-hub
# docker tag hor_test:v1 sosan/horo_test:v1
# docker push sosan/horo_test:v1


# docker network create --attachable redtoni
# docker run -d --name=db mongo
# docker run --name=flask -d  horoscopo_ima:v1
# docker network connect redtoni db
# docker nwtowkr connect redtoni flask

# docker network inspect redtoni

# "IPv4Address": "172.19.0.3/16",
# "IPv4Address": "172.19.0.2/16",

# docker esta al mando de esas redes.

# docker compose esta creado para que haya menos equivocaaciones. es una ayuda para todos los pasos necesarios.
# yaml .... 
# ejemplo 
# 



































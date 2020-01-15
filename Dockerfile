# Docker utiliza los contenedores como maquinas virtuales muy livianas y modulares, flexibles, open source. ibm, microsoft 
# acutalmente uno de los mecnisos son capaces de crear cocidgo de destribuirlo de forma sencilla sin quebraderes 
# solomon hykes creador

# paso a poso

FROM alpine:3.11.2

# instalar python 3 y la ultima version de pip

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip
#RUN apk --update add bash nano

# en terminal 

# docker build -t nombnreimagen . 
# docker build -t sosan/cheers2019 .
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
RUN pip3 --no-cache install -r requirements.txt

# docker run -it --publish 7050:5000 nombreapp
# docker run -it -p 7050:5000 inmobiliaria

# lista de tareas pendientes
# CMD [ "python3", "main.py" ]
# CMD [ "SET FLASK APP", "main.py" ]
# las ips de entorno locla son diferentes a las ips de la imagen docker
ENV FLASK_APP=main.py:app
CMD ["flask", "run", "--host", "0.0.0.0"]

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


# docker run -it mongo /b
# ver un vistazo de como lo han implementado
# 


# heroku => plataform
# doker => integracion y desarrollo
# 

# go live















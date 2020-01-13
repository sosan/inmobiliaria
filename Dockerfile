# Docker utiliza los contenedores como maquinas virtuales muy livianas y modulares, flexibles, open source. ibm, microsoft 
# acutalmente uno de los mecnisos son capaces de crear cocidgo de destribuirlo de forma sencilla sin quebraderes 
# solomon hykes creador

# paso a poso

FROM alpine:3.11.2

# instalar python 3 y la ultima version de pip
RUN apk add --no-cache python3-dev && pip3 install --upgrade pip


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

# lista de tareas pendientes
# CMD [ "python3", "main.py" ]
# CMD [ "SET FLASK APP", "main.py" ]
# las ips de entorno locla son diferentes a las ips de la imagen docker
CMD [ "python3", "main.py" ]












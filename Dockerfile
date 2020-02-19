FROM python:3.8-slim-buster

# copiamos lugar volatil requirements
COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
        pip install -r /tmp/requirements.txt

# copiamos el shell a bin para comprobar si
# estmaos en entorno de desarrollo o produccion
COPY /testing.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/testing.sh

# para slim-buster
RUN useradd --create-home usuarioapp
WORKDIR /home/usuarioapp

# creamos el arbol de directorios
COPY /src /home/usuarioapp/src

# copiamos todo dentro de usuarioapp
# estamos copiando los dockerfile y docker-compose, etc..
# preguntar en el examen si lso dockerfile tienen que
# en la imagen.
#COPY . /home/usuarioapp

USER usuarioapp

# cambiamos directorio a SRC
WORKDIR /home/usuarioapp/src

# bin en PATH
ENV PATH="/home/usuarioapp/.local/bin:${PATH}"

# por si acaso no esta en requirements. memorion 2 veces al dia XD
RUN pip install gunicorn

# abierto puerto -- cambiar por otro puerto --
EXPOSE 5000
ENV PORT=5000

# argumentos y varibles de entorno para flask --  cambiar development/production . devolopment=hot reloads ----
# BUILD.... docker build -t dados:latest -t dados:v1 . --build-arg FLASK_ENV="development"
# RUN ..... docker run ........ -e "FLASK_ENV=production"
ARG FLASK_ENV="development"
ENV FLASK_ENV="${FLASK_ENV}" \
        FLASK_DEBUG=1 \
        FLASK_APP=main.py:app \
        PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1

# pequeño echo para saber si por defecto estamos en producion o development
# RUN set -ex; \
#     if [ "${FLASK_ENV}" = "development" ]; then \
#         echo "FLASK_ENV POR DEFECTO: development"; \
#     else \
#         echo "FLASK_ENV POR DEFECTO: production"; \
#     fi

ENTRYPOINT [ "/usr/local/bin/testing.sh" ]
# si estamos en produccion, no aconsejan a flask como servidor.
# aconsejan nginx + gunicorn
CMD ["python", "main.py"]



















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
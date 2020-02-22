# -*- coding:utf-8 -*-
"""
APLICACION BACKEND INMOBILIARIA

"""

import base64
import os
import math

from datetime import datetime

from flask import Flask, jsonify
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask import send_from_directory

from ModuloMongodb.ManagerMongodb import managermongo
from ModuloLogica.ManagerLogica import ManagerLogica

from ModuloHelper.ManagerHelper import Errores
from ModuloWeb.ManagerWeb import ManagerWeb
from flask_socketio import SocketIO
from flask_socketio import emit

import sys

# instanciaciones e inicializaciones
app = Flask(__name__)
managerweb = ManagerWeb()
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
errores = Errores()
managerlogica = ManagerLogica()

# configuracion
app.secret_key = "holaa"
# recuperar una ruta absoluta
CARPETA_SUBIDAS = os.path.abspath("static/images/archivos_subidos")
print("capr:" + CARPETA_SUBIDAS)
app.config["CARPETA_SUBIDAS"] = CARPETA_SUBIDAS
# limite 16 megas
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/c", methods=["GET", "POST"])
def ruta_css():
    if request.method == "POST":
        f = request.files["fichero"]
        # recuperar el nombre del archivo
        if f.filename == "":
            return "No seleccionado fichero"

        nombre_archivo = f.filename

        # la ruta donde queremos que se guarde nuestor archivo
        # recien subido y ademas que nos quede claro que os.path.join 
        # lo utilizamos para acceder a un directorio
        print("NOMBRE ARCHIVO => {0}".format(nombre_archivo))
        print("APP CONFIG CARPETA {0}".format(app.config["CARPETA_SUBIDAS"]),
              os.path.join(app.config["CARPETA_SUBIDAS"], nombre_archivo))
        f.save(os.path.join(app.config["CARPETA_SUBIDAS"]), nombre_archivo)
        return redirect(url_for("recibir_nombre"))

    # return send_from_directory("css", path)

    return """
    <form method="post" enctype="multipart/form-data">
    <input type="file" name="fichero" required accepted="*.png">
    <button type="submit">ENVIAR</button>
    <form>
    """


@app.route("/verarchivos/<nombre_archivo>")
def recibir_nombre(nombre_archivo):
    return send_from_directory(app.config["CARPETA"], nombre_archivo)


###################################

@app.route("/admin")
def admin_login():
    return render_template("login_admin.html")


@app.route("/admin", methods=["POST"])
def recibir_login():
    if "usuario" and "password" in request.form:
        ok, nombre = managermongo.primeracomprobacionadmin(request.form["usuario"], request.form["password"])
        if ok == True:
            session["usuario"] = request.form["usuario"]
            session["password"] = request.form["password"]
            session["nombre"] = nombre
            return redirect(url_for("menu_admin"))

        else:
            pass

    return redirect(url_for("admin_login"))


@app.route("/profile", methods=["GET"])
def menu_admin():
    if "usuario" and "password" in session:
        ok = managermongo.comprobar_existencia_usuario(session["usuario"], session["password"])
        if ok == True:

            # listado = managermongo.getallproductos()
            # dependiende de la configuracion elegir que mostrar primero
            # if config == True:
            listado = managermongo.get_sin_mediciones()
            # else .......
            # listado = managermongo.get_con_mediciones()
            if len(listado) > 0:
                fechadelta = datetime.utcnow()
                return render_template("menu_admin.html", datos=listado, fechaahora=fechadelta,
                                       totalelementos=len(listado))
            else:
                return render_template("menu_admin.html", datos=None)

    return redirect(url_for("admin_login"))


@app.route("/profile", methods=["POST"])
def menu_admin_post():
    return redirect(url_for("menu_admin"))


# @app.route("/profile/getlocation", mehtods=["POST"])
# def getlocation():
#     """
#     https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?prox=
#     41.8842,-87.6388,250
#     &mode=retrieveAddresses
#     &maxresults=1
#     &gen=9
#     &apiKey=k-EckgQuyQOTGQoMy54SsslKuX9oMP8PFj2SyV-_wJM
#
#     """
#
# """ https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json
# ?apiKey=k-EckgQuyQOTGQoMy54SsslKuX9oMP8PFj2SyV-_wJM &mode=retrieveAddresses &prox=41.8842,-87.6388,
# 250 &maxresults=1 """ "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.{format}"
# "https://geocoder.ls.hereapi.com/6.2/geocode.{format}" # uri = """ #
# https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=k-EckgQuyQOTGQoMy54SsslKuX9oMP8PFj2SyV-_wJM
#     &mode=retrieveAddresses #     &prox={0},{1} #     &maxresults=1 #     """.format(request.form["latitude"],
#     request.form["longitud"])
#
#     v = managerweb.getstreet(request.form["latitude"], request.form["longitud"])


@app.route("/profile/alta", methods=["GET"])
def alta_piso():
    if "usuario" not in session or "password" not in session:
        return redirect(url_for("admin_login"))
    else:
        posibleexistencia = managermongo.comprobar_existencia_usuario(session["usuario"], session["password"])
        if posibleexistencia == False:
            return redirect(url_for("admin_login"))

    if "anterior_calle" in session:
        anterior_calle = session.pop("anterior_calle")
        anterior_numero = session.pop("anterior_numero")

        outputhtml = managerlogica.generarmensajeerror(session["mensajeerror"], anterior_calle, anterior_numero)

        return jsonify({"data": outputhtml, "errores": session["mensajeerror"]})

    if "calle" and "numero" and "cp" and "habitaciones" and "localidad" and "numerobanos" \
            and "tipocasa" and "dueno" and "totalmetros" \
            in session:
        variables = managerlogica.mostrarvivienda()
        return render_template("alta_piso_admin.html", **variables)

    if "mensajeerror" in session:
        session.pop("mensajeerror")

    return render_template("alta_piso_admin.html")


@socketio.on('obtenercalle')
def obtenercalle(latitude, longitude):
    print("lat {0} long; {1} tipo:{2}".format(latitude, longitude, type(longitude)))
    calle, numero, cp, localidad = managerweb.getstreet(latitude, longitude)
    emit("r_obtenercalle",
         {
             "calle": calle,
             "numero": numero,
             "cp": cp,
             "localidad": localidad
         })


@app.route("/profile/alta", methods=["POST"])
def recibir_alta_piso():
    if "usuario" not in session or "password" not in session:
        return redirect(url_for("admin_login"))

    if "calle" and "cp" and "habitaciones" and "localidad" \
            and "banos" and "tipocasa" and "numero" and "dueno" and "telefonodueno" in request.form:

        # comprobacion de si ya existe el piso en la db
        posible_insercion = managerlogica.comprobarexisteinmueble(request.form["calle"], request.form["numero"])
        if posible_insercion == True:
            managerlogica.alta_vivienda(request.form, app.config["MAX_CONTENT_LENGTH"], app.config["CARPETA_SUBIDAS"])
        else:
            # ya existe
            managerlogica.procesar_formulario_noposibleinsercion(request.form)

    return redirect(url_for("alta_piso"))


@app.route("/profile/ver", methods=["GET"])
def ver_piso():
    return render_template("ver_piso.html")


@app.route("/profile/ver", methods=["GET"])
def buscar_piso():
    return render_template("buscar_piso.html")


@app.route("/profile/item", methods=["get"])
def ver_piso_para_modificar_get():
    if "usuario" not in session or "password" not in session:
        return redirect(url_for("admin_login"))
    else:
        ok = managermongo.comprobar_existencia_usuario(session["usuario"], session["password"])
        if ok == False:
            return redirect(url_for("admin_login"))

    if "mensajeerror" in session:
        outputhtml = managerlogica.generarmensajeerror(session["mensajeerror"])
        session.pop("mensajeerror")

        return jsonify({"data": outputhtml, "errores": session["mensajeerror"]})

    if "datos_vivienda" in session:
        datos_vivienda = session.pop("datos_vivienda")
        return render_template("modificar_piso_admin.html", datos_vivienda=datos_vivienda)

    return redirect(url_for("menu_admin"))


@app.route("/profile/item", methods=["post"])
def ver_piso_para_modificar():
    if "usuario" not in session or "password" not in session:
        return redirect(url_for("admin_login"))
    else:
        ok = managermongo.comprobar_existencia_usuario(session["usuario"], session["password"])
        if ok == False:
            return redirect(url_for("admin_login"))

    if "iditem" in request.form:
        datos = managermongo.get_vivienda_porid(request.form["iditem"])
        session["datos_vivienda"] = datos

    return redirect(url_for("ver_piso_para_modificar_get"))


# quizas hacer con websockets?
@app.route("/profile/item_modificado", methods=["post"])
def modificar_vivienda():
    if "usuario" not in session or "password" not in session:
        return redirect(url_for("admin_login"))
    else:
        ok = managermongo.comprobar_existencia_usuario(session["usuario"], session["password"])
        if ok == False:
            return redirect(url_for("admin_login"))

    if "iditem" and "calle" and "cp" and "habitaciones" and "localidad" \
            and "banos" and "tipocasa" and "numero" and "dueno" and "telefonodueno" in request.form:

        # comprobacion de si el iditem existe en la db
        ok, datosmongo = managerlogica.comprobarexiste_iditem(request.form["iditem"])
        if ok == errores.existe:

            actualizado = managerlogica.actualizar_vivienda(request.form, app.config["CARPETA_SUBIDAS"],
                                                            app.config["MAX_CONTENT_LENGTH"], datosmongo["nombrefile"])
            session["mensajeerror"] = actualizado
        else:
            # alerta
            # todo: mostrar mensaje de error
            session["mensajeerror"] = ok
        return redirect(url_for("ver_piso_para_modificar_get"))

    return redirect(url_for("menu_admin"))


@app.route("/profile/tomar_medidas_pago", methods=["GET"])
def tomar_medidas_pago():
    return render_template("tomar_medidas_pago.html")


@app.route("/profile/tomar_medidas", methods=["GET"])
def tomar_medidas_light():
    return render_template("tomar_medidas_light.html")


@app.route("/profile/recibir_menu_medicion", methods=["POST"])
def recibir_menu_medicion():
    if "sin" in request.form:
        listado = managermongo.get_sin_mediciones()
        session["listado_viviendas"] = listado
        return redirect(url_for("menu_admin"))
    elif "con" in request.form:
        listado = managermongo.get_con_mediciones()
        session["listado_viviendas"] = listado
        return redirect(url_for("menu_admin"))

    return render_template("listado_sin_mediciones.html")


##################################

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    env_port = int(os.environ.get("PORT", 5000))
    env_debug = os.environ.get("FLASK_DEBUG", 1)

    socketio.run(host="0.0.0.0", port=env_port, app=app, debug=env_debug)

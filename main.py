from datetime import datetime

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import request

# nos permite servir archivos de forma estatico o absoluta
from flask import send_from_directory

from ModuloMongodb.ManagerMongodb import managermongo
from flask_bootstrap import Bootstrap
from ModuloHelper.ManagerHelper import ManagerHelper
from ModuloWeb.ManagerWeb import ManagerWeb
from flask_socketio import SocketIO
from flask_socketio import emit
import eventlet

app = Flask(__name__)
app.secret_key = "holaa"
socketio = SocketIO(app)
# eventlet.monkey_patch(thread=False)


# MUCHO CUIDADO EN NO PISAR LAS VARIABLES YA CREADAS
# app.config["DEBUG"] = True
managerweb = ManagerWeb()

import os

# recuperar una ruta absoluta
CARPETA = os.path.abspath(".//archivos_subidos")
app.config["CARPETA"] = CARPETA

bootstrap = Bootstrap(app)
helper = ManagerHelper()


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
        print("APP CONFIG CARPETA {0}".format(app.config["CARPETA"]),
              os.path.join(app.config["CARPETA"], nombre_archivo))
        f.save(os.path.join(app.config["CARPETA"]), nombre_archivo)
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
        ok = managermongo.comprobaradmin(session["usuario"], session["password"])
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
    if "anterior_calle" in session:
        anterior_calle = session.pop("anterior_calle")
        anterior_numero = session.pop("anterior_numero")

        return render_template("alta_piso.html", anterior_calle=anterior_calle, anterior_numero=anterior_numero)

    if "obtener_calle" in session:
        session.pop("obtener_calle")
        calle = session.pop("calle")
        numero = session.pop("numero")
        cp = session.pop("cp")
        localidad = session.pop("localidad")
        return render_template("alta_piso.html",
                               calle=calle,
                               numero=numero,
                               cp=cp,
                               localidad=localidad)

    if "calle" and "alquiler" and "cp" and "habitaciones" and "localidad" and "numerobanos" \
            and "template" and "tipocasa" and "zonas" and "latitude_gps" and "longitude_gps" and "dueno" and "precio" and "totalmetros" \
            in session:
        calle = session.pop("calle")
        alquiler = session.pop("alquiler")
        cp = session.pop("cp")
        habitaciones = session.pop("habitaciones")
        localidad = session.pop("localidad")
        numero = session.pop("numero")
        numerobanos = session.pop("numerobanos")
        template = session.pop("template")
        tipocasa = session.pop("tipocasa")
        zonas = session.pop("zonas")
        latitude_gps = session.pop("latitude_gps")
        longitude_gps = session.pop("longitude_gps")
        dueno = session.pop("dueno")
        precio = session.pop("precio")
        totalmetros = session.pop("totalmetros")

        return render_template("alta_piso.html",
                               calle=calle,
                               aquiler=alquiler,
                               cp=cp,
                               habitaciones=habitaciones,
                               localidad=localidad,
                               numero=numero,
                               numerobanos=numerobanos,
                               template=template,
                               tipocasa=tipocasa,
                               zonas=zonas,
                               latitude_gps=latitude_gps,
                               longitude_gps=longitude_gps,
                               dueno=dueno,
                               precio=precio,
                               totalmetros=totalmetros

                               )

    if "mensajeerror" in session:
        session.pop("mensajeerror")

    return render_template("alta_piso.html")


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
    # if "obtener_calle" in request.form: session["obtener_calle"] = True calle, numero, cp, localidad =
    # managerweb.getstreet(request.form["latitude_gps"], request.form["longitude_gps"]) session["calle"] = calle
    # session["numero"] = numero session["cp"] = cp session["localidad"] = localidad
    #
    #     return redirect(url_for("alta_piso"))

    if "usuario" not in session or "password" not in session:
        return redirect(url_for("alta_piso"))

    if "tiponegocio" and "calle" and "cp" and "habitaciones" and "localidad" \
            and "banos" and "tipocasa" and "numero" and "dueno" and "telefonodueno" in request.form:

        # comprobacion de si ya existe el piso en la db
        ok = managermongo.comprobarexisteinmueble(
            request.form["calle"],
            # request.form["latitude_gps"],
            # request.form["longitude_gps"],
            request.form["numero"]
        )
        if ok == True:
            ok = managermongo.altaproducto(
                request.form["calle"],
                request.form["cp"],
                request.form["habitaciones"],
                request.form["localidad"],
                request.form["numero"],
                request.form["banos"],
                request.form["wasap"],
                request.form["tipocasa"],
                request.form["telefonodueno"],
                request.form["calledueno"],
                request.form["numerodueno"],
                request.form["tiponegocio"],
                request.form["latitude_gps"],
                request.form["longitude_gps"],
                request.form["dueno"],
                request.form["precioventa"],
                request.form["precioalquiler"],
                request.form["totalmetros"],
                request.form["nombre"],
                request.form["precision"]

            )

            if ok == True:
                session["mensajeerror"] = helper.errores.insertado_correctamente
                session["anterior_calle"] = request.form["calle"]
                session["anterior_numero"] = request.form["numero"]
            else:
                session["mensajeerror"] = helper.errores.no_insertado
        else:
            # ya existe mensaje de error
            session["mensajeerror"] = helper.errores.no_insertado
            session["calle"] = request.form["calle"]
            session["alquiler"] = request.form["alquiler"]
            session["cp"] = request.form["cp"]
            session["habitaciones"] = request.form["habitaciones"]
            session["localidad"] = request.form["localidad"]
            session["numero"] = request.form["numero"]
            session["numerobanos"] = request.form["numerobanos"]
            session["template"] = request.form["template"]
            session["tipocasa"] = request.form["tipocasa"]
            session["zonas"] = request.form["zonas"]
            session["latitude_gps"] = request.form["latitude_gps"]
            session["longitude_gps"] = request.form["longitude_gps"]
            session["dueno"] = request.form["dueno"]
            session["precio"] = request.form["precio"]
            session["totalmetros"] = request.form["totalmetros"]

    return redirect(url_for("alta_piso"))


@app.route("/profile/ver", methods=["GET"])
def ver_piso():
    return render_template("ver_piso.html")


@app.route("/profile/ver", methods=["GET"])
def buscar_piso():
    return render_template("buscar_piso.html")


@app.route("/profile/modificar", methods=["GET"])
def modificar_piso():
    return render_template("modificar_piso.html")


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
    socketio.run(host="0.0.0.0", port=5000, app=app, debug=True)
    # app.run("0.0.0.0", 5000, debug=True)

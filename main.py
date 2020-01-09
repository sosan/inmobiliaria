from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from ModuloMongodb.ManagerMongodb import managermongo
from flask_bootstrap import Bootstrap
from ModuloHelper.ManagerHelper import ManagerHelper

app = Flask(__name__)
app.secret_key = "holaa"

bootstrap = Bootstrap(app)
helper = ManagerHelper()


###################################

@app.route("/admin")
def admin_login():
    return render_template("login_admin.html")


@app.route("/admin", methods=["POST"])
def recibir_login():
    if "usuario" and "password" in request.form:

        ok = managermongo.comprobaradmin(request.form["usuario"], request.form["password"])
        if ok == True:
            session["usuario"] = request.form["usuario"]
            session["password"] = request.form["password"]
            return redirect(url_for("menu_admin"))

        else:
            pass

    return redirect(url_for("admin_login"))


@app.route("/profile", methods=["GET"])
def menu_admin():
    if "usuario" and "password" in session:
        ok = managermongo.comprobaradmin(session["usuario"], session["password"])
        if ok == True:
            return render_template("menu_admin.html")

    return redirect(url_for("admin_login"))


@app.route("/profile/alta", methods=["GET"])
def alta_piso():
    if "anterior_calle" and "anterior_numero" in session:
        anterior_calle = session.pop("anterior_calle")
        anterior_numero = session.pop("anterior_numero")

        return render_template("alta_piso.html", anterior_calle=anterior_calle, anterior_numero=anterior_numero)

    if "calle" and "alquiler" and "cp" and "habitaciones" and "localidad" and "numero" and "numerobanos" \
            and "template" and "tipocasa" and "zonas" and "x_gps" and "y_gps" and "dueno" and "precio" and "totalmetros" \
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
        x_gps = session.pop("x_gps")
        y_gps = session.pop("y_gps")
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
                               x_gps=x_gps,
                               y_gps=y_gps,
                               dueno=dueno,
                               precio=precio,
                               totalmetros=totalmetros

                               )

    if "mensajeerror" in session:
        session.pop("mensajeerror")

    return render_template("alta_piso.html")


@app.route("/profile/alta", methods=["POST"])
def recibir_alta_piso():
    if "alquiler" and "calle" and "cp" and "habitaciones" and "localidad" and "numero" \
            and "numerobanos" and "template" and "tipocasa" and "zonas" in request.form:

        # comprobacion de si ya existe el piso en la db
        ok = managermongo.comprobarexisteinmueble(
            request.form["calle"],
            request.form["numero"]
        )
        if ok == True:
            ok = managermongo.altaproducto(
                request.form["calle"],
                request.form["alquiler"],
                request.form["cp"],
                request.form["habitaciones"],
                request.form["localidad"],
                request.form["numero"],
                request.form["numerobanos"],
                request.form["template"],
                request.form["tipocasa"],
                request.form["zonas"],
                request.form["x_gps"],
                request.form["y_gps"],
                request.form["dueno"],
                request.form["precio"],
                request.form["totalmetros"]

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
            session["x_gps"] = request.form["x_gps"]
            session["y_gps"] = request.form["y_gps"]
            session["dueno"] = request.form["dueno"]
            session["precio"] = request.form["precio"]
            session["totalmetros"] = request.form["totalmetros"]

    return redirect(url_for("alta_piso"))


@app.route("/profile/ver", methods=["GET"])
def ver_piso():
    return render_template("ver_piso.html")


@app.route("/profile/modificar", methods=["GET"])
def modificar_piso():
    return render_template("modificar_piso.html")


@app.route("/profile/tomar_medidas_pago", methods=["GET"])
def tomar_medidas_pago():
    return render_template("tomar_medidas_pago.html")


@app.route("/profile/tomar_medidas", methods=["GET"])
def tomar_medidas_light():
    return render_template("tomar_medidas_light.html")


##################################

@app.route("/")
def home():
    return render_template("geo.html")

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
    
    if "mensajeerror" in session:
        session.pop("mensajerror")
    
    return render_template("alta_piso.html")


@app.route("/profile/alta", methods=["POST"])
def recibir_alta_piso():
    
    print("hola")
    if "alquiler" and "calle" and "cp" and "habitaciones" and "habitaciones_otro" and "localidad" and "numero" \
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
                request.form["habitaciones_otro"],
                request.form["localidad"],
                request.form["numero"],
                request.form["numerobanos"],
                request.form["template"],
                request.form["tipocasa"],
                request.form["zonas"],
                request.form["x_longitud_gps"],
                request.form["y_longitud_gps"],
                request.form["x_latitud_gps"],
                request.form["y_latitud_gps"],
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
        pass

    return redirect(url_for("alta_piso"))


@app.route("/profile/ver", methods=["GET"])
def ver_piso():
    return render_template("ver_piso.html")


@app.route("/profile/modificar", methods=["GET"])
def modificar_piso():
    return render_template("modificar_piso.html")


##################################

@app.route("/")
def home():
    return render_template("index.html")

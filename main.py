from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from ModuloMongodb.ManagerMongodb import mongocliente


app = Flask(__name__)
app.secret_key = "holaa"



###################################

@app.route("/admin")
def admin_login():
    
    return render_template("login_admin.html")

@app.route("/admin", methods=["POST"])
def recibir_login():
    
    if "usuario" and "password" in request.form:
        
        ok = mongocliente.comprobaradmin(request.form["usuario"], request.form["password"])
        if ok == True:
            session["usuario"] = request.form["usuario"]
            session["password"] = request.form["password"]
            return redirect(url_for("menu_admin"))
            
        else:
            pass
    
    return redirect(url_for("admin_login"))

@app.route("/profile", methods=["GET"])
def menu_admin():
    return render_template("menu_admin.html")


@app.route("/profile/alta", methods=["GET"])
def alta_piso():
    
    return render_template("alta_piso.html")
    

@app.route("/profile/alta", methods=["POST"])
def recibir_alta_piso():
    
    if "" in request.form:
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

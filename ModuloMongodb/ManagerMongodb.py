import locale
import uuid

from pymongo import MongoClient
from bson.objectid import ObjectId

from datetime import datetime
from datetime import timedelta
from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


class ManagerMongoDb:
    def __init__(self):

        self.MONGO_URL = "mongodb+srv://{0}:{1}@{2}"
        self.cliente: MongoClient = None
        self.db: Database = None
        self.cursorpisos: Collection = None
        self.cursoradmin: Collection = None

    def conectDB(self, usuario, password, host, db, coleccion):
        try:
            self.cliente = MongoClient(self.MONGO_URL.format(usuario, password, host), ssl_cert_reqs=False)
            self.db = self.cliente[db]
            self.cursorpisos = self.db[coleccion]
            self.cursoradmin = self.db["admin"]

        except ConnectionFailure:
            raise Exception("Servidor no disponible")

    def getid_autoincremental(self, idcontador, keyaumentar):
        id_autoincremental = self.cursoradmin.find_one_and_update(
            {"_id": idcontador},
            {"$inc": {keyaumentar: 1}},
            projection={"_id": False},
            upsert=True,
            return_document=ReturnDocument.AFTER

        )
        if id_autoincremental is None:
            return False

        return True, id_autoincremental["cantidadproductos"]

    def altaproducto(self,
                     calle,
                     cp,
                     habitaciones,
                     localidad,
                     numero,
                     banos,
                     wasap,
                     tipocasa,
                     telefonodueno,
                     calledueno,
                     numerodueno,
                     tiponegocio_alquiler,
                     tiponegocio_venta,
                     latitud_txt,
                     longitud_txt,
                     dueno,
                     precioventa,
                     precioalquiler,
                     totalmetros,
                     nombre,
                     precision_txt,
                     nombrefile
                     ):

        try:
            latitud = float(latitud_txt)
            longitud = float(longitud_txt)

            fecha = datetime.utcnow()
            fechadelta = datetime.utcnow() + timedelta(hours=24)

            ok = self.cursorpisos.insert_one(
                {
                    "calle": calle,
                    "tiponegocio_alquiler": tiponegocio_alquiler,
                    "tiponegocio_venta": tiponegocio_venta,
                    "cp": cp,
                    "habitaciones": habitaciones,
                    "precioventa": precioventa,
                    "precioalquiler": precioalquiler,
                    "localidad": localidad,
                    "numero": numero,
                    "banos": banos,
                    "wasap": wasap,
                    "tipocasa": tipocasa,
                    "telefonodueno": telefonodueno,
                    "calledueno": calledueno,
                    "numerodueno": numerodueno,
                    "dueno": dueno,
                    "totalmetros": totalmetros,
                    "medicion": False,
                    "nombre": nombre,
                    "nombrefile": nombrefile,
                    "fecha": fecha,
                    "fechadelta": fechadelta,
                    "datosgps": {
                        "coordenadas": [latitud, longitud],
                        "precision": precision_txt

                    }
                }
            )
            if ok.inserted_id != None:
                return True
            return False

        except ValueError:
            raise Exception("Conversion no posible")

    def comprobarexisteinmueble(self, calle, numero):

        try:
            # latitud = float(latitud_txt)
            # longitud = float(longitud_txt)
            patron = {"calle": calle, "numero": numero}
            ok = list(self.cursorpisos.find(patron))
            if ok != None:
                if len(ok) <= 0:
                    return True
            return False
        except ValueError:
            raise Exception("no podidod conversion {0} {1}".format(calle, numero))

    def getcantidadproductos(self):
        resultados = self.cursoradmin.find_one({"_id": "contador"}, {"_id": False})
        if resultados == None:
            return False
        return True, resultados["cantidadproductos"]

    def primeracomprobacionadmin(self, usuario, password):
        resultado = self.cursoradmin.find_one({"usuario": usuario, "password": password}, {"_id": False})
        if resultado != None:
            return True, resultado["nombre"]
        return False

    def comprobaradmin(self, usuario, password):
        resultado = self.cursoradmin.find_one({"usuario": usuario, "password": password}, {"_id": False})
        if resultado != None:
            if len(resultado) > 0:
                return True
        return False

    def getallproductos(self):
        resultados = list(self.cursorpisos.find({}))
        return resultados

    def get_sin_mediciones(self):
        resultados = list(self.cursorpisos.find({"medicion": False}, {"_id": False}))
        return resultados

    def updateproducto(self, fecha, idproducto, calle, alquiler, cp, habitaciones, precio, localidad, numero,
                       numerobanos,
                       template, tipocasa, zonas, dueno, totalmetros, medicion, latitud, longitud
                       ):

        ok = self.cursorpisos.update_one({"_id": ObjectId(idproducto)}, {"$set":
            {
                "calle": calle,
                "alquiler": alquiler,
                "cp": cp,
                "habitaciones": habitaciones,
                "precio": precio,
                "localidad": localidad,
                "numero": numero,
                "numerobanos": numerobanos,
                "template": template,
                "tipocasa": tipocasa,
                "zonas": zonas,
                "dueno": dueno,
                "totalmetros": totalmetros,
                "medicion": medicion,
                "datosgps": {
                    "coordenadas": [latitud, longitud]

                }

            }})
        if ok.modified_count == 1:
            return True
        return False

    def deleteproducto(self, idproducto):
        ok = self.cursorpisos.delete_one({"_id": ObjectId(idproducto)})
        if ok.deleted_count == 1:

            ok = self.cursoradmin.update_one(
                {"_id": "contador"},
                {"$inc": {"cantidadproductos": -1}}
            )
            if ok.modified_count == 1:
                return True
        return False


managermongo = ManagerMongoDb()
managermongo.conectDB("pepito", "pepito", "cluster0-6oq5a.gcp.mongodb.net/test?retryWrites=true&w=majority",
                      db="inmobiliaria", coleccion="pisos")

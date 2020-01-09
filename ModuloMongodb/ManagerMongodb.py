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
                     alquiler,
                     cp,
                     habitaciones,
                     localidad,
                     numero,
                     numerobanos,
                     template,
                     tipocasa,
                     zonas,
                     x_txt,
                     y_txt,
                     dueno,
                     precio,
                     totalmetros
                     ):

        try:
            x = float(x_txt)
            y = float(y_txt)

            ok = self.cursorpisos.insert_one(
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
                    "datosgps": {
                        "gps": [x, y],
                    }
                }
            )
            if ok.inserted_id != None:
                return True
            return False

        except ValueError:
            raise Exception("Conversion no posible")

    def comprobarexisteinmueble(self, calle, numero):
        ok = self.cursorpisos.find({"calle": calle, "numero": numero})
        if ok != None:
            return True
        return False

    def getcantidadproductos(self):
        resultados = self.cursoradmin.find_one({"_id": "contador"}, {"_id": False})
        if resultados == None:
            return False
        return True, resultados["cantidadproductos"]

    def comprobaradmin(self, usuario, password):
        resultado = self.cursoradmin.find_one({"usuario": usuario, "password": password}, {"_id": False})
        if resultado != None:
            return True
        return False

    def getallproductos(self):
        resultados = list(self.cursorpisos.find({}))
        return resultados

    def updateproducto(self, fecha, idproducto, nombreproducto, urlproducto, urlimagenproducto, h, v):

        ok = self.cursorpisos.update_one({"_id": ObjectId(idproducto)}, {"$set":
            {
                "fecha_mod": fecha,
                "nombreproducto": nombreproducto,
                "urlproducto": urlproducto,
                "urlimagenproducto": urlimagenproducto,
                "h": h,
                "v": v

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

import base64
import os
import sys
from datetime import datetime
from werkzeug.utils import secure_filename
import math

from ModuloMongodb.ManagerMongodb import managermongo
from ModuloHelper.ManagerHelper import Errores


class ManagerLogica:
    def __init__(self):
        self.errores = Errores()

    def manejodatosvivienda(self):
        pass

    def comprobarexiste_iditem(self, iditem):
        resultado = managermongo.comprobarexiste_iditem(iditem)
        if resultado == 1:
            datos = managermongo.get_vivienda_porid(iditem)
            return self.errores.existe, datos
        elif resultado > 1:
            return self.errores.duplicado, None
            # raise Exception("id item con mas de 2 documentos {0} ".format(iditem))
        elif resultado <= 0:
            return self.errores.noexiste, None

    def actualizar_vivienda(self, formulario: dict, carpeta_subidas, max_content_length, datosmongo: list):
        try:
            length_files = int(formulario["files_len"])
            longitud_file_ya_existe = int(formulario["longitud_file_ya_existe"])
            habitaciones = int(formulario["habitaciones"])
            banyos = int(formulario["banos"])
            precioventa = int(formulario["precioventa"])
            precioalquiler = int(formulario["precioalquiler"])
            totalmetros = int(formulario["totalmetros"])

        except ValueError:
            raise Exception("no podido convertir")

        datosarchivos = []
        # procesar los archivos antiguos
        for i in range(0, longitud_file_ya_existe):
            if "file_ya_existe_{0}_nombrefile".format(i) in formulario:
                for o in range(0, length_files):
                    if (formulario["file_ya_existe_{0}_nombrefile".format(i)] == datosmongo[o]["nombrefile"]) and \
                            (formulario["file_ya_existe_{0}_nombrefile_fromform".format(i)] == datosmongo[o][
                                "nombrefile_from_form"]) and \
                            (formulario["file_ya_existe_{0}_tamano".format(i)] == datosmongo[o]["tamano_str"]):
                        datosarchivos.append(
                            {
                                "nombrefile": datosmongo[o]["nombrefile"],
                                "nombrefile_fromform": datosmongo[o]["nombrefile_from_form"],
                                "tamano": datosmongo[o]["tamano_str"]
                            })

        for i in range(0, length_files):
            if "files_{0}_datafile".format(i) in formulario:
                datafile_b64 = formulario["files_{0}_datafile".format(i)]

                if sys.getsizeof(datafile_b64) > max_content_length:
                    continue

                nombrefile_from_form = secure_filename(formulario["files_{0}_filename".format(i)])

                if datafile_b64 == "" or nombrefile_from_form == "":
                    raise Exception("campo vacio {0}".format(nombrefile_from_form))

                nombrefile = datetime.utcnow().strftime("%d-%b-%Y-%H.%M.%S.%f_") + nombrefile_from_form

                tamanoarchivo_bytes = sys.getsizeof(datafile_b64)

                sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
                lent = math.floor(math.log(tamanoarchivo_bytes) / math.log(1024))
                tamano_str = "{0} {1}".format(round(tamanoarchivo_bytes / math.pow(1024, lent), 2), sizes[lent])

                datosarchivos.append(
                    {
                        "nombrefile": nombrefile,
                        "nombrefile_fromform": nombrefile_from_form,
                        "tamano": tamano_str
                    })

                print(os.path.join(carpeta_subidas, nombrefile))
                with open(os.path.join(carpeta_subidas, nombrefile), "wb") as arch:
                    cad_cero = datafile_b64.find(',')
                    imagen_data64 = datafile_b64[cad_cero + 1:]
                    arch.write(base64.decodebytes(imagen_data64.encode()))
                    arch.close()

        tiponegocio_alquiler = False
        tiponegocio_venta = False
        if "tiponegocio_alquiler" in formulario:
            tiponegocio_alquiler = True

        if "tiponegocio_venta" in formulario:
            tiponegocio_venta = True

        ok = managermongo.actualizacion_producto(
            formulario["calle"],
            formulario["cp"],
            habitaciones,
            formulario["localidad"],
            formulario["numero"],
            banyos,
            formulario["wasap"],
            formulario["tipocasa"],
            formulario["telefonodueno"],
            formulario["calledueno"],
            formulario["numerodueno"],
            tiponegocio_alquiler,
            tiponegocio_venta,
            formulario["latitude_gps"],
            formulario["longitude_gps"],
            formulario["dueno"],
            precioventa,
            precioalquiler,
            totalmetros,
            formulario["usuario_que_modifica"],
            formulario["precision"],
            datosarchivos,
            formulario["iditem"]

        )

        return ok

    def generarmensajeerror(self, mensajeerror):
        if mensajeerror == self.errores.no_actualizado:
            return "NO ACTUALIZADO"
        elif mensajeerror == self.errores.duplicado:
            return "EXISTENCIA DE DOS VIVIENDAS IGUALES"
        elif mensajeerror == self.errores.actualizado_correctamente:
            return "ACTUALIZADO CORRECTAMENTE"
        else:
            return "PROBLEMA GENERAL"

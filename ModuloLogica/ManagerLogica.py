import base64
import os
import math
import sys

from ModuloMongodb.ManagerMongodb import managermongo
from datetime import datetime
from werkzeug.utils import secure_filename
import math


class ManagerLogica:

    def manejodatosvivienda(self):
        pass

    def actualizarvivienda(self, formulario, carpeta_subidas, max_content_length):
        try:
            length_files = int(formulario["files_len"])
            habitaciones = int(formulario["habitaciones"])
            banyos = int(formulario["banos"])
            precioventa = int(formulario["precioventa"])
            precioalquiler = int(formulario["precioalquiler"])
            totalmetros = int(formulario["totalmetros"])

        except ValueError:
            raise Exception("no podido convertir")

        datosarchivos = []
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
            formulario["nombre"],
            formulario["precision"],
            datosarchivos

        )

        if ok == True:
            pass
        else:
            pass
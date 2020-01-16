import subprocess
from json import JSONDecodeError

from requests_html import HTMLSession
from datetime import datetime
import json


class ManagerWeb:
    def __init__(self):
        self.web = HTMLSession()

    def getstreet(self, x, y):
        uri = """https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=k-EckgQuyQOTGQoMy54SsslKuX9oMP8PFj2SyV-_wJM&mode=retrieveAddresses&prox={0},{1}&maxresults=1""".format(x, y)

        resultado = self.web.get(uri)
        if resultado != None:
            temp = json.loads(resultado.text)
            fulldireccion = temp["Response"]["View"][0]["Result"][0]["Location"]["Address"]["Label"]

            splitdire = fulldireccion.split(" ")
            if len(splitdire) == 5:  # sin nombre de la calle
                # ['07001', 'Palma', '(Illes', 'Balears),', 'Espanya']
                return "Ninguna", "Ninguna", splitdire[0], splitdire[1]  # calle= None, numero=None, cp, ciudad
            else:
                return None, None, splitdire[0], splitdire[1]  # calle= None, numero=None, cp, ciudad

        return None
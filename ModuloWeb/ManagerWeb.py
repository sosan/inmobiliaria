import subprocess
from json import JSONDecodeError

from requests_html import HTMLSession
from datetime import datetime
import json

class ManagerWeb:
    def __init__(self):
        self.web = HTMLSession()

    def getstreet(self, x, y):
        uri = """
               https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=k-EckgQuyQOTGQoMy54SsslKuX9oMP8PFj2SyV-_wJM
               &mode=retrieveAddresses
               &prox={0},{1}
               &maxresults=1
               """.format(x, y)

        resultado = self.web.get(uri)
        return resultado


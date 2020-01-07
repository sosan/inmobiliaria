from pymongo import MongoClient()


class ManagerMongodb:
    
    def __init__(self):
        self.cliente: MongoClient = None
        self.conexion = None
        self.coleccion_admin = None
        
    def conectardb(self, host, usuario, password):
        self.cliente = MongoClient(host=host, usuario=usuario, password=password)
        self.conexion = self.cliente.
        self.coleccion_admin = self.conexion.
        
mongocliente = ManagerMongodb()
mongocliente.conectardb("")
        
class Errores():
    def __init__(self):
        self.insertado_correctamente = 1
        self.no_insertado = 2


class ManagerHelper:
    def __init__(self):
        self.errores = Errores()
        
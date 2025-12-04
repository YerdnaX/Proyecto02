from pymongo import MongoClient

class ClaseMONGO:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["AgroMon"]

    # ========== LECTURAS ==========
    def insertarLectura(self, lectura):
        self.db.Lecturas.insert_one(lectura.transformarDiccionario())

    def obtenerLecturas(self):
        return list(self.db.Lecturas.find({}))

    # ========== ALERTAS ==========
    def insertarAlerta(self, alerta):
        self.db.Alertas.insert_one(alerta.transformarDiccionario())

    def obtenerAlertas(self):
        return list(self.db.Alertas.find({}))

    def eliminarLecturasPorParcelaYFecha(self, idParcela, fecha):
        resultado = self.db.Lecturas.delete_many(
            {"idParcela": idParcela, "fechaHora": {"$regex": f"^{fecha}"}}
        )
        return resultado.deleted_count

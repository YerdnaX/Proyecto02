import pyodbc
from datetime import datetime


class ClaseSQL:
    def __init__(self):
        self.conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=AgroMon;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        self.cursor = self.conexion.cursor()

    # ========== PARCELAS ===========
    def insertarParcela(self, parcela):
        self.cursor.execute(
            """
            INSERT INTO Parcelas VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                parcela.idParcela,
                parcela.nombre,
                parcela.ubicacion,
                parcela.tipoCultivo,
                parcela.area,
                parcela.profundidadRaiz,
                parcela.eficienciaRiego,
                parcela.umbralHumedadMin,
                parcela.umbralHumedadMax,
                parcela.volumenDeseado,
            ),
        )
        self.conexion.commit()

    def obtenerParcelas(self):
        self.cursor.execute("SELECT * FROM Parcelas")
        return self.cursor.fetchall()

    def actualizarParcela(self, parcela):
        self.cursor.execute(
            """
            UPDATE Parcelas SET
            nombre=?, ubicacion=?, tipoCultivo=?, area=?, profundidadRaiz=?,
            eficienciaRiego=?, umbralHumedadMin=?, umbralHumedadMax=?, volumenDeseado=?
            WHERE idParcela=?
            """,
            (
                parcela.nombre,
                parcela.ubicacion,
                parcela.tipoCultivo,
                parcela.area,
                parcela.profundidadRaiz,
                parcela.eficienciaRiego,
                parcela.umbralHumedadMin,
                parcela.umbralHumedadMax,
                parcela.volumenDeseado,
                parcela.idParcela,
            ),
        )
        self.conexion.commit()

    def eliminarParcela(self, idParcela):
        self.cursor.execute("DELETE FROM Parcelas WHERE idParcela=?", idParcela)
        self.conexion.commit()

    # ========== SENSORES ===========
    def insertarSensor(self, sensor):
        self.cursor.execute(
            """
            INSERT INTO Sensores VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sensor.idSensor,
                sensor.tipo,
                sensor.idParcela,
                sensor.estado,
                sensor.ubicacionParcela,
                sensor.unidadMedida,
                sensor.rangoValido,
            ),
        )
        self.conexion.commit()

    def obtenerSensores(self):
        self.cursor.execute("SELECT * FROM Sensores")
        return self.cursor.fetchall()

    def actualizarSensor(self, sensor):
        self.cursor.execute(
            """
            UPDATE Sensores
            SET tipo=?, idParcela=?, estado=?, ubicacionParcela=?,
            unidadMedida=?, rangoValido=?
            WHERE idSensor=?
            """,
            (
                sensor.tipo,
                sensor.idParcela,
                sensor.estado,
                sensor.ubicacionParcela,
                sensor.unidadMedida,
                sensor.rangoValido,
                sensor.idSensor,
            ),
        )
        self.conexion.commit()

    def eliminarSensor(self, idSensor):
        self.cursor.execute("DELETE FROM Sensores WHERE idSensor=?", idSensor)
        self.conexion.commit()

    # ========== CALCULO RIEGO ===========
    def insertarCalculoRiego(self, calculo):
        fecha_valor = calculo["fecha"]
        try:
            fecha_dt = datetime.strptime(fecha_valor, "%d-%m-%Y")
        except ValueError:
            fecha_dt = datetime.strptime(fecha_valor, "%d-%m-%Y %H:%M:%S")
        self.cursor.execute(
            """
            INSERT INTO CalculoVolumenRiego (idParcela, fecha, volumenRiego)
            VALUES (?, ?, ?)
            """,
            (
                calculo["idParcela"],
                fecha_dt,
                calculo["volumenRiego"],
            ),
        )
        self.conexion.commit()

    def obtenerCalculosRiego(self):
        self.cursor.execute("SELECT * FROM CalculoVolumenRiego")
        return self.cursor.fetchall()

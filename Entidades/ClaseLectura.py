class ClaseLectura:
    def __init__(self, idLectura, idSensor, idParcela, fechaHora, valorMedido):
        self.__idLectura = idLectura
        self.__idSensor = idSensor
        self.__idParcela = idParcela
        self.__fechaHora = fechaHora
        self.__valorMedido = valorMedido
        
## Getters and Setters para cada atributo

    @property
    def idLectura(self):
        return self.__idLectura
    
    @idLectura.setter
    def idLectura(self, nuevoIdLectura):
        self.__idLectura = nuevoIdLectura

    @property
    def idSensor(self):
        return self.__idSensor
    
    @idSensor.setter
    def idSensor(self, nuevoIdSensor):
        self.__idSensor = nuevoIdSensor
    
    @property
    def idParcela(self):
        return self.__idParcela
    
    @idParcela.setter
    def idParcela(self, nuevoIdParcela):
        self.__idParcela = nuevoIdParcela

    @property
    def fechaHora(self):
        return self.__fechaHora
    
    @fechaHora.setter
    def fechaHora(self, nuevaFechaHora):
        self.__fechaHora = nuevaFechaHora
    
    @property
    def valorMedido(self):
        return self.__valorMedido
    
    @valorMedido.setter
    def valorMedido(self, nuevoValorMedido):
        self.__valorMedido = nuevoValorMedido

## string para imprimir la informacion
    def __str__(self):
        return "ID Lectura: {}  ID Sensor: {}  ID Parcela: {}  Fecha y Hora: {}  Valor Medido: {}".format(self.__idLectura, self.__idSensor, self.__idParcela, self.__fechaHora, self.__valorMedido)


    def crearDesdeDiccionario(diccionario):
        return ClaseLectura(
            diccionario["idLectura"],
            diccionario["idSensor"],
            diccionario["idParcela"],
            diccionario["fechaHora"],
            diccionario["valorMedido"]
        )
    
    def transformarDiccionario(self):
        return {
            "idLectura": self.__idLectura,
            "idSensor": self.__idSensor,
            "idParcela": self.__idParcela,
            "fechaHora": self.__fechaHora,
            "valorMedido": self.__valorMedido
        }
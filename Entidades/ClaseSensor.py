class ClaseSensor:
    def __init__(self, idSensor, tipo, idParcela, estado, ubicacionParcela, unidadMedida, rangoValido):
        self.__idSensor = idSensor
        self.__tipo = tipo
        self.__idParcela = idParcela
        self.__estado = estado
        self.__ubicacionParcela = ubicacionParcela
        self.__unidadMedida = unidadMedida
        self.__rangoValido = rangoValido
    
## Getters and Setters para cada atributo

    @property
    def idSensor(self):
        return self.__idSensor 
    
    @idSensor.setter
    def idSensor(self, nuevoIdSensor):
        self.__idSensor = nuevoIdSensor
    
    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, nuevoTipo):
        self.__tipo = nuevoTipo
    
    @property
    def idParcela(self):
        return self.__idParcela
    
    @idParcela.setter
    def idParcela(self, nuevoIdParcela):
        self.__idParcela = nuevoIdParcela

    @property
    def estado(self):  
        return self.__estado
    
    @estado.setter
    def estado(self, nuevoEstado):
        self.__estado = nuevoEstado

    @property
    def ubicacionParcela(self):
        return self.__ubicacionParcela
    
    @ubicacionParcela.setter
    def ubicacionParcela(self, nuevaUbicacion):
        self.__ubicacionParcela = nuevaUbicacion

    @property
    def unidadMedida(self):
        return self.__unidadMedida
    
    @unidadMedida.setter
    def unidadMedida(self, nuevaUnidad):
        self.__unidadMedida = nuevaUnidad

    @property
    def rangoValido(self):
        return self.__rangoValido
    
    @rangoValido.setter
    def rangoValido(self, nuevoRango):
        self.__rangoValido = nuevoRango

 ## string para imprimir la informacion del sensor   
    def __str__(self):
        return "ID Sensor: {}  Tipo: {}  ID Parcela: {}  Estado: {}  Ubicacion en Parcela: {}  Unidad de Medida: {}  Rango Valido: {}".format(self.__idSensor, self.__tipo, self.__idParcela, self.__estado, self.__ubicacionParcela, self.__unidadMedida, self.__rangoValido)
    
    def transformarDiccionario(self) -> dict:
        return {
            "idSensor": self.__idSensor,
            "tipo": self.__tipo,
            "idParcela": self.__idParcela,
            "estado": self.__estado,
            "ubicacionParcela": self.__ubicacionParcela,
            "unidadMedida": self.__unidadMedida,
            "rangoValido": self.__rangoValido
        }
    
    def crearDesdeDiccionario(diccionario: dict):
        return ClaseSensor(
            diccionario["idSensor"],
            diccionario["tipo"],
            diccionario["idParcela"],
            diccionario["estado"],
            diccionario["ubicacionParcela"],
            diccionario["unidadMedida"],
            diccionario["rangoValido"]
        )
class ClaseAlerta:
    def __init__(self, idParcela, idSensor, tipo, fechaGeneracion, valorDetectado, mensajeAlerta):
        self.__idParcela = idParcela
        self.__idSensor = idSensor
        self.__tipo = tipo 
        self.__fechaGeneracion = fechaGeneracion
        self.__valorDetectado = valorDetectado
        self.__mensajeAlerta = mensajeAlerta

## Getters and Setters para cada atributo

    @property
    def idParcela(self):
        return self.__idParcela
    
    @idParcela.setter
    def idParcela(self, nuevoIdParcela):
        self.__idParcela = nuevoIdParcela

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
    def fechaGeneracion(self):
        return self.__fechaGeneracion
    
    @fechaGeneracion.setter
    def fechaGeneracion(self, nuevaFecha):
        self.__fechaGeneracion = nuevaFecha

    @property
    def valorDetectado(self):
        return self.__valorDetectado
    
    @valorDetectado.setter
    def valorDetectado(self, nuevoValor):
        self.__valorDetectado = nuevoValor

    @property
    def mensajeAlerta(self):
        return self.__mensajeAlerta
    
    @mensajeAlerta.setter
    def mensajeAlerta(self, nuevoMensaje):
        self.__mensajeAlerta = nuevoMensaje
    
## string para imprimir la informacion
    def __str__(self):
        return f"Alerta - Parcela ID: {self.__idParcela}, Sensor ID: {self.__idSensor}, Tipo: {self.__tipo}, Fecha Generacion: {self.__fechaGeneracion}, Valor Detectado: {self.__valorDetectado}, Mensaje Alerta: {self.__mensajeAlerta}"
    
    def transformarDiccionario(self):
        return {
            "idParcela": self.__idParcela,
            "idSensor": self.__idSensor,
            "tipo": self.__tipo,
            "fechaGeneracion": self.__fechaGeneracion,
            "valorDetectado": self.__valorDetectado,
            "mensajeAlerta": self.__mensajeAlerta
        }
    

    def crearDesdeDiccionario(data): 
        return ClaseAlerta(
            data["idParcela"],
            data["idSensor"],
            data["tipo"],
            data["fechaGeneracion"],
            data["valorDetectado"],
            data["mensajeAlerta"]
        )
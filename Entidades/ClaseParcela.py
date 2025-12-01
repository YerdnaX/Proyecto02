class ClaseParcela:
    def __init__(self, idParcela, nombre, ubicacion, tipoCultivo, area, profundidadRaiz, eficienciaRiego, umbralHumedadMin, umbralHumedadMax, volumenDeseado):
        self.__idParcela = idParcela
        self.__nombre = nombre
        self.__ubicacion = ubicacion
        self.__tipoCultivo = tipoCultivo
        self.__area = area
        self.__profundidadRaiz = profundidadRaiz
        self.__eficienciaRiego = eficienciaRiego
        self.__umbralHumedadMin = umbralHumedadMin
        self.__umbralHumedadMax = umbralHumedadMax
        self.__volumenDeseado = volumenDeseado

## Getters and Setters para cada atributo

    @property
    def idParcela(self):
        return self.__idParcela

    @idParcela.setter
    def idParcela(self, nuevoIdParcela):
        self.__idParcela = nuevoIdParcela

    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevoNombre):
        self.__nombre = nuevoNombre

    @property
    def ubicacion(self):
        return self.__ubicacion
    
    @ubicacion.setter
    def ubicacion(self, nuevaUbicacion):
        self.__ubicacion = nuevaUbicacion

    @property
    def tipoCultivo(self):
        return self.__tipoCultivo   
    
    @tipoCultivo.setter
    def tipoCultivo(self, nuevoTipoCultivo):
        self.__tipoCultivo = nuevoTipoCultivo

    @property
    def area(self):
        return self.__area
    
    @area.setter
    def area(self, nuevaArea):
        self.__area = nuevaArea

    @property
    def profundidadRaiz(self):
        return self.__profundidadRaiz
    
    @profundidadRaiz.setter
    def profundidadRaiz(self, nuevaProfundidad):
        self.__profundidadRaiz = nuevaProfundidad   

    @property
    def eficienciaRiego(self):
        return self.__eficienciaRiego      
    
    @eficienciaRiego.setter
    def eficienciaRiego(self, nuevaEficiencia):
        self.__eficienciaRiego = nuevaEficiencia

    @property
    def umbralHumedadMin(self):
        return self.__umbralHumedadMin
    
    @umbralHumedadMin.setter
    def umbralHumedadMin(self, nuevoUmbralMin):
        self.__umbralHumedadMin = nuevoUmbralMin
    
    @property
    def umbralHumedadMax(self):
        return self.__umbralHumedadMax     
    
    @umbralHumedadMax.setter
    def umbralHumedadMax(self, nuevoUmbralMax):
        self.__umbralHumedadMax = nuevoUmbralMax    

    @property
    def volumenDeseado(self):
        return self.__volumenDeseado
    
    @volumenDeseado.setter
    def volumenDeseado(self, nuevoVolumen):
        self.__volumenDeseado = nuevoVolumen

## string para imprimir la informacion
    def __str__(self):
        return "ID Parcela: {}  Nombre: {}  Ubicacion: {}  Tipo de Cultivo: {}  Area: {}  Profundidad de Raiz: {}  Eficiencia de Riego: {}  Umbral de Humedad Minimo: {}  Umbral de Humedad Maximo: {}  Volumen Deseado: {}".format(self.__idParcela, self.__nombre, self.__ubicacion, self.__tipoCultivo, self.__area, self.__profundidadRaiz, self.__eficienciaRiego, self.__umbralHumedadMin, self.__umbralHumedadMax, self.__volumenDeseado)
    
    def transformarDiccionario(self):
        return {
            "idParcela": self.__idParcela,
            "nombre": self.__nombre,
            "ubicacion": self.__ubicacion,
            "tipoCultivo": self.__tipoCultivo,
            "area": self.__area,
            "profundidadRaiz": self.__profundidadRaiz,
            "eficienciaRiego": self.__eficienciaRiego,
            "umbralHumedadMin": self.__umbralHumedadMin,
            "umbralHumedadMax": self.__umbralHumedadMax,
            "volumenDeseado": self.__volumenDeseado
        }
    
    def crearDesdeDiccionario(diccionario):
        return ClaseParcela(
            diccionario["idParcela"],
            diccionario["nombre"],
            diccionario["ubicacion"],
            diccionario["tipoCultivo"],
            diccionario["area"],
            diccionario["profundidadRaiz"],
            diccionario["eficienciaRiego"],
            diccionario["umbralHumedadMin"],
            diccionario["umbralHumedadMax"],
            diccionario["volumenDeseado"]
        )
    
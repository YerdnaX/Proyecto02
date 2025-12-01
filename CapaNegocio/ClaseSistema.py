import Entidades.ClaseParcela as Parcela
import Entidades.ClaseSensor as Sensor
import Entidades.ClaseLectura as Lectura
import Entidades.ClaseAlerta as Alertas
from CapaNegocio.ClaseValidaciones import ClaseValidaciones
from CapaDatos.ClaseSQL import ClaseSQL
from CapaDatos.ClaseMONGO import ClaseMONGO

sql_db = ClaseSQL()
mongo_db = ClaseMONGO()

# Listas en memoria para operar con los objetos actuales
ListaParcelas = []
ListaSensores = []
ListaLecturas = []
ListaAlertas = []
ListaCalculoVolumen = []


# ================== CARGA DE DATOS DESDE LAS BD ==================
def leerParcelasJson():
    """Carga parcelas desde SQL Server."""
    ListaParcelas.clear()
    for row in sql_db.obtenerParcelas():
        parcela = Parcela.ClaseParcela(
            str(row[0]),
            row[1],
            row[2],
            row[3],
            str(row[4]),
            str(row[5]),
            str(row[6]),
            str(row[7]),
            str(row[8]),
            str(row[9]),
        )
        ListaParcelas.append(parcela)


def leerSensoresJson():
    """Carga sensores desde SQL Server."""
    ListaSensores.clear()
    for row in sql_db.obtenerSensores():
        sensor = Sensor.ClaseSensor(
            str(row[0]),
            row[1],
            str(row[2]),
            row[3],
            row[4],
            row[5],
            row[6],
        )
        ListaSensores.append(sensor)


def leerLecturasJson():
    """Carga lecturas desde MongoDB."""
    ListaLecturas.clear()
    for doc in mongo_db.obtenerLecturas():
        doc.pop("_id", None)
        lectura = Lectura.ClaseLectura.crearDesdeDiccionario(doc)
        ListaLecturas.append(lectura)


def leerAlertasJson():
    """Carga alertas desde MongoDB."""
    ListaAlertas.clear()
    for doc in mongo_db.obtenerAlertas():
        doc.pop("_id", None)
        alerta = Alertas.ClaseAlerta.crearDesdeDiccionario(doc)
        ListaAlertas.append(alerta)


def leerCalculoVolumenRiegoJson():
    """Carga cálculos de volumen de riego desde SQL Server."""
    ListaCalculoVolumen.clear()
    for row in sql_db.obtenerCalculosRiego():
        ListaCalculoVolumen.append(
            {"idParcela": str(row[0]), "fecha": row[1], "volumenRiego": float(row[2])}
        )


# ================== FUNCIONES DE PARCELAS ==================
def nuevaparcela():
    print("Creando una nueva parcela...")

    while True:
        idParcela = input("Ingrese el ID de la parcela: ")
        if ClaseValidaciones.esNumericoNoVacio(idParcela):
            if ClaseValidaciones.existeParcelaID(idParcela, ListaParcelas):
                print("El ID de la parcela ya existe. Ingrese un ID diferente.")
            else:
                break
        else:
            print("Ingrese un ID que sea un codigo de numeros enteros")

    while True:
        nombre = input("Ingrese el nombre de la parcela: ")
        if ClaseValidaciones.estaVacioString(nombre):
            break
        else:
            print("Ingrese un nombre adecuado")

    while True:
        ubicacion = input("Ingrese la ubicacion de la parcela: ")
        if ClaseValidaciones.estaVacioString(ubicacion):
            break
        else:
            print("Ingrese una ubicacion adecuado")

    while True:
        tipoCultivo = input("Ingrese el tipo de cultivo: ")
        if ClaseValidaciones.estaVacioString(tipoCultivo):
            break
        else:
            print("Ingrese un tipo de cultivo")

    while True:
        area = input("Ingrese el area de la parcela (en mA�): ")
        if ClaseValidaciones.esNumericoNoVacioFloat(area):
            break
        else:
            print("Ingrese un area en valores numericos")

    parcela = Parcela.ClaseParcela(
        idParcela, nombre, ubicacion, tipoCultivo, area, "", "", "", "", ""
    )
    sql_db.insertarParcela(parcela)
    leerParcelasJson()
    print("Parcela agregada exitosamente.")


def modificarParcela():
    idparcelamodificar = input("Ingrese el ID de la parcela que desea modificar: ")
    for parcela in ListaParcelas:
        if parcela.idParcela == idparcelamodificar:
            print("Parcela encontrada. Ingrese los nuevos datos:")

            while True:
                parcela.nombre = input("Ingrese el nuevo nombre de la parcela: ")
                if ClaseValidaciones.estaVacioString(parcela.nombre):
                    break
                else:
                    print("Ingrese un nombre adecuado")

            while True:
                parcela.ubicacion = input("Ingrese la nueva ubicacion de la parcela: ")
                if ClaseValidaciones.estaVacioString(parcela.ubicacion):
                    break
                else:
                    print("Ingrese una ubicacion adecuado")

            while True:
                parcela.tipoCultivo = input("Ingrese el nuevo tipo de cultivo: ")
                if ClaseValidaciones.estaVacioString(parcela.tipoCultivo):
                    break
                else:
                    print("Ingrese un tipo de cultivo")

            while True:
                area = input("Ingrese la area de la parcela (en mA�): ")
                if ClaseValidaciones.esNumericoNoVacioFloat(area):
                    parcela.area = float(area)
                    break
                else:
                    print("Ingrese un area en valores numericos")

            sql_db.actualizarParcela(parcela)
            leerParcelasJson()
            print("Parcela modificada exitosamente.")
            return
    print("Parcela no encontrada.")


def modificarDatosGeneralesParcela():
    idparcelamodificar = input("Ingrese el ID de la parcela que desea modificar: ")
    for parcela in ListaParcelas:
        if parcela.idParcela == idparcelamodificar:
            print("Parcela encontrada. Ingrese los nuevos datos:")

            while True:
                parcela.profundidadRaiz = input(
                    "Ingrese la nueva profundidad de la raiz (en cm): "
                )
                if ClaseValidaciones.esNumericoNoVacioFloat(parcela.profundidadRaiz):
                    break
                else:
                    print("Ingrese una profundidad de raiz en valores numericos")

            while True:
                parcela.eficienciaRiego = input(
                    "Ingrese la nueva eficiencia de riego (en %): "
                )
                if ClaseValidaciones.esNumericoNoVacioFloat(parcela.eficienciaRiego):
                    break
                else:
                    print("Ingrese una eficiencia de riego en valores numericos")

            while True:
                parcela.umbralHumedadMin = input(
                    "Ingrese el nuevo umbral de humedad minimo (en %): "
                )
                if ClaseValidaciones.esNumericoNoVacioFloat(parcela.umbralHumedadMin):
                    break
                else:
                    print("Ingrese un umbral de humedad minino en valores numericos")

            while True:
                parcela.umbralHumedadMax = input(
                    "Ingrese el nuevo umbral de humedad maximo (en %): "
                )
                if ClaseValidaciones.esNumericoNoVacioFloat(parcela.umbralHumedadMax):
                    if float(parcela.umbralHumedadMax) > float(
                        parcela.umbralHumedadMin
                    ):
                        break
                    else:
                        print(
                            "El umbral de humedad maximo debe ser mayor al umbral de humedad minimo"
                        )
                else:
                    print("Ingrese un umbral de humedad maximo en valores numericos")

            while True:
                parcela.volumenDeseado = input(
                    "Ingrese el nuevo volumen deseado de agua (en litros): "
                )
                if ClaseValidaciones.esNumericoNoVacioFloat(parcela.volumenDeseado):
                    break
                else:
                    print("Ingrese un volumen deseado en valores numericos")

            sql_db.actualizarParcela(parcela)
            leerParcelasJson()
            print("Parcela modificada exitosamente.")
            return
    print("Parcela no encontrada.")


def eliminarParcela():
    while True:
        idparcelaeliminar = input("Ingrese el ID de la parcela que desea modificar: ")
        if ClaseValidaciones.esNumericoNoVacio(idparcelaeliminar):
            break
        else:
            print("Ingrese un ID que sea un codigo de numeros enteros")

    sql_db.eliminarParcela(idparcelaeliminar)
    leerParcelasJson()
    print("Parcela eliminada exitosamente.")


def verParcelaPorID():
    while True:
        idparcelaver = input("Ingrese el ID de la parcela que desea ver: ")
        if ClaseValidaciones.esNumericoNoVacio(idparcelaver):
            break
        else:
            print("Ingrese un ID que sea un codigo de numeros enteros")
    for parcela in ListaParcelas:
        if parcela.idParcela == idparcelaver:
            print(parcela)
            return
    print("Parcela no encontrada.")


def verTodasLasParcelas():
    if not ListaParcelas:
        print("No hay parcelas registradas.")
        return
    for parcela in ListaParcelas:
        print(parcela)


# ================== FUNCIONES DE SENSORES ==================
def nuevoSensor():
    print("Creando una nuevo Sensor...")

    while True:
        idSensor = input("Ingrese el ID del sensor: ")
        if ClaseValidaciones.esNumericoNoVacio(idSensor):
            if ClaseValidaciones.existeSensorID(idSensor, ListaSensores):
                print("El ID del sensor ya existe. Ingrese un ID diferente.")
            else:
                break
        else:
            print("Ingrese un ID que sea un codigo de numeros enteros")

    while True:
        tipo = input(
            "Ingrese el tipo de sensor (HumedadSuelo/Temperatura/LLuvia(Humedad De La Hoja)):  "
        ).lower()
        if ClaseValidaciones.esValidoTipoSensor(tipo):
            break
        else:
            print("Ingrese un tipo de sensor adecuado")

    while True:
        idParcela = input("Ingrese el ID de la parcela asociada al sensor: ")
        if ClaseValidaciones.esNumericoNoVacio(idParcela):
            if ClaseValidaciones.existeParcelaID(idParcela, ListaParcelas):
                break
            else:
                print("El ID de la parcela no existe. Ingrese un ID valido.")
        else:
            print("Ingrese un ID que sea un codigo de numeros enteros")

    while True:
        estado = input(
            "Ingrese el estado del sensor (Activo/Inactivo/Mantenimiento o Revision): "
        ).lower()
        if ClaseValidaciones.esValidoEstadoSensor(estado):
            break
        else:
            print("Ingrese un estado valido: activo, inactivo, mantenimiento o revision")

    while True:
        ubicacionParcela = input("Ingrese la ubicacion del sensor en la parcela: ")
        if ClaseValidaciones.estaVacioString(ubicacionParcela):
            break
        else:
            print("Ingrese una ubicacion adecuada")

    while True:
        unidadMedida = input("Ingrese la unidad de medida del sensor: ")
        if ClaseValidaciones.estaVacioString(unidadMedida):
            break
        else:
            print("Ingrese una unidad de medida adecuada")

    while True:
        rangoValido = input(
            "Ingrese el rango valido de medicion del sensor(Formato: XX - XX): "
        )
        if ClaseValidaciones.esRangoSensorValido(rangoValido):
            break
        else:
            print("Ingrese un rango valido adecuado")

    sensor = Sensor.ClaseSensor(
        idSensor, tipo, idParcela, estado, ubicacionParcela, unidadMedida, rangoValido
    )
    sql_db.insertarSensor(sensor)
    leerSensoresJson()
    print("Sensor agregado exitosamente.")


def modificarSensor():
    idsensormodificar = input("Ingrese el ID del sensor que desea modificar: ")
    for sensor in ListaSensores:
        if sensor.idSensor == idsensormodificar:
            print("Sensor encontrado. Ingrese los nuevos datos:")

            while True:
                sensor.tipo = input(
                    "Ingrese el nuevo tipo de sensor (HumedadSuelo/Temperatura/LLuvia):  "
                ).lower()
                if ClaseValidaciones.esValidoTipoSensor(sensor.tipo):
                    break
                else:
                    print("Ingrese un tipo de sensor adecuado")

            while True:
                sensor.idParcela = input(
                    "Ingrese el nuevo ID de la parcela asociada al sensor: "
                )
                if ClaseValidaciones.esNumericoNoVacio(sensor.idParcela):
                    if ClaseValidaciones.existeParcelaID(sensor.idParcela, ListaParcelas):
                        break
                    else:
                        print("El ID de la parcela no existe. Ingrese un ID valido.")

            while True:
                sensor.estado = input(
                    "Ingrese el nuevo estado del sensor (activo/inactivo): "
                )
                if ClaseValidaciones.esValidoEstadoSensor(sensor.estado):
                    break
                else:
                    print("Ingrese un estado de sensor adecuado")

            while True:
                sensor.ubicacionParcela = input(
                    "Ingrese la nueva ubicacion del sensor en la parcela: "
                )
                if ClaseValidaciones.estaVacioString(sensor.ubicacionParcela):
                    break
                else:
                    print("Ingrese una ubicacion adecuada")

            while True:
                sensor.unidadMedida = input(
                    "Ingrese la nueva unidad de medida del sensor: "
                )
                if ClaseValidaciones.estaVacioString(sensor.unidadMedida):
                    break
                else:
                    print("Ingrese una unidad de medida adecuada")

            while True:
                sensor.rangoValido = input(
                    "Ingrese el nuevo rango valido de medicion del sensor: "
                )
                if ClaseValidaciones.esRangoSensorValido(sensor.rangoValido):
                    break
                else:
                    print("Ingrese un rango valido adecuado")

            sql_db.actualizarSensor(sensor)
            leerSensoresJson()
            print("Sensor modificado exitosamente.")
            return
    print("Sensor no encontrado.")


def eliminarSensor():
    idsensormodificar = input("Ingrese el ID del sensor que desea modificar: ")
    sql_db.eliminarSensor(idsensormodificar)
    leerSensoresJson()
    print("Sensor eliminado exitosamente.")


def verSensorPorID():
    idsensorver = input("Ingrese el ID del sensor que desea ver: ")
    for sensor in ListaSensores:
        if sensor.idSensor == idsensorver:
            print(sensor)
            return
    print("Sensor no encontrado.")


def verTodosLosSensores():
    if not ListaSensores:
        print("No hay sensores registrados.")
        return
    for sensor in ListaSensores:
        print(sensor)


def verSensoresPorParcela():
    idparcelaver = input("Ingrese el ID de la parcela que desea ver los sensores: ")
    if not ClaseValidaciones.existeParcelaID(idparcelaver, ListaParcelas):
        print("La parcela no existe.")
        return

    sensoresEnParcela = [sensor for sensor in ListaSensores if sensor.idParcela == idparcelaver]
    if not sensoresEnParcela:
        print("No hay sensores registrados en esta parcela.")
        return

    for sensor in sensoresEnParcela:
        print(sensor)


# ================== FUNCIONES DE LECTURAS ==================
def nuevaLectura():
    print("Creando una nueva lectura de sensor...")

    while True:
        idLectura = input("Ingrese el ID de la lectura: ")
        if ClaseValidaciones.existeLectura(idLectura, ListaLecturas):
            print("El ID de la lectura ya existe. Ingrese un ID diferente.")
        else:
            break

    while True:
        idSensor = input("Ingrese el ID del sensor: ")
        if ClaseValidaciones.existeSensorID(idSensor, ListaSensores):
            break
        else:
            print("El ID del sensor no existe. Ingrese un ID valido.")

    while True:
        idParcela = input("Ingrese el ID de la parcela: ")
        if ClaseValidaciones.existeParcelaID(idParcela, ListaParcelas):
            break
        else:
            print("El ID de la parcela no existe. Ingrese un ID valido.")

    while True:
        fechaHora = input("Ingrese la fecha y hora (DD-MM-YYYY HH:MM:SS): ")
        if ClaseValidaciones.esfechaValidaFormato(fechaHora):
            break
        else:
            print(
                "La fecha y hora ingresadas no son validas. Ingrese una fecha y hora en el formato DD-MM-YYYY HH:MM:SS."
            )

    while True:
        valorMedido = input("Ingrese el valor medido: ")
        if ClaseValidaciones.esNumericoNoVacioFloat(valorMedido):
            break
        else:
            print("Ingrese un valor medido en valores numericos")

    lectura = Lectura.ClaseLectura(idLectura, idSensor, idParcela, fechaHora, valorMedido)
    ListaLecturas.append(lectura)
    mongo_db.insertarLectura(lectura)
    print("Lectura de sensor agregada exitosamente.")
    determinarAlertas(lectura)


def verLecturaPorFecha():
    while True:
        fechaVer = input("Ingrese la fecha (DD-MM-YYYY) de las lecturas que desea ver: ")
        if ClaseValidaciones.esFechaCortaValida(fechaVer):
            break
        else:
            print("La fecha ingresada no es valida. Ingrese una fecha en el formato DD-MM-YYYY.")

    lecturasEncontradas = [lectura for lectura in ListaLecturas if lectura.fechaHora.startswith(fechaVer)]
    if not lecturasEncontradas:
        print("No se encontraron lecturas para la fecha y parcela especificada.")
        return

    for lectura in lecturasEncontradas:
        print(lectura)


def VerLecturasPorParcela():
    while True:
        idparcelaver = input("Ingrese el ID de la parcela que desea ver: ")
        if ClaseValidaciones.existeParcelaID(idparcelaver, ListaParcelas):
            break
        else:
            print("El ID de la parcela no existe. Ingrese un ID valido.")

    for lectura in ListaLecturas:
        if lectura.idParcela == idparcelaver:
            print(lectura)
            return
    print("Lectura no encontrada.")


def verLecturasSensor():
    while True:
        idsensorver = input("Ingrese el ID del sensor que desea ver las lecturas: ")
        if ClaseValidaciones.existeSensorID(idsensorver, ListaSensores):
            break
        else:
            print("El ID del sensor no existe. Ingrese un ID valido.")

    for lectura in ListaLecturas:
        if lectura.idSensor == idsensorver:
            print(lectura)
    print("Fin de las lecturas para el sensor.")


def borrarLecturaParcelaFecha():
    while True:
        idparcelaborrar = input("Ingrese el ID de la parcela que desea borrar las lecturas: ")
        if ClaseValidaciones.existeParcelaID(idparcelaborrar, ListaParcelas):
            break
        else:
            print("El ID de la parcela no existe. Ingrese un ID valido.")

    while True:
        fechaBorrar = input("Ingrese la fecha (DD-MM-YYYY) de las lecturas que desea borrar: ")
        if ClaseValidaciones.esFechaCortaValida(fechaBorrar):
            break
        else:
            print("La fecha ingresada no es valida. Ingrese una fecha en el formato DD-MM-YYYY.")

    resultado = mongo_db.eliminarLecturasPorParcelaYFecha(idparcelaborrar, fechaBorrar)
    leerLecturasJson()
    if resultado == 0:
        print("No se encontraron lecturas para la fecha y parcela especificada.")
        return
    print(f"Se borraron {resultado} lecturas para la fecha {fechaBorrar} y la parcela {idparcelaborrar}.")


# ================== FUNCIONES DE ALERTAS ==================
def determinarAlertas(lectura):
    lecturaIDParcela = lectura.idParcela
    lecturaIDSensor = lectura.idSensor
    LecturaValorMedido = lectura.valorMedido
    lecturaFechaHora = lectura.fechaHora
    rangoInferior = rangoSuperior = tipoSensor = None
    for sensor in ListaSensores:
        if sensor.idSensor == lecturaIDSensor:
            partes = [parte.strip() for parte in sensor.rangoValido.split("-")]
            rangoInferior = partes[0]
            rangoSuperior = partes[1]
            tipoSensor = sensor.tipo
            break
    if tipoSensor == "humedadsuelo":
        alertaNueva = Alertas.ClaseAlerta(
            lecturaIDParcela,
            lecturaIDSensor,
            tipoSensor,
            lecturaFechaHora,
            LecturaValorMedido,
            mensajeAlertaHumedadSuelo(LecturaValorMedido, rangoInferior, rangoSuperior),
        )
        nuevaAlerta(alertaNueva)
    if tipoSensor == "temperatura":
        alertaNueva = Alertas.ClaseAlerta(
            lecturaIDParcela,
            lecturaIDSensor,
            tipoSensor,
            lecturaFechaHora,
            LecturaValorMedido,
            mensajeAlertaTemperatura(LecturaValorMedido, rangoInferior, rangoSuperior),
        )
        nuevaAlerta(alertaNueva)
    if tipoSensor == "lluvia":
        alertaNueva = Alertas.ClaseAlerta(
            lecturaIDParcela,
            lecturaIDSensor,
            tipoSensor,
            lecturaFechaHora,
            LecturaValorMedido,
            mensajeAlertaLluvia(LecturaValorMedido, rangoInferior, rangoSuperior),
        )
        nuevaAlerta(alertaNueva)


def nuevaAlerta(NuevaAlerta):
    ListaAlertas.append(NuevaAlerta)
    mongo_db.insertarAlerta(NuevaAlerta)
    print("Alerta generada exitosamente.")


def mensajeAlertaHumedadSuelo(LecturaValorMedido, rangoInferior, rangoSuperior) -> str:
    if int(LecturaValorMedido) <= int(rangoInferior) or int(LecturaValorMedido) >= int(rangoSuperior):
        mensajeAlerta = "ALERTA!!!! El parametro {} rebasa el rango permitido [{} - {}]".format(
            LecturaValorMedido, rangoInferior, rangoSuperior
        )
        print(mensajeAlerta)
        return mensajeAlerta
    mensajeExito = "La humedad del suelo esta dentro de los niveles optimos."
    print(mensajeExito)
    return mensajeExito


def mensajeAlertaTemperatura(LecturaValorMedido, rangoInferior, rangoSuperior) -> str:
    if int(LecturaValorMedido) <= int(rangoInferior) or int(LecturaValorMedido) >= int(rangoSuperior):
        mensajeAlerta = "ALERTA!!!! El parametro {} rebasa el rango permitido [{} - {}]".format(
            LecturaValorMedido, rangoInferior, rangoSuperior
        )
        print(mensajeAlerta)
        return mensajeAlerta
    mensajeExito = "La temperatura esta dentro de los niveles optimos."
    print(mensajeExito)
    return mensajeExito


def mensajeAlertaLluvia(LecturaValorMedido, rangoInferior, rangoSuperior) -> str:
    if int(LecturaValorMedido) <= int(rangoInferior) or int(LecturaValorMedido) >= int(rangoSuperior):
        mensajeAlerta = "ALERTA!!!! El parametro {} rebasa el rango permitido [{} - {}]".format(
            LecturaValorMedido, rangoInferior, rangoSuperior
        )
        print(mensajeAlerta)
        return mensajeAlerta
    mensajeExito = "La cantidad de lluvia esta dentro de los niveles optimos."
    print(mensajeExito)
    return mensajeExito


def verAlertasPorParcela():
    idParcelaVer = input("Ingrese el ID de la parcela para ver sus alertas: ")
    if not ClaseValidaciones.existeParcelaID(idParcelaVer, ListaParcelas):
        print("La parcela no existe.")
        return

    alertasEnParcela = [alerta for alerta in ListaAlertas if alerta.idParcela == idParcelaVer]
    if not alertasEnParcela:
        print("No hay alertas registradas en esta parcela.")
        return

    for alerta in alertasEnParcela:
        print(alerta)


def verAlertasPorParcelaFecha():
    while True:
        idParcelaVer = input("Ingrese el ID de la parcela para ver sus alertas: ")
        if ClaseValidaciones.existeParcelaID(idParcelaVer, ListaParcelas):
            break
        else:
            print("El ID de la parcela no existe. Ingrese un ID valido.")

    while True:
        fechaVer = input("Ingrese la fecha (DD-MM-YYYY) para ver las alertas: ")
        if ClaseValidaciones.esFechaCortaValida(fechaVer):
            break
        else:
            print("La fecha ingresada no es valida. Ingrese una fecha en el formato DD-MM-YYYY.")

    alertasEncontradas = [
        alerta for alerta in ListaAlertas if int(alerta.idParcela) == int(idParcelaVer) and alerta.fechaGeneracion.startswith(fechaVer)
    ]
    if not alertasEncontradas:
        print("No se encontraron alertas para la fecha y parcela especificada.")
        return

    for alerta in alertasEncontradas:
        print(alerta)


# ================== CALCULO DE VOLUMEN DE RIEGO ==================
def calcularVolumenRiegoPorParcelaYFecha():
    while True:
        idParcelaVer = input("Ingrese el ID de la parcela para calcular el volumen de riego: ")
        if ClaseValidaciones.existeParcelaID(idParcelaVer, ListaParcelas):
            break
        else:
            print("El ID de la parcela no existe. Ingrese un ID valido.")

    while True:
        fechaVer = input("Ingrese la fecha (DD-MM-YYYY) para calcular el volumen de riego: ")
        if ClaseValidaciones.esFechaCortaValida(fechaVer):
            break
        else:
            print("La fecha ingresada no es valida. Ingrese una fecha en el formato DD-MM-YYYY.")

    for parcela in ListaParcelas:
        if parcela.idParcela == idParcelaVer:
            areaParcela = float(parcela.area)
            eficienciaRiego = float(parcela.eficienciaRiego)
            profundidadRaiz = float(parcela.profundidadRaiz)
            volumenRiegoDeseado = float(parcela.volumenDeseado)
            break

    SensoresHumedad = [
        sensor for sensor in ListaSensores if sensor.idParcela == idParcelaVer and sensor.tipo == "humedadsuelo"
    ]
    humedadVolumetrica = 0.0
    for sensor in SensoresHumedad:
        idSensorHumedadSuelo = sensor.idSensor
        lecturasFiltradas = [
            lectura
            for lectura in ListaLecturas
            if lectura.idParcela == idParcelaVer and lectura.idSensor == idSensorHumedadSuelo and lectura.fechaHora.startswith(fechaVer)
        ]
        if lecturasFiltradas:
            for lectura in lecturasFiltradas:
                humedadVolumetrica = humedadVolumetrica + float(lectura.valorMedido)
            break

    VolumenDeRiego = ((areaParcela * (volumenRiegoDeseado - humedadVolumetrica) * profundidadRaiz) / eficienciaRiego)
    if humedadVolumetrica >= volumenRiegoDeseado:
        print("El volumen de Riego Necesario es 0.")
        print("No es necesario regar la parcela, ya que la humedad es adecuada al volumen de riego deseado.")
    else:
        print(f"El volumen total de riego para la parcela ID {idParcelaVer} en la fecha {fechaVer} es: {VolumenDeRiego} litros.")
        print("Es necesario regar la parcela, ya que la humedad es menor al volumen de riego deseado.")

    CalculoVolumenRiego = {"idParcela": idParcelaVer, "fecha": fechaVer, "volumenRiego": VolumenDeRiego}
    ListaCalculoVolumen.append(CalculoVolumenRiego)
    sql_db.insertarCalculoRiego(CalculoVolumenRiego)
    leerCalculoVolumenRiegoJson()

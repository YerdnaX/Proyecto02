import Entidades.ClaseParcela as Parcela
import Entidades.ClaseSensor as Sensor
import Entidades.ClaseLectura as Lectura
import Entidades.ClaseAlerta as Alertas
from CapaNegocio.ClaseValidaciones import ClaseValidaciones
from CapaDatos.ClaseSQL import ClaseSQL
from CapaDatos.ClaseMONGO import ClaseMONGO
from CapaDatos.ClaseXmlManager import cargarLecturasXML
from datetime import datetime, date


sql_db = ClaseSQL()
mongo_db = ClaseMONGO()

# Estado en memoria
ListaParcelas = []
ListaSensores = []
ListaLecturas = []
ListaAlertas = []
ListaCalculoVolumen = []


# ================== Transformadores ==================
def _parcela_a_dict(parcela):
    return {
        "idParcela": parcela.idParcela,
        "nombre": parcela.nombre,
        "ubicacion": parcela.ubicacion,
        "tipoCultivo": parcela.tipoCultivo,
        "area": parcela.area,
        "profundidadRaiz": parcela.profundidadRaiz,
        "eficienciaRiego": parcela.eficienciaRiego,
        "umbralHumedadMin": parcela.umbralHumedadMin,
        "umbralHumedadMax": parcela.umbralHumedadMax,
        "volumenDeseado": parcela.volumenDeseado,
    }


def _sensor_a_dict(sensor):
    return {
        "idSensor": sensor.idSensor,
        "tipo": sensor.tipo,
        "idParcela": sensor.idParcela,
        "estado": sensor.estado,
        "ubicacionParcela": sensor.ubicacionParcela,
        "unidadMedida": sensor.unidadMedida,
        "rangoValido": sensor.rangoValido,
    }


def _lectura_a_dict(lectura):
    return {
        "idLectura": lectura.idLectura,
        "idSensor": lectura.idSensor,
        "idParcela": lectura.idParcela,
        "fechaHora": lectura.fechaHora,
        "valorMedido": lectura.valorMedido,
    }


def _alerta_a_dict(alerta):
    return {
        "idParcela": alerta.idParcela,
        "idSensor": alerta.idSensor,
        "tipo": alerta.tipo,
        "fechaGeneracion": alerta.fechaGeneracion,
        "valorDetectado": alerta.valorDetectado,
        "mensajeAlerta": alerta.mensajeAlerta,
    }


def cargar_datos_iniciales():
    cargar_parcelas_db()
    cargar_sensores_db()
    cargar_lecturas_db()
    cargar_alertas_db()
    cargar_calculos_riego_db()


# ================== Lecturas desde BD ==================
def cargar_parcelas_db():
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


def cargar_sensores_db():
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


def cargar_lecturas_db():
    ListaLecturas.clear()
    for doc in mongo_db.obtenerLecturas():
        doc.pop("_id", None)
        lectura = Lectura.ClaseLectura.crearDesdeDiccionario(doc)
        ListaLecturas.append(lectura)


def cargar_alertas_db():
    ListaAlertas.clear()
    for doc in mongo_db.obtenerAlertas():
        doc.pop("_id", None)
        alerta = Alertas.ClaseAlerta.crearDesdeDiccionario(doc)
        ListaAlertas.append(alerta)


def cargar_calculos_riego_db():
    ListaCalculoVolumen.clear()
    for row in sql_db.obtenerCalculosRiego():
        fecha_val = getattr(row, "fecha", None)
        volumen_val = getattr(row, "volumenRiego", None)
        if fecha_val is None and len(row) >= 2:
            fecha_val = row[1]
        if volumen_val is None and len(row) >= 3:
            volumen_val = row[2]
        # Si vienen invertidos por el orden de columnas, corrige.
        if isinstance(volumen_val, (datetime, date)) and not isinstance(fecha_val, (datetime, date)):
            fecha_val, volumen_val = volumen_val, fecha_val

        fecha_str = (
            fecha_val.strftime("%d-%m-%Y") if isinstance(fecha_val, (datetime, date)) else str(fecha_val)
        )
        volumen_num = float(volumen_val) if volumen_val is not None else 0.0

        ListaCalculoVolumen.append({"idParcela": str(row[0]), "fecha": fecha_str, "volumenRiego": volumen_num})


def cargar_lecturas_desde_xml(ruta="./Lecturas.xml"):
    """Carga lecturas desde un XML y las inserta en MongoDB (omite duplicados por idLectura)."""
    nuevos = 0
    cargar_sensores_db()  # asegure rangos y tipos cargados para generar alertas
    lecturas = cargarLecturasXML(ruta)
    ids_existentes = {lec.idLectura for lec in ListaLecturas}
    for dic in lecturas:
        if dic["idLectura"] in ids_existentes:
            continue
        lectura = Lectura.ClaseLectura.crearDesdeDiccionario(dic)
        ListaLecturas.append(lectura)
        mongo_db.insertarLectura(lectura)
        determinarAlertas(lectura)
        nuevos += 1
    cargar_lecturas_db()
    cargar_alertas_db()
    return nuevos


# ================== Parcela ==================
def listar_parcelas():
    return [_parcela_a_dict(p) for p in ListaParcelas]


def crear_parcela(data):
    if not ClaseValidaciones.esNumericoNoVacio(data["idParcela"]):
        raise ValueError("ID de parcela invalido")
    if ClaseValidaciones.existeParcelaID(data["idParcela"], ListaParcelas):
        raise ValueError("La parcela ya existe")
    if not ClaseValidaciones.estaVacioString(data["nombre"]):
        raise ValueError("Nombre requerido")
    if not ClaseValidaciones.estaVacioString(data["ubicacion"]):
        raise ValueError("Ubicacion requerida")
    if not ClaseValidaciones.estaVacioString(data["tipoCultivo"]):
        raise ValueError("Tipo de cultivo requerido")
    for campo in ("area", "profundidadRaiz", "eficienciaRiego", "umbralHumedadMin", "umbralHumedadMax", "volumenDeseado"):
        if not ClaseValidaciones.esNumericoNoVacioFloat(data.get(campo, "")):
            raise ValueError(f"{campo} debe ser numerico")
    if float(data["umbralHumedadMax"]) <= float(data["umbralHumedadMin"]):
        raise ValueError("Umbral maximo debe ser mayor al minimo")

    parcela = Parcela.ClaseParcela(
        data["idParcela"],
        data["nombre"],
        data["ubicacion"],
        data["tipoCultivo"],
        data["area"],
        data["profundidadRaiz"],
        data["eficienciaRiego"],
        data["umbralHumedadMin"],
        data["umbralHumedadMax"],
        data["volumenDeseado"],
    )
    sql_db.insertarParcela(parcela)
    cargar_parcelas_db()
    return parcela


def actualizar_parcela(data):
    if not ClaseValidaciones.existeParcelaID(data["idParcela"], ListaParcelas):
        raise ValueError("Parcela no existe")
    if not ClaseValidaciones.estaVacioString(data["nombre"]):
        raise ValueError("Nombre requerido")
    if not ClaseValidaciones.estaVacioString(data["ubicacion"]):
        raise ValueError("Ubicacion requerida")
    if not ClaseValidaciones.estaVacioString(data["tipoCultivo"]):
        raise ValueError("Tipo de cultivo requerido")
    for campo in ("area", "profundidadRaiz", "eficienciaRiego", "umbralHumedadMin", "umbralHumedadMax", "volumenDeseado"):
        if not ClaseValidaciones.esNumericoNoVacioFloat(data.get(campo, "")):
            raise ValueError(f"{campo} debe ser numerico")
    if float(data["umbralHumedadMax"]) <= float(data["umbralHumedadMin"]):
        raise ValueError("Umbral maximo debe ser mayor al minimo")

    parcela = Parcela.ClaseParcela(
        data["idParcela"],
        data["nombre"],
        data["ubicacion"],
        data["tipoCultivo"],
        data["area"],
        data["profundidadRaiz"],
        data["eficienciaRiego"],
        data["umbralHumedadMin"],
        data["umbralHumedadMax"],
        data["volumenDeseado"],
    )
    sql_db.actualizarParcela(parcela)
    cargar_parcelas_db()
    return parcela


def eliminar_parcela(idParcela):
    if not ClaseValidaciones.existeParcelaID(idParcela, ListaParcelas):
        raise ValueError("Parcela no existe")
    sql_db.eliminarParcela(idParcela)
    cargar_parcelas_db()


# ================== Sensor ==================
def listar_sensores():
    return [_sensor_a_dict(s) for s in ListaSensores]


def crear_sensor(data):
    if not ClaseValidaciones.esNumericoNoVacio(data["idSensor"]):
        raise ValueError("ID de sensor invalido")
    if ClaseValidaciones.existeSensorID(data["idSensor"], ListaSensores):
        raise ValueError("Sensor ya existe")
    if not ClaseValidaciones.esValidoTipoSensor(data["tipo"]):
        raise ValueError("Tipo de sensor invalido")
    if not ClaseValidaciones.existeParcelaID(data["idParcela"], ListaParcelas):
        raise ValueError("Parcela asociada no existe")
    if not ClaseValidaciones.esValidoEstadoSensor(data["estado"]):
        raise ValueError("Estado de sensor invalido")
    if not ClaseValidaciones.estaVacioString(data["ubicacionParcela"]):
        raise ValueError("Ubicacion requerida")
    if not ClaseValidaciones.estaVacioString(data["unidadMedida"]):
        raise ValueError("Unidad de medida requerida")
    if not ClaseValidaciones.esRangoSensorValido(data["rangoValido"]):
        raise ValueError("Rango valido requerido")

    sensor = Sensor.ClaseSensor(
        data["idSensor"],
        data["tipo"],
        data["idParcela"],
        data["estado"],
        data["ubicacionParcela"],
        data["unidadMedida"],
        data["rangoValido"],
    )
    sql_db.insertarSensor(sensor)
    cargar_sensores_db()
    return sensor


def actualizar_sensor(data):
    if not ClaseValidaciones.existeSensorID(data["idSensor"], ListaSensores):
        raise ValueError("Sensor no existe")
    if not ClaseValidaciones.esValidoTipoSensor(data["tipo"]):
        raise ValueError("Tipo de sensor invalido")
    if not ClaseValidaciones.existeParcelaID(data["idParcela"], ListaParcelas):
        raise ValueError("Parcela asociada no existe")
    if not ClaseValidaciones.esValidoEstadoSensor(data["estado"]):
        raise ValueError("Estado de sensor invalido")
    if not ClaseValidaciones.estaVacioString(data["ubicacionParcela"]):
        raise ValueError("Ubicacion requerida")
    if not ClaseValidaciones.estaVacioString(data["unidadMedida"]):
        raise ValueError("Unidad de medida requerida")
    if not ClaseValidaciones.esRangoSensorValido(data["rangoValido"]):
        raise ValueError("Rango valido requerido")

    sensor = Sensor.ClaseSensor(
        data["idSensor"],
        data["tipo"],
        data["idParcela"],
        data["estado"],
        data["ubicacionParcela"],
        data["unidadMedida"],
        data["rangoValido"],
    )
    sql_db.actualizarSensor(sensor)
    cargar_sensores_db()
    return sensor


def eliminar_sensor(idSensor):
    if not ClaseValidaciones.existeSensorID(idSensor, ListaSensores):
        raise ValueError("Sensor no existe")
    sql_db.eliminarSensor(idSensor)
    cargar_sensores_db()


# ================== Lecturas ==================
def listar_lecturas():
    return [_lectura_a_dict(l) for l in ListaLecturas]


def crear_lectura(data):
    if ClaseValidaciones.existeLectura(data["idLectura"], ListaLecturas):
        raise ValueError("La lectura ya existe")
    if not ClaseValidaciones.existeSensorID(data["idSensor"], ListaSensores):
        raise ValueError("Sensor no existe")
    if not ClaseValidaciones.existeParcelaID(data["idParcela"], ListaParcelas):
        raise ValueError("Parcela no existe")
    if not ClaseValidaciones.esfechaValidaFormato(data["fechaHora"]):
        raise ValueError("FechaHora invalida (DD-MM-YYYY HH:MM:SS)")
    if not ClaseValidaciones.esNumericoNoVacioFloat(data["valorMedido"]):
        raise ValueError("Valor medido invalido")

    lectura = Lectura.ClaseLectura(
        data["idLectura"],
        data["idSensor"],
        data["idParcela"],
        data["fechaHora"],
        data["valorMedido"],
    )
    ListaLecturas.append(lectura)
    mongo_db.insertarLectura(lectura)
    determinarAlertas(lectura)
    cargar_lecturas_db()
    return lectura


def lecturas_por_sensor(idSensor):
    return [_lectura_a_dict(l) for l in ListaLecturas if l.idSensor == idSensor]


def lecturas_por_parcela(idParcela):
    return [_lectura_a_dict(l) for l in ListaLecturas if l.idParcela == idParcela]


def lecturas_por_fecha(fecha):
    return [_lectura_a_dict(l) for l in ListaLecturas if l.fechaHora.startswith(fecha)]


def borrar_lecturas_parcela_fecha(idParcela, fecha):
    cantidad = mongo_db.eliminarLecturasPorParcelaYFecha(idParcela, fecha)
    cargar_lecturas_db()
    return cantidad

def lecturas_en_rango(idParcela, sensores_ids, fecha_inicio, fecha_fin):
    """Devuelve lecturas filtradas por parcela, sensores y rango de fechas (inclusive)."""
    def parse(dt_str):
        try:
            return datetime.strptime(dt_str, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            try:
                return datetime.strptime(dt_str, "%d-%m-%Y")
            except ValueError:
                return None

    inicio_dt = parse(fecha_inicio)
    fin_dt = parse(fecha_fin)
    if not inicio_dt or not fin_dt:
        raise ValueError("Fechas deben tener formato DD-MM-YYYY o DD-MM-YYYY HH:MM:SS")

    sensores_set = set(sensores_ids) if sensores_ids else None
    resultado = []
    for l in ListaLecturas:
        if l.idParcela != idParcela:
            continue
        if sensores_set and l.idSensor not in sensores_set:
            continue
        dt_l = parse(l.fechaHora)
        if not dt_l:
            continue
        if inicio_dt <= dt_l <= fin_dt:
            resultado.append(_lectura_a_dict(l))
    return resultado

# ================== Alertas ==================
def listar_alertas():
    return [_alerta_a_dict(a) for a in ListaAlertas]


def alertas_por_parcela(idParcela):
    return [_alerta_a_dict(a) for a in ListaAlertas if a.idParcela == idParcela]


def alertas_por_parcela_fecha(idParcela, fecha):
    return [
        _alerta_a_dict(a)
        for a in ListaAlertas
        if a.idParcela == idParcela and a.fechaGeneracion.startswith(fecha)
    ]


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
    cargar_alertas_db()


def mensajeAlertaHumedadSuelo(LecturaValorMedido, rangoInferior, rangoSuperior) -> str:
    if int(LecturaValorMedido) <= int(rangoInferior) or int(LecturaValorMedido) >= int(rangoSuperior):
        return "ALERTA!!!! El parametro {} rebasa el rango permitido [{} - {}]".format(
            LecturaValorMedido, rangoInferior, rangoSuperior
        )
    return "La humedad del suelo esta dentro de los niveles optimos."


def mensajeAlertaTemperatura(LecturaValorMedido, rangoInferior, rangoSuperior) -> str:
    if int(LecturaValorMedido) <= int(rangoInferior) or int(LecturaValorMedido) >= int(rangoSuperior):
        return "ALERTA!!!! El parametro {} rebasa el rango permitido [{} - {}]".format(
            LecturaValorMedido, rangoInferior, rangoSuperior
        )
    return "La temperatura esta dentro de los niveles optimos."


def mensajeAlertaLluvia(LecturaValorMedido, rangoInferior, rangoSuperior) -> str:
    if int(LecturaValorMedido) <= int(rangoInferior) or int(LecturaValorMedido) >= int(rangoSuperior):
        return "ALERTA!!!! El parametro {} rebasa el rango permitido [{} - {}]".format(
            LecturaValorMedido, rangoInferior, rangoSuperior
        )
    return "La cantidad de lluvia esta dentro de los niveles optimos."


# ================== Calculo Riego ==================
def calcular_volumen_riego(idParcelaVer, fechaVer):
    if not ClaseValidaciones.existeParcelaID(idParcelaVer, ListaParcelas):
        raise ValueError("La parcela no existe")
    if not ClaseValidaciones.esFechaCortaValida(fechaVer):
        raise ValueError("Fecha invalida (DD-MM-YYYY)")

    for parcela in ListaParcelas:
        if parcela.idParcela == idParcelaVer:
            if parcela.area in (None, "") or parcela.eficienciaRiego in (None, "") or parcela.profundidadRaiz in (None, "") or parcela.volumenDeseado in (None, ""):
                raise ValueError("Complete los datos numericos de la parcela (area, eficiencia, profundidad, volumen deseado) antes de calcular.")
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
    CalculoVolumenRiego = {"idParcela": idParcelaVer, "fecha": fechaVer, "volumenRiego": VolumenDeRiego}
    ListaCalculoVolumen.append(CalculoVolumenRiego)
    sql_db.insertarCalculoRiego(CalculoVolumenRiego)
    cargar_calculos_riego_db()
    return CalculoVolumenRiego


def listar_calculos_riego():
    return list(ListaCalculoVolumen)

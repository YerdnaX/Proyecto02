from pathlib import Path
import json
import os

################## Parcelas ##################
##Guardar parcelas existentes
def guardarParcelaJson(parcela, RutaArchivo):
    rutaUsar = Path(RutaArchivo)
    rutaUsar.parent.mkdir(parents=True, exist_ok=True)
    rutaUsar.touch(exist_ok=True)
    with open(RutaArchivo, 'w', encoding="utf-8") as archivo:
            json.dump(parcela, archivo, indent=4, ensure_ascii=False)

##Cargar parcelas existentes desde archivo
def cargarParcelaJson(RutaArchivo):
    if not os.path.exists(RutaArchivo):
        return []
    with open(RutaArchivo, 'r', encoding="utf-8") as archivo:
            datos = json.load(archivo)
    return datos

################## Sensores ##################
##Guardar sensores existentes
def guardarSensorJson(sensor, RutaArchivo):
    rutaUsar = Path(RutaArchivo)
    rutaUsar.parent.mkdir(parents=True, exist_ok=True)
    rutaUsar.touch(exist_ok=True)
    with open(RutaArchivo, 'w', encoding="utf-8") as archivo:
            json.dump(sensor, archivo, indent=4, ensure_ascii=False)

##Cargar sensores existentes desde archivo
def cargarSensorJson(RutaArchivo):
    if not os.path.exists(RutaArchivo):
        return []
    with open(RutaArchivo, 'r', encoding="utf-8") as archivo:
            datos = json.load(archivo)
    return datos

################## Lecturas ##################
##Guardar lecturas de sensores existentes
def guardarLecturaSensorJson(lecturaSensor, RutaArchivo):
    rutaUsar = Path(RutaArchivo)
    rutaUsar.parent.mkdir(parents=True, exist_ok=True)
    rutaUsar.touch(exist_ok=True)
    with open(RutaArchivo, 'w', encoding="utf-8") as archivo:
            json.dump(lecturaSensor, archivo, indent=4, ensure_ascii=False)

def cargarLecturaSensorJson(RutaArchivo):
    if not os.path.exists(RutaArchivo):
        return []
    with open(RutaArchivo, 'r', encoding="utf-8") as archivo:
            datos = json.load(archivo)
    return datos

def guardarAlertaJson(alerta, RutaArchivo):
    rutaUsar = Path(RutaArchivo)
    rutaUsar.parent.mkdir(parents=True, exist_ok=True)
    rutaUsar.touch(exist_ok=True)
    with open(RutaArchivo, 'w', encoding="utf-8") as archivo:
            json.dump(alerta, archivo, indent=4, ensure_ascii=False)

def cargarAlertaJson(RutaArchivo):
    if not os.path.exists(RutaArchivo):
        return []
    with open(RutaArchivo, 'r', encoding="utf-8") as archivo:
            datos = json.load(archivo)
    return datos

def guardarCalculoVolumenRiegoJson(calculoVolumenRiego, RutaArchivo):
    rutaUsar = Path(RutaArchivo)
    rutaUsar.parent.mkdir(parents=True, exist_ok=True)
    rutaUsar.touch(exist_ok=True)
    with open(RutaArchivo, 'w', encoding="utf-8") as archivo:
            json.dump(calculoVolumenRiego, archivo, indent=4, ensure_ascii=False)
    
def cargarCalculoVolumenRiegoJson(RutaArchivo):
    if not os.path.exists(RutaArchivo):
        return []
    with open(RutaArchivo, 'r', encoding="utf-8") as archivo:
            datos = json.load(archivo)
    return datos
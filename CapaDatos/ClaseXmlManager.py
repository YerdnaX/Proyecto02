import xml.etree.ElementTree as ET
import os


def cargarLecturasXML(ruta: str = "./Lecturas.xml") -> list:
    """Carga lecturas desde un archivo XML en la ruta dada."""
    lista_lecturas = []
    if os.path.exists(ruta):
        tree = ET.parse(ruta)
        raiz = tree.getroot()
        for nodo in raiz.findall("Lectura"):
            idLectura = nodo.find("idLectura").text
            idSensor = nodo.find("idSensor").text
            idParcela = nodo.find("idParcela").text
            fechaHora = nodo.find("fechaHora").text
            valorMedido = nodo.find("valorMedido").text
            lectura = {
                "idLectura": idLectura,
                "idSensor": idSensor,
                "idParcela": idParcela,
                "fechaHora": fechaHora,
                "valorMedido": valorMedido,
            }
            lista_lecturas.append(lectura)
    return lista_lecturas

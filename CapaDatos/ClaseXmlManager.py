import xml.etree.ElementTree as ET
import os


def cargarLecturasXML() -> list:
    lista_lecturas = []
    if os.path.exists("./Lecturas.xml"):
        tree = ET.parse("./Lecturas.xml")
        raiz = tree.getroot()
        for nodo in raiz.findall('Lectura'):

            idLectura = nodo.find('idLectura').text
            idSensor = nodo.find('idSensor').text
            idParcela = nodo.find('idParcela').text
            fechaHora = nodo.find('fechaHora').text
            valorMedido = nodo.find('valorMedido').text
            lectura = {
                "idLectura": idLectura,
                "idSensor": idSensor,
                "idParcela": idParcela,
                "fechaHora": fechaHora,
                "valorMedido": valorMedido
            }
            lista_lecturas.append(lectura)
    return lista_lecturas
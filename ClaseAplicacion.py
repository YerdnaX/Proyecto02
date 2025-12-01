from ClaseMenu import *
from CapaNegocio.ClaseSistema import *

##############Clase aplicacion interactua con el menu y las funciones de la ClaseSistema##############
def main():
    leerParcelasJson()
    leerSensoresJson()
    leerLecturasJson()
    leerAlertasJson()
    leerCalculoVolumenRiegoJson()

    continuar = True
    while continuar:
        opcion = menu()
        match opcion:
            case 11:
                nuevaparcela()
            case 12:
                modificarParcela()
            case 13:
                modificarDatosGeneralesParcela()
            case 14:
                eliminarParcela()
            case 15:
                verParcelaPorID()
            case 16:
                verTodasLasParcelas()
            case 21:
                nuevoSensor()
            case 22:
                modificarSensor()
            case 23:
                eliminarSensor()
            case 24:
                verSensorPorID()
            case 25:
                verTodosLosSensores()
            case 26:
                verSensoresPorParcela()
            case 31:
                nuevaLectura()
            case 32:
                cargarLecturasSensoresXML()
            case 33:
                verLecturasSensor()
            case 34:
                VerLecturasPorParcela()
            case 35:
                verLecturaPorFecha()
            case 36:
                borrarLecturaParcelaFecha()
            case 41:
                verAlertasPorParcela()
            case 42:
                verAlertasPorParcelaFecha()
            case 51:
                calcularVolumenRiegoPorParcelaYFecha()
            case _:
                continue
                

if __name__ == "__main__":
    main()
    
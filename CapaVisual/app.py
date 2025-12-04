import tkinter as tk
from tkinter import ttk

from CapaNegocio import ClaseSistema as svc
from CapaVisual.alerta_tab import AlertaTab
from CapaVisual.grafico_tab import GraficoTab
from CapaVisual.helpers import apply_modern_dark
from CapaVisual.lectura_tab import LecturaTab
from CapaVisual.parcela_tab import ParcelaTab
from CapaVisual.riego_tab import RiegoTab
from CapaVisual.sensor_tab import SensorTab
from CapaVisual.xml_tab import XmlTab


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AgroMon")
        self.geometry("1000x700")
        apply_modern_dark(self)
        self.contruirMenu()
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)
        nb.add(ParcelaTab(nb), text="Parcelas")
        nb.add(SensorTab(nb), text="Sensores")
        nb.add(LecturaTab(nb), text="Lecturas")
        nb.add(AlertaTab(nb), text="Alertas")
        nb.add(RiegoTab(nb), text="Riego")
        nb.add(XmlTab(nb), text="Carga XML")
        nb.add(GraficoTab(nb), text="Graficos")

    def contruirMenu(self):
        menubar = tk.Menu(self)
        datos_menu = tk.Menu(menubar, tearoff=0)
        datos_menu.add_command(label="Refrescar datos", command=svc.cargar_datos_iniciales)
        menubar.add_cascade(label="Datos", menu=datos_menu)
        menubar.add_command(label="Salir", command=self.destroy)
        self.config(menu=menubar)

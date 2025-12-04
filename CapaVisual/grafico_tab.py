import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from CapaNegocio import ClaseSistema as svc
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    Figure = None
    FigureCanvasTkAgg = None


class GraficoTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="ID Parcela").grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.parcela_entry = ttk.Entry(self, width=15)
        self.parcela_entry.grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        ttk.Label(self, text="IDs Sensores (Separados por ,)").grid(row=0, column=2, padx=4, pady=4, sticky="w")
        self.sensores_entry = ttk.Entry(self, width=20)
        self.sensores_entry.grid(row=0, column=3, padx=4, pady=4, sticky="ew")

        ttk.Label(self, text="Fecha Inicio (DD-MM-YYYY)").grid(row=1, column=0, padx=4, pady=4, sticky="w")
        self.fecha_ini_entry = ttk.Entry(self, width=15)
        self.fecha_ini_entry.grid(row=1, column=1, padx=4, pady=4, sticky="ew")
        ttk.Label(self, text="Fecha Fin (DD-MM-YYYY)").grid(row=1, column=2, padx=4, pady=4, sticky="w")
        self.fecha_fin_entry = ttk.Entry(self, width=15)
        self.fecha_fin_entry.grid(row=1, column=3, padx=4, pady=4, sticky="ew")

        ttk.Button(self, text="Graficar", command=self.graficar).grid(row=2, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Limpiar", command=self.limpiar).grid(row=2, column=1, padx=4, pady=6, sticky="ew")

        self.figure = None
        self.canvas = None
        self.columnconfigure(3, weight=1)
        self.rowconfigure(3, weight=1)

    def graficar(self):
        if Figure is None or FigureCanvasTkAgg is None:
            messagebox.showerror("Libreria faltante")
            return
        parcela = self.parcela_entry.get().strip()
        sensores_raw = self.sensores_entry.get().strip()
        sensores = [s.strip() for s in sensores_raw.split(",") if s.strip()] if sensores_raw else []
        fecha_ini = self.fecha_ini_entry.get().strip()
        fecha_fin = self.fecha_fin_entry.get().strip()
        if not parcela or not fecha_ini or not fecha_fin:
            messagebox.showwarning("Faltan datos", "Parcela y rango de fechas son obligatorios")
            return
        try:
            lecturas = svc.lecturas_en_rango(parcela, sensores, fecha_ini, fecha_fin)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return
        if not lecturas:
            messagebox.showinfo("Sin datos", "No hay lecturas para esos filtros")
            return
        df = pd.DataFrame(lecturas)
        df["valorMedido"] = df["valorMedido"].astype(float)
        df["fechaHora"] = pd.to_datetime(df["fechaHora"], format="%d-%m-%Y %H:%M:%S", errors="coerce")
        df = df.sort_values("fechaHora")

        color_map = {}
        palette = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]

        def color_for(sensor):
            if sensor not in color_map:
                color_map[sensor] = palette[len(color_map) % len(palette)]
            return color_map[sensor]

        df["color"] = df["idSensor"].apply(color_for)

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.figure = Figure(figsize=(7, 4), dpi=100)
        ax = self.figure.add_subplot(111)
        ax.scatter(df["fechaHora"], df["valorMedido"], c=df["color"])
        if not df.empty:
            ax.plot(df["fechaHora"], df["valorMedido"], color="#888888", linewidth=1.5, alpha=0.8)
        ax.set_xlabel("Fecha y Hora")
        ax.set_ylabel("Valor medido")
        ax.set_title(f"Lecturas parcela {parcela}")
        ax.tick_params(axis="x", rotation=45)
        self.figure.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=4, sticky="nsew", padx=4, pady=4)

    def limpiar(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

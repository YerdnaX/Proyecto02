import tkinter as tk
from tkinter import ttk, messagebox

from CapaNegocio import ClaseSistema as svc
from CapaVisual.helpers import _safe_get


class RiegoTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="ID Parcela").grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.parcela_entry = ttk.Entry(self, width=18)
        self.parcela_entry.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        ttk.Label(self, text="Fecha (DD-MM-YYYY)").grid(row=0, column=2, padx=4, pady=4, sticky="w")
        self.fecha_entry = ttk.Entry(self, width=18)
        self.fecha_entry.grid(row=0, column=3, padx=2, pady=2, sticky="ew")

        ttk.Button(self, text="Calcular", command=self.calcular).grid(row=1, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Refrescar historial", command=self.refresh_historial).grid(row=1, column=1, padx=4, pady=6, sticky="ew")

        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=1, column=2, columnspan=2, padx=4, pady=6, sticky="w")

        self.tree = ttk.Treeview(
            self,
            columns=("parcela", "fecha", "volumen"),
            show="headings",
            height=10,
        )
        for col, text in [("parcela", "Parcela"), ("fecha", "Fecha"), ("volumen", "Volumen")]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=140, anchor="w")
        self.tree.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=4, pady=4)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.refresh_historial()

    def calcular(self):
        pid = _safe_get(self.parcela_entry)
        fecha = _safe_get(self.fecha_entry)
        if not pid or not fecha:
            messagebox.showwarning("Falta dato", "Ingrese parcela y fecha (DD-MM-YYYY)")
            return
        try:
            resultado = svc.calcular_volumen_riego(pid, fecha)
            self.result_label.config(text=f"Volumen: {resultado['volumenRiego']}")
            self.refresh_historial()
            messagebox.showinfo("Listo", "Calculo guardado")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def refresh_historial(self):
        self.tree.delete(*self.tree.get_children())
        for c in svc.listar_calculos_riego():
            self.tree.insert("", "end", values=(c["idParcela"], c["fecha"], c["volumenRiego"]))

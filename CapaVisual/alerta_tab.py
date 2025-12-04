import tkinter as tk
from tkinter import ttk, messagebox

from CapaNegocio import ClaseSistema as svc
from CapaVisual.helpers import _safe_get


class AlertaTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(
            self,
            columns=("parcela", "sensor", "tipo", "fecha", "valor", "mensaje"),
            show="headings",
            height=10,
        )
        headings = [
            ("parcela", "Parcela"),
            ("sensor", "Sensor"),
            ("tipo", "Tipo"),
            ("fecha", "Fecha"),
            ("valor", "Valor"),
            ("mensaje", "Mensaje"),
        ]
        for col, text in headings:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=120, anchor="w")
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=4, pady=4)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        ttk.Label(self, text="ID Parcela").grid(row=1, column=0, padx=2, pady=1, sticky="w")
        self.parcela_entry = ttk.Entry(self, width=20)
        self.parcela_entry.grid(row=1, column=1, padx=2, pady=1, sticky="ew")

        ttk.Label(self, text="Fecha (DD-MM-YYYY)").grid(row=1, column=2, padx=2, pady=1, sticky="w")
        self.fecha_entry = ttk.Entry(self, width=20)
        self.fecha_entry.grid(row=1, column=3, padx=2, pady=1, sticky="ew")

        ttk.Button(self, text="Filtrar por parcela", command=self.filtrarParcela).grid(row=2, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Filtrar por parcela/fecha", command=self.filtrarParcelaFecha).grid(row=2, column=1, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Refrescar", command=self.refrescarTodo).grid(row=2, column=2, padx=4, pady=6, sticky="ew")

        self.refrescarTodo()

    def refrescarTodo(self, data=None):
        self.limpiarForm()
        self.tree.delete(*self.tree.get_children())
        alertas = data if data is not None else svc.listar_alertas()
        for a in alertas:
            self.tree.insert(
                "",
                "end",
                values=(a["idParcela"], a["idSensor"], a["tipo"], a["fechaGeneracion"], a["valorDetectado"], a["mensajeAlerta"]),
            )

    def filtrarParcela(self):
        pid = _safe_get(self.parcela_entry)
        if not pid:
            messagebox.showwarning("Falta dato", "Ingrese ID de parcela")
            return
        self.refrescarTodo(svc.alertas_por_parcela(pid))

    def filtrarParcelaFecha(self):
        pid = _safe_get(self.parcela_entry)
        fecha = _safe_get(self.fecha_entry)
        if not pid or not fecha:
            messagebox.showwarning("Falta dato", "Ingrese parcela y fecha (DD-MM-YYYY)")
            return
        self.refrescarTodo(svc.alertas_por_parcela_fecha(pid, fecha))

    def limpiarForm(self):
        self.parcela_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)

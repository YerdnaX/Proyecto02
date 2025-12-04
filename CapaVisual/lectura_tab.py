import tkinter as tk
from tkinter import ttk, messagebox

from CapaNegocio import ClaseSistema as svc
from CapaVisual.helpers import _safe_get


class LecturaTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(
            self,
            columns=("idLectura", "sensor", "parcela", "fecha", "valor"),
            show="headings",
            height=10,
        )
        for col, text in [
            ("idLectura", "ID Lectura"),
            ("sensor", "Sensor"),
            ("parcela", "Parcela"),
            ("fecha", "Fecha"),
            ("valor", "Valor"),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=130, anchor="w")
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=4, pady=4)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        labels = ["ID Lectura", "ID Sensor", "ID Parcela", "FechaHora (DD-MM-YYYY HH:MM:SS)", "Valor"]
        self.inputs = {}
        for i, label in enumerate(labels):
            ttk.Label(self, text=label).grid(row=1 + i // 2, column=(i % 2) * 2, sticky="w", padx=2, pady=1)
            entry = ttk.Entry(self, width=28)
            entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, sticky="ew", padx=2, pady=1)
            self.inputs[label] = entry

        ttk.Button(self, text="Agregar lectura", command=self.guardar).grid(row=4, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Filtrar por sensor", command=self.filtrarSensor).grid(row=4, column=1, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Filtrar por parcela", command=self.filtrarParcela).grid(row=4, column=2, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Filtrar por fecha", command=self.filtrarFecha).grid(row=4, column=3, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Borrar por parcela/fecha", command=self.eliminarporparcelafecha).grid(row=5, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Refrescar", command=self.refrescarTodo).grid(row=5, column=1, padx=4, pady=6, sticky="ew")

        self.refrescarTodo()

    def refrescarTodo(self, data=None):
        self.limpiarForm()
        self.tree.delete(*self.tree.get_children())
        lecturas = data if data is not None else svc.listar_lecturas()
        for l in lecturas:
            self.tree.insert(
                "",
                "end",
                iid=l["idLectura"],
                values=(l["idLectura"], l["idSensor"], l["idParcela"], l["fechaHora"], l["valorMedido"]),
            )

    def guardar(self):
        data = {
            "idLectura": _safe_get(self.inputs["ID Lectura"]),
            "idSensor": _safe_get(self.inputs["ID Sensor"]),
            "idParcela": _safe_get(self.inputs["ID Parcela"]),
            "fechaHora": _safe_get(self.inputs["FechaHora (DD-MM-YYYY HH:MM:SS)"]),
            "valorMedido": _safe_get(self.inputs["Valor"]),
        }
        try:
            svc.crear_lectura(data)
            messagebox.showinfo("Listo", "Lectura creada")
            self.refrescarTodo()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def filtrarSensor(self):
        sid = _safe_get(self.inputs["ID Sensor"])
        if not sid:
            messagebox.showwarning("Falta dato", "Ingrese ID de sensor")
            return
        self.refrescarTodo(svc.lecturas_por_sensor(sid))

    def filtrarParcela(self):
        pid = _safe_get(self.inputs["ID Parcela"])
        if not pid:
            messagebox.showwarning("Falta dato", "Ingrese ID de parcela")
            return
        self.refrescarTodo(svc.lecturas_por_parcela(pid))

    def filtrarFecha(self):
        fecha = _safe_get(self.inputs["FechaHora (DD-MM-YYYY HH:MM:SS)"])[:10]
        if not fecha:
            messagebox.showwarning("Falta dato", "Ingrese fecha (DD-MM-YYYY)")
            return
        self.refrescarTodo(svc.lecturas_por_fecha(fecha))

    def eliminarporparcelafecha(self):
        pid = _safe_get(self.inputs["ID Parcela"])
        fecha = _safe_get(self.inputs["FechaHora (DD-MM-YYYY HH:MM:SS)"])[:10]
        if not pid or not fecha:
            messagebox.showwarning("Falta dato", "Ingrese parcela y fecha (DD-MM-YYYY)")
            return
        try:
            borradas = svc.borrar_lecturas_parcela_fecha(pid, fecha)
            self.refrescarTodo()
            messagebox.showinfo("Listo", f"Eliminadas {borradas} lecturas")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def limpiarForm(self):
        for entry in self.inputs.values():
            entry.delete(0, tk.END)

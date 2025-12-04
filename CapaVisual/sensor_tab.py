import tkinter as tk
from tkinter import ttk, messagebox

from CapaNegocio import ClaseSistema as svc
from CapaVisual.helpers import _safe_get


class SensorTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(
            self,
            columns=("id", "tipo", "parcela", "estado", "ubicacion", "unidad", "rango"),
            show="headings",
            height=8,
        )
        headings = [
            ("id", "ID"),
            ("tipo", "Tipo"),
            ("parcela", "Parcela"),
            ("estado", "Estado"),
            ("ubicacion", "Ubicacion"),
            ("unidad", "Unidad"),
            ("rango", "Rango"),
        ]
        for col, text in headings:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=110, anchor="w")
        self.tree.bind("<<TreeviewSelect>>", self.enSeleccion)
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=4, pady=4)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        labels = ["ID", "Tipo", "ID Parcela", "Estado", "Ubicacion", "Unidad", "Rango"]
        self.inputs = {}
        for i, label in enumerate(labels):
            ttk.Label(self, text=label).grid(row=1 + i // 2, column=(i % 2) * 2, sticky="w", padx=2, pady=1)
            if label == "Tipo":
                entry = ttk.Combobox(self, values=["humedadsuelo", "temperatura", "lluvia"], width=22, state="readonly")
            elif label == "Estado":
                entry = ttk.Combobox(self, values=["activo", "inactivo", "mantenimiento", "revision"], width=22, state="readonly")
            else:
                entry = ttk.Entry(self, width=24)
            entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, sticky="ew", padx=2, pady=1)
            self.inputs[label] = entry

        ttk.Button(self, text="Crear/Actualizar", command=self.guardar).grid(row=5, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Eliminar", command=self.eliminar).grid(row=5, column=1, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Refrescar", command=self.refrescar).grid(row=5, column=2, padx=4, pady=6, sticky="ew")
        ttk.Label(self, text="Filtrar por parcela").grid(row=6, column=0, padx=2, pady=2, sticky="w")
        self.filter_entry = ttk.Entry(self, width=20)
        self.filter_entry.grid(row=6, column=1, padx=2, pady=2, sticky="ew")
        ttk.Button(self, text="Aplicar filtro", command=self.filtrarParcela).grid(row=6, column=2, padx=2, pady=2, sticky="ew")

        self.refrescar()

    def enSeleccion(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        sid = sel[0]
        for s in svc.listar_sensores():
            if s["idSensor"] == sid:
                self.llenarForm(s)
                break

    def llenarForm(self, data):
        mapping = {
            "ID": "idSensor",
            "Tipo": "tipo",
            "ID Parcela": "idParcela",
            "Estado": "estado",
            "Ubicacion": "ubicacionParcela",
            "Unidad": "unidadMedida",
            "Rango": "rangoValido",
        }
        for label, key in mapping.items():
            self.inputs[label].delete(0, tk.END)
            self.inputs[label].insert(0, data.get(key, ""))

    def filtrarParcela(self):
        pid = _safe_get(self.filter_entry)
        self.tree.delete(*self.tree.get_children())
        sensores = [s for s in svc.listar_sensores() if (not pid or s["idParcela"] == pid)]
        for s in sensores:
            self.tree.insert(
                "",
                "end",
                iid=s["idSensor"],
                values=(
                    s["idSensor"],
                    s["tipo"],
                    s["idParcela"],
                    s["estado"],
                    s["ubicacionParcela"],
                    s["unidadMedida"],
                    s["rangoValido"],
                ),
            )

    def guardar(self):
        data = {
            "idSensor": _safe_get(self.inputs["ID"]),
            "tipo": _safe_get(self.inputs["Tipo"]).lower(),
            "idParcela": _safe_get(self.inputs["ID Parcela"]),
            "estado": _safe_get(self.inputs["Estado"]).lower(),
            "ubicacionParcela": _safe_get(self.inputs["Ubicacion"]),
            "unidadMedida": _safe_get(self.inputs["Unidad"]),
            "rangoValido": _safe_get(self.inputs["Rango"]),
        }
        try:
            existing = any(s["idSensor"] == data["idSensor"] for s in svc.listar_sensores())
            if existing:
                svc.actualizar_sensor(data)
                messagebox.showinfo("Listo", "Sensor actualizado")
            else:
                svc.crear_sensor(data)
                messagebox.showinfo("Listo", "Sensor creado")
            self.refrescar()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def eliminar(self):
        sid = _safe_get(self.inputs["ID"])
        if not sid:
            messagebox.showwarning("Falta ID", "Ingrese el ID del sensor")
            return
        try:
            svc.eliminar_sensor(sid)
            self.refrescar()
            messagebox.showinfo("Listo", "Sensor eliminado")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def limpiarForm(self):
        for label, widget in self.inputs.items():
            if hasattr(widget, "set"):
                widget.set("")
            else:
                widget.delete(0, tk.END)
        self.filter_entry.delete(0, tk.END)

    def refrescar(self):
        self.limpiarForm()
        self.tree.delete(*self.tree.get_children())
        for s in svc.listar_sensores():
            self.tree.insert(
                "",
                "end",
                iid=s["idSensor"],
                values=(
                    s["idSensor"],
                    s["tipo"],
                    s["idParcela"],
                    s["estado"],
                    s["ubicacionParcela"],
                    s["unidadMedida"],
                    s["rangoValido"],
                ),
            )

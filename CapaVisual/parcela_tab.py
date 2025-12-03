import tkinter as tk
from tkinter import ttk, messagebox

from CapaNegocio import ClaseSistema as svc
from CapaVisual.helpers import _safe_get


class ParcelaTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(
            self,
            columns=("id", "nombre", "ubicacion", "cultivo", "area", "humMin", "humMax", "volumen"),
            show="headings",
            height=8,
        )
        headings = [
            ("id", "ID"),
            ("nombre", "Nombre"),
            ("ubicacion", "Ubicacion"),
            ("cultivo", "Cultivo"),
            ("area", "Area"),
            ("humMin", "Hum Min"),
            ("humMax", "Hum Max"),
            ("volumen", "Volumen"),
        ]
        for col, text in headings:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=110, anchor="w")
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=4, pady=4)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        labels = [
            "ID",
            "Nombre",
            "Ubicacion",
            "Cultivo",
            "Area",
            "Profundidad Raiz",
            "Eficiencia Riego",
            "Humbral Humedad Min",
            "Humbral Humedad Max",
            "Volumen Deseado",
        ]
        self.inputs = {}
        for i, label in enumerate(labels):
            ttk.Label(self, text=label).grid(row=1 + i // 2, column=(i % 2) * 2, sticky="w", padx=2, pady=1)
            entry = ttk.Entry(self, width=24)
            entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, sticky="ew", padx=2, pady=1)
            self.inputs[label] = entry

        ttk.Button(self, text="Crear/Actualizar", command=self.save).grid(row=6, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Eliminar", command=self.delete).grid(row=6, column=1, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Refrescar", command=self.refresh).grid(row=6, column=2, padx=4, pady=6, sticky="ew")

        self.refresh()

    def _on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        pid = sel[0]
        for p in svc.listar_parcelas():
            if p["idParcela"] == pid:
                self._fill_form(p)
                break

    def _fill_form(self, data):
        mapping = {
            "ID": "idParcela",
            "Nombre": "nombre",
            "Ubicacion": "ubicacion",
            "Cultivo": "tipoCultivo",
            "Area": "area",
            "Profundidad Raiz": "profundidadRaiz",
            "Eficiencia Riego": "eficienciaRiego",
            "Humbral Humedad Min": "umbralHumedadMin",
            "Humbral Humedad Max": "umbralHumedadMax",
            "Volumen Deseado": "volumenDeseado",
        }
        for label, key in mapping.items():
            self.inputs[label].delete(0, tk.END)
            self.inputs[label].insert(0, data.get(key, ""))

    def refresh(self):
        self._clear_form()
        self.tree.delete(*self.tree.get_children())
        for p in svc.listar_parcelas():
            self.tree.insert(
                "",
                "end",
                iid=p["idParcela"],
                values=(
                    p["idParcela"],
                    p["nombre"],
                    p["ubicacion"],
                    p["tipoCultivo"],
                    p["area"],
                    p["umbralHumedadMin"],
                    p["umbralHumedadMax"],
                    p["volumenDeseado"],
                ),
            )

    def _clear_form(self):
        for entry in self.inputs.values():
            entry.delete(0, tk.END)

    def save(self):
        data = {
            "idParcela": _safe_get(self.inputs["ID"]),
            "nombre": _safe_get(self.inputs["Nombre"]),
            "ubicacion": _safe_get(self.inputs["Ubicacion"]),
            "tipoCultivo": _safe_get(self.inputs["Cultivo"]),
            "area": _safe_get(self.inputs["Area"]),
            "profundidadRaiz": _safe_get(self.inputs["Profundidad Raiz"]),
            "eficienciaRiego": _safe_get(self.inputs["Eficiencia Riego"]),
            "umbralHumedadMin": _safe_get(self.inputs["Humbral Humedad Min"]),
            "umbralHumedadMax": _safe_get(self.inputs["Humbral Humedad Max"]),
            "volumenDeseado": _safe_get(self.inputs["Volumen Deseado"]),
        }
        try:
            existing = any(p["idParcela"] == data["idParcela"] for p in svc.listar_parcelas())
            if existing:
                svc.actualizar_parcela(data)
                messagebox.showinfo("Listo", "Parcela actualizada")
            else:
                svc.crear_parcela(data)
                messagebox.showinfo("Listo", "Parcela creada")
            self.refresh()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete(self):
        pid = _safe_get(self.inputs["ID"])
        if not pid:
            messagebox.showwarning("Falta ID", "Ingrese el ID de la parcela")
            return
        try:
            svc.eliminar_parcela(pid)
            self.refresh()
            messagebox.showinfo("Listo", "Parcela eliminada")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

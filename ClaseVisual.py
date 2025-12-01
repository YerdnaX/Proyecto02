import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from CapaNegocio import ClaseSistema as svc
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    Figure = None
    FigureCanvasTkAgg = None


def _safe_get(entry):
    return entry.get().strip()

## FRAME PARCELA
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


## FRAME SENSOR
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
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
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

        ttk.Button(self, text="Crear/Actualizar", command=self.save).grid(row=5, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Eliminar", command=self.delete).grid(row=5, column=1, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Refrescar", command=self.refresh).grid(row=5, column=2, padx=4, pady=6, sticky="ew")
        ttk.Label(self, text="Filtrar por parcela").grid(row=6, column=0, padx=2, pady=2, sticky="w")
        self.filter_entry = ttk.Entry(self, width=20)
        self.filter_entry.grid(row=6, column=1, padx=2, pady=2, sticky="ew")
        ttk.Button(self, text="Aplicar filtro", command=self.filter_by_parcela).grid(row=6, column=2, padx=2, pady=2, sticky="ew")

        self.refresh()

    def _on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        sid = sel[0]
        for s in svc.listar_sensores():
            if s["idSensor"] == sid:
                self._fill_form(s)
                break

    def _fill_form(self, data):
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

    def filter_by_parcela(self):
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

    def save(self):
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
            self.refresh()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete(self):
        sid = _safe_get(self.inputs["ID"])
        if not sid:
            messagebox.showwarning("Falta ID", "Ingrese el ID del sensor")
            return
        try:
            svc.eliminar_sensor(sid)
            self.refresh()
            messagebox.showinfo("Listo", "Sensor eliminado")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _clear_form(self):
        for label, widget in self.inputs.items():
            if hasattr(widget, "set"):
                widget.set("")
            else:
                widget.delete(0, tk.END)
        self.filter_entry.delete(0, tk.END)

    def refresh(self):
        self._clear_form()
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

### FRAME LECTURA
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

        ttk.Button(self, text="Agregar lectura", command=self.save).grid(row=4, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Filtrar por sensor", command=self.filter_sensor).grid(row=4, column=1, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Filtrar por parcela", command=self.filter_parcela).grid(row=4, column=2, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Filtrar por fecha", command=self.filter_fecha).grid(row=4, column=3, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Borrar por parcela/fecha", command=self.delete_por_parcela_fecha).grid(row=5, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Refrescar", command=self.refresh_all).grid(row=5, column=1, padx=4, pady=6, sticky="ew")

        self.refresh_all()

    def refresh_all(self, data=None):
        self._clear_form()
        self.tree.delete(*self.tree.get_children())
        lecturas = data if data is not None else svc.listar_lecturas()
        for l in lecturas:
            self.tree.insert(
                "",
                "end",
                iid=l["idLectura"],
                values=(l["idLectura"], l["idSensor"], l["idParcela"], l["fechaHora"], l["valorMedido"]),
            )

    def save(self):
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
            self.refresh_all()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def filter_sensor(self):
        sid = _safe_get(self.inputs["ID Sensor"])
        if not sid:
            messagebox.showwarning("Falta dato", "Ingrese ID de sensor")
            return
        self.refresh_all(svc.lecturas_por_sensor(sid))

    def filter_parcela(self):
        pid = _safe_get(self.inputs["ID Parcela"])
        if not pid:
            messagebox.showwarning("Falta dato", "Ingrese ID de parcela")
            return
        self.refresh_all(svc.lecturas_por_parcela(pid))

    def filter_fecha(self):
        fecha = _safe_get(self.inputs["FechaHora (DD-MM-YYYY HH:MM:SS)"])[:10]
        if not fecha:
            messagebox.showwarning("Falta dato", "Ingrese fecha (DD-MM-YYYY)")
            return
        self.refresh_all(svc.lecturas_por_fecha(fecha))

    def delete_por_parcela_fecha(self):
        pid = _safe_get(self.inputs["ID Parcela"])
        fecha = _safe_get(self.inputs["FechaHora (DD-MM-YYYY HH:MM:SS)"])[:10]
        if not pid or not fecha:
            messagebox.showwarning("Falta dato", "Ingrese parcela y fecha (DD-MM-YYYY)")
            return
        try:
            borradas = svc.borrar_lecturas_parcela_fecha(pid, fecha)
            self.refresh_all()
            messagebox.showinfo("Listo", f"Eliminadas {borradas} lecturas")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _clear_form(self):
        for entry in self.inputs.values():
            entry.delete(0, tk.END)

## FRAME XML
class XmlTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Ruta archivo XML de lecturas").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.path_entry = ttk.Entry(self, width=60)
        self.path_entry.insert(0, "./Lecturas.xml")
        self.path_entry.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Examinar", command=self.browse).grid(row=0, column=2, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Cargar lecturas XML", command=self.cargar).grid(row=1, column=0, columnspan=3, padx=6, pady=6, sticky="ew")
        self.columnconfigure(1, weight=1)

    def browse(self):
        path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml"), ("Todos", "*.*")])
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def cargar(self):
        ruta = self.path_entry.get().strip()
        try:
            nuevos = svc.cargar_lecturas_desde_xml(ruta)
            messagebox.showinfo("Listo", f"Lecturas nuevas cargadas: {nuevos}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

### FRAME GRAFICO
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
            messagebox.showerror("Dependencia faltante", "Instale matplotlib: pip install matplotlib")
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
        fechas = [l["fechaHora"] for l in lecturas]
        valores = [float(l["valorMedido"]) for l in lecturas]
        sensores_ids = [l["idSensor"] for l in lecturas]

        color_map = {}
        palette = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
        def color_for(sensor):
            if sensor not in color_map:
                color_map[sensor] = palette[len(color_map) % len(palette)]
            return color_map[sensor]
        colors = [color_for(s) for s in sensores_ids]

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.figure = Figure(figsize=(7, 4), dpi=100)
        ax = self.figure.add_subplot(111)
        ax.scatter(fechas, valores, c=colors)
        ordenados = sorted(zip(fechas, valores), key=lambda x: x[0])
        if ordenados:
            line_x, line_y = zip(*ordenados)
            ax.plot(line_x, line_y, color="#888888", linewidth=1.5, alpha=0.8)
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

### FRAME ALERTA
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

        ttk.Button(self, text="Filtrar por parcela", command=self.filter_parcela).grid(row=2, column=0, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Filtrar por parcela/fecha", command=self.filter_parcela_fecha).grid(row=2, column=1, padx=4, pady=6, sticky="ew")
        ttk.Button(self, text="Refrescar", command=self.refresh_all).grid(row=2, column=2, padx=4, pady=6, sticky="ew")

        self.refresh_all()

    def refresh_all(self, data=None):
        self._clear_form()
        self.tree.delete(*self.tree.get_children())
        alertas = data if data is not None else svc.listar_alertas()
        for a in alertas:
            self.tree.insert(
                "",
                "end",
                values=(a["idParcela"], a["idSensor"], a["tipo"], a["fechaGeneracion"], a["valorDetectado"], a["mensajeAlerta"]),
            )

    def filter_parcela(self):
        pid = _safe_get(self.parcela_entry)
        if not pid:
            messagebox.showwarning("Falta dato", "Ingrese ID de parcela")
            return
        self.refresh_all(svc.alertas_por_parcela(pid))

    def filter_parcela_fecha(self):
        pid = _safe_get(self.parcela_entry)
        fecha = _safe_get(self.fecha_entry)
        if not pid or not fecha:
            messagebox.showwarning("Falta dato", "Ingrese parcela y fecha (DD-MM-YYYY)")
            return
        self.refresh_all(svc.alertas_por_parcela_fecha(pid, fecha))

    def _clear_form(self):
        self.parcela_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)

### FRAME RIEGO
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

### APLICACION PRINCIPAL
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AgroMon")
        self.geometry("1000x700")
        apply_modern_dark(self)
        self._build_menu()
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)
        nb.add(ParcelaTab(nb), text="Parcelas")
        nb.add(SensorTab(nb), text="Sensores")
        nb.add(LecturaTab(nb), text="Lecturas")
        nb.add(AlertaTab(nb), text="Alertas")
        nb.add(RiegoTab(nb), text="Riego")
        nb.add(XmlTab(nb), text="Carga XML")
        nb.add(GraficoTab(nb), text="Graficos")

    def _build_menu(self):
        menubar = tk.Menu(self)
        datos_menu = tk.Menu(menubar, tearoff=0)
        datos_menu.add_command(label="Refrescar datos", command=svc.cargar_datos_iniciales)
        menubar.add_cascade(label="Datos", menu=datos_menu)
        menubar.add_command(label="Salir", command=self.destroy)
        self.config(menu=menubar)


def apply_modern_dark(root: tk.Tk):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    bg = "#1E1E1E"
    panel = "#242424"
    fg = "#F0F0F0"
    hover = "#505050"
    button = "#3C3C3C"
    border = "#444444"
    focus = "#5A5A5A"
    alt_row = "#2a2a2a"
    sel_bg = "#3f6ad8"
    sel_fg = "#ffffff"

    root.configure(bg=bg)

    style.configure(".", background=panel, foreground=fg, font=("Segoe UI", 10))
    style.configure("TFrame", background=panel, borderwidth=0, relief="flat")
    style.configure("TLabel", background=panel, foreground=fg)
    style.configure(
        "TButton",
        background=button,
        foreground=fg,
        borderwidth=0,
        focusthickness=1,
        focuscolor=panel,
        padding=6,
    )
    style.map(
        "TButton",
        background=[("active", hover), ("pressed", hover)],
        foreground=[("disabled", "#888888")],
    )

    style.configure(
        "TEntry",
        fieldbackground=panel,
        foreground=fg,
        bordercolor=border,
        lightcolor=focus,
        darkcolor=border,
        insertcolor=fg,
        padding=6,
    )
    style.map(
        "TEntry",
        fieldbackground=[("disabled", "#2a2a2a"), ("readonly", "#2a2a2a")],
        bordercolor=[("focus", focus)],
    )

    style.configure(
        "TCombobox",
        fieldbackground=panel,
        background=panel,
        foreground=fg,
        arrowcolor=fg,
        bordercolor=border,
        lightcolor=focus,
        darkcolor=border,
        padding=6,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", panel)],
        bordercolor=[("focus", focus)],
        arrowcolor=[("active", fg)],
    )

    style.configure(
        "Treeview",
        background=panel,
        fieldbackground=panel,
        foreground=fg,
        bordercolor=border,
        lightcolor=border,
        darkcolor=border,
        rowheight=24,
    )
    style.map(
        "Treeview",
        background=[("selected", sel_bg)],
        foreground=[("selected", sel_fg)],
    )
    style.configure("Treeview.Heading", background=panel, foreground=fg, bordercolor=border)
    style.layout(
        "Treeview",
        [
            (
                "Treeview.field",
                {
                    "sticky": "nswe",
                    "border": 0,
                    "children": [
                        ("Treeview.padding", {"sticky": "nswe", "children": [("Treeview.treearea", {"sticky": "nswe"})]})
                    ],
                },
            )
        ],
    )
    style.configure("oddrow", background=panel)
    style.configure("evenrow", background=alt_row)

    style.configure(
        "TNotebook",
        background=bg,
        borderwidth=0,
    )
    style.configure(
        "TNotebook.Tab",
        background=bg,
        foreground=fg,
        padding=(10, 5),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", panel)],
        foreground=[("selected", fg)],
    )

    style.configure(
        "Vertical.TScrollbar",
        gripcount=0,
        background=panel,
        troughcolor=bg,
        bordercolor=border,
        arrowcolor=fg,
    )
    style.map("Vertical.TScrollbar", background=[("active", hover)])
    style.configure(
        "Horizontal.TScrollbar",
        gripcount=0,
        background=panel,
        troughcolor=bg,
        bordercolor=border,
        arrowcolor=fg,
    )
    style.map("Horizontal.TScrollbar", background=[("active", hover)])


if __name__ == "__main__":
    svc.cargar_datos_iniciales()
    app = App()
    app.mainloop()

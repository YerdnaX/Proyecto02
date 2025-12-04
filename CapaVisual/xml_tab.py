import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from CapaNegocio import ClaseSistema as svc


class XmlTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Ruta archivo XML de lecturas").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.path_entry = ttk.Entry(self, width=60)
        self.path_entry.insert(0, "./Lecturas.xml")
        self.path_entry.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Examinar", command=self.buscadorRuta).grid(row=0, column=2, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Cargar lecturas XML", command=self.cargar).grid(row=1, column=0, columnspan=3, padx=6, pady=6, sticky="ew")
        self.columnconfigure(1, weight=1)

    def buscadorRuta(self):
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

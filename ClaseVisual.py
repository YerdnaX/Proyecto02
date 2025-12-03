from CapaNegocio import ClaseSistema as svc
from CapaVisual import App

__all__ = ["App"]


def run():
    svc.cargar_datos_iniciales()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    run()

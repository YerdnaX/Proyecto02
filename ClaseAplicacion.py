from CapaNegocio import ClaseSistema as svc
from CapaVisual import App

__all__ = ["run", "App"]


def run():
    svc.cargar_datos_iniciales()
    app = App()
    app.mainloop()

def main():
    run()

if __name__ == "__main__":
    main()
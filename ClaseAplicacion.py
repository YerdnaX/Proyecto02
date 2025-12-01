from CapaNegocio import ClaseSistema as svc
from ui_app import App


def main():
    svc.cargar_datos_iniciales()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
    

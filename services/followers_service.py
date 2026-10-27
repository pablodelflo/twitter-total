from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class FollowerService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path
        self.excel = app.excel


    def getFollowers(self):
        ##Esta función obtiene el listado completo de las cuentas que te siguen
        print("Vamos a obtener tus followers\n")

        #Comprobar si el fichero existe previamente o crearlo en caso contrario
        self.excel.controlExist(historicoFollowers)
        followers = []

        #Comprobamos si ya estamos en la página de followers, si no, vamos.
        if self.driver.current_url != PAGINA_FOLLOWERS:
            print(f"Primero, vamos a la página de seguidores: {PAGINA_FOLLOWERS}")
            self.driver.get(PAGINA_FOLLOWERS)

        #Recogemos el nº de followers actual para futuras comprobaciones
        
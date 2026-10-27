from pathlib import Path
from config import *
#from utils.excel import ExcelUtils
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from time import sleep
from datetime import datetime
import os
from pathlib import Path
import pandas as pd

class TwitterApp:

    def __init__(self):
        self.base_path = Path(BASE_PATH_COLECCIONES)
        self.driver = get_driver()
        #self.excel = ExcelUtils(self)

    
    def cerrar(self):
        print("\nSaliendo de la app... ¡Hasta la próxima!")
        self.driver.quit()


    def bienvenida(self, url):
        ##Esta función mostrará en pantalla el banner de bienvenida con el nombre del usuario y abrirá su perfil en TWT
        self.driver.get(url)

        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n================ TWITTER TOTAL ===================")
        print("\n* Una app en Python para gestionar tu red social *\n")
        print("==================================================")
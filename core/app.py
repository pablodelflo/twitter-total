from pathlib import Path
from config import *
from utils.excel import ExcelUtils
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
        self.excel = ExcelUtils(self)

    
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


    def full_scroll(self, pausa=2):
        ##Esta función fuerza el scroll vertical para asegurar la carga de todos los elementos (vídeos, colecciones, etc)
        # Obtener altura inicial
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Hacer scroll al final
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)

            # Comparar altura después del scroll
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                print("📉 Fin del scroll detectado, forzando scrolls adicionales...")
                
                # Hacer scrolls adicionales forzados
                for i in range(MAX_EXTRA_SCROLLS):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(SCROLL_PAUSE_TIME)
                
                # Una última comprobación
                final_height = self.driver.execute_script("return document.body.scrollHeight")
                if final_height == last_height:
                    print("✅ Scroll final confirmado.")
                    break
                else:
                    print("🔁 Scroll reactivado, continuando...")
                    last_height = final_height
            else:
                last_height = new_height

    def obtenFollowX(self):
        spanFollowers = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Seguidores')]")))
        spanFollowings = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Siguiendo')]")))
        
        # Subir al <a> contenedor y bajar al span del número
        enlace = spanFollowers.find_element(By.XPATH, "./ancestor::a")
        followers = enlace.find_element(By.XPATH, ".//span/span").text

        enlace = spanFollowings.find_element(By.XPATH, "./ancestor::a")
        followings = enlace.find_element(By.XPATH, ".//span/span").text
        
        return followers, followings
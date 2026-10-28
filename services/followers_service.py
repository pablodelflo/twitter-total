from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep

class FollowerService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path
        self.excel = app.excel


    def getFollowers(self):
        ##Esta función obtiene el listado completo de las cuentas que te siguen
        #Recogemos el nº de followers actual para futuras comprobaciones
        if self.driver.current_url != PROFILE_TWITTER:
            print("\nNecesito estar en la página de tu perfil para guardar el histórico de followers")
            self.driver.get(PROFILE_TWITTER)
            sleep(3)
        followers, followings = self.app.obtenFollowX()

        print(f"\nActualmente tienes {followers} seguidores. Ahora, obtenemos la lista.\n")

        #Comprobar si el fichero existe previamente o crearlo en caso contrario
        self.excel.controlExist(historicoFollowers)
        followers = []

        #Comprobamos si ya estamos en la página de followers, si no, vamos.
        if self.driver.current_url != PAGINA_FOLLOWERS:
            print(f"Ok, vamos a la página de seguidores: {PAGINA_FOLLOWERS}")
            self.driver.get(PAGINA_FOLLOWERS)
        
        print("\nEspera mientras obtenemos tus seguidores. Esto puede tardar algunos minutos.")
        self.app.full_scroll()

        listFollowers = self.driver.find_elements(By.CSS_SELECTOR, 'div.css-g5y9jx.r-1adg3ll.r-1ny4l3l')

        for idx, follower in enumerate(listFollowers, start=1):            
            userName = follower.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href").strip("/").split("/")[-1]
            nombreReal = follower.find_element(By.CSS_SELECTOR, "span.x1lliihq.x193iq5w").text
            link = follower.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href")
            try:
                loSigo = follower.find_element(By.CSS_SELECTOR, 'div._ap3a._aacn._aacw._aad6').text
            except:
                loSigo = ""

            if loSigo:
                estadoReciproco = "No"    
            else:
                estadoReciproco = "Si"

            followers.append([userName, nombreReal, link, estadoReciproco])
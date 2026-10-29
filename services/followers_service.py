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

    def recoger_followers(self, max_scrolls=None, pausa=3.5, max_sin_nuevos=6):
        ##Esta función obtiene el listado completo de las cuentas que te siguen
        #Recogemos el nº de followers actual para futuras comprobaciones
        if self.driver.current_url != PROFILE_TWITTER:
            print("\nNecesito estar en la página de tu perfil para guardar el histórico de followers")
            self.driver.get(PROFILE_TWITTER)
            sleep(3)
        totalActual, followings = self.app.obtenFollowX()

        print(f"\nActualmente tienes {totalActual} seguidores. Ahora, obtenemos la lista.\n")

        #Comprobar si el fichero existe previamente o crearlo en caso contrario
        self.excel.controlExist(historicoFollowers)

        #Comprobamos si ya estamos en la página de followers, si no, vamos.
        if "/followers" not in self.driver.current_url:
            print(f"Ok, vamos a la página de seguidores: {PAGINA_FOLLOWERS}")
            self.driver.get(PAGINA_FOLLOWERS)

        # Esperar a que cargue la primera fila de la lista
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, FOLLOWERUNICO))
        )

        print("\nEspera mientras obtenemos tus seguidores. Esto puede tardar algunos minutos.")

        vistos = {}   # userName -> [userName, nombreReal, link]
        sin_nuevos = 0
        scrolls = 0

        while sin_nuevos < max_sin_nuevos:
            celdas = self.driver.find_elements(By.CSS_SELECTOR, FOLLOWERUNICO)
            antes = len(vistos)

            for celda in celdas:
                try:
                    link = celda.find_element(By.CSS_SELECTOR, USERFOLLOWER).get_attribute("href")
                    userName = link.rstrip("/").split("/")[-1]
                    if userName in vistos:
                        continue
                    nombreReal = celda.find_element(By.CSS_SELECTOR, NOMBREFOLLOWER).get_attribute("textContent")
                    vistos[userName] = [userName, nombreReal, link]
                except Exception:
                    continue   # fila reciclada por X mientras la leíamos

            sin_nuevos = sin_nuevos + 1 if len(vistos) == antes else 0

            print(f"Scroll {scrolls + 1}: {len(celdas)} celdas visibles, "
                f"{len(vistos)} únicos, sin_nuevos={sin_nuevos}")

            if celdas:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'end'});", celdas[-1]
                )
            self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
            sleep(pausa)

            scrolls += 1
            if max_scrolls and scrolls >= max_scrolls:
                break

        print(f"\nRecogidos: {len(vistos)} de {totalActual} seguidores")
        for idx, (userName, nombreReal, link) in enumerate(vistos.values(), start=1):
            print(f"{idx:>3}. {nombreReal} (@{userName}) -> {link}")
        return list(vistos.values())

    '''
    def recoger_followers(self, max_scrolls=None, pausa=2.5):
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

        vistos = {}   # userName -> [userName, nombreReal, link]
        sin_nuevos = 0
        scrolls = 0

        while sin_nuevos < 3:
            celdas = self.driver.find_elements(By.CSS_SELECTOR, FOLLOWERUNICO)
            antes = len(vistos)

            for celda in celdas:
                try:
                    link = celda.find_element(By.CSS_SELECTOR, USERFOLLOWER).get_attribute("href")
                    userName = link.rstrip("/").split("/")[-1]
                    if userName in vistos:
                        continue
                    nombreReal = celda.find_element(By.CSS_SELECTOR, NOMBREFOLLOWER).get_attribute("textContent")
                    vistos[userName] = [userName, nombreReal, link]
                except Exception:
                    continue   # fila reciclada por X mientras la leíamos

            sin_nuevos = sin_nuevos + 1 if len(vistos) == antes else 0

            if celdas:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'end'});", celdas[-1]
                )
            sleep(pausa)

            scrolls += 1
            if max_scrolls and scrolls >= max_scrolls:
                break

        print(f"Recogidos: {len(vistos)}")
        for idx, (userName, nombreReal, link) in enumerate(vistos.values(), start=1):
            print(f"{idx:>3}. {nombreReal} (@{userName}) -> {link}")
        return list(vistos.values())
    '''

    '''
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
        self.app.full_scroll(max_scrolls=3) #DEPURACION
        #self.app.full_scroll()

        
        listFollowers = self.driver.find_elements(By.CSS_SELECTOR, FOLLOWERUNICO)

        for idx, follower in enumerate(listFollowers, start=1):
            nombreReal = follower.find_element(By.CSS_SELECTOR, NOMBREFOLLOWER).text
            userName = follower.find_element(By.CSS_SELECTOR, USERFOLLOWER).get_attribute("href")
            print(nombreReal)
            print(userName)
    '''
    '''
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
    '''
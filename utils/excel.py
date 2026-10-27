from config import *
from datetime import datetime
import os
import shutil
import pandas as pd

class ExcelUtils:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path


    def controlExist(self, fichero):
        if not os.path.exists(fichero):
            print("\nEl fichero excel no existe, lo creo")
            if 'Followers' in str(fichero):
                df = pd.DataFrame(columns=["Número seguidores", "Fecha comprobación"])
            elif 'Followings' in str(fichero):
                df = pd.DataFrame(columns=["Número seguidos", "Fecha comprobación"])
            df.to_excel(fichero, index=False)
import sys
from core.app import TwitterApp
from config import *
from services.followers_service import FollowerService
#from services.following_service import FollowingService
#from services.saved_service import SavedService

#Codificación de salida para la consola
sys.stdout.reconfigure(encoding='utf-8')

def main():

    app = TwitterApp()

    app.bienvenida(PROFILE_TWITTER)

    while True:
        print("\n0 - Salir de la app")
        print("1 - Herramientas para seguidores (followers)")
        print("2 - Herramientas para seguidos (followings)")
        print("3 - Comprobar último chequeo de followers")

        try:
            opcion = int(input("Elige opción: "))
            if opcion not in (0, 1, 2, 3, 4):
                raise ValueError
        except ValueError:
            print("\nDebes introducir una opción correcta. Vuelve a probar.")
            continue
        if opcion == 1:
            FollowerService(app).getFollowers()

        elif opcion == 2:
            #FollowingService(app).bannerFollowX()
            #FollowingService(app).menuFollowings()
            print("Opcion 2")

        elif opcion == 3:
            #app.excel.checkUnfollow(excelFollowers, excelFollowersOld)
            print("Opcion 3")
        
        elif opcion == 0:
            app.cerrar()
            break


if __name__ == "__main__":
    main()
import os
import shutil
import zipfile
import requests
from tqdm import tqdm

OWNER = "acierto-incomodo"
REPO = "MyJonCraft-SGS"
ZIP_NAME = "MyJonCraft-SGS.zip"
VERSION_FILE = "version.txt"

def descargar_github_file(path, save_as):
    url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/main/{path}"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(save_as, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return True
    return False

def get_latest_release_info():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    r = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
    return r.json() if r.status_code == 200 else None

def eliminar_archivos():
    folders = ["config", "defaultconfig", "emotes", "essential", "mods", "resourcepacks"]
    file = "logo.png"

    print("\nEliminando...")
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Carpeta eliminada: {folder}")
        else:
            print(f"No existe: {folder}")

    if os.path.exists(file):
        os.remove(file)
        print(f"Archivo eliminado: {file}")
    else:
        print(f"No existe: {file}")

    print("¡Hecho!\n")

def descomprimir_zip():
    temp = "Archivos Temporales"
    with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
        zip_ref.extractall(temp)

    print("\nMoviendo contenido a raiz...")
    for item in os.listdir(temp):
        src = os.path.join(temp, item)
        dst = os.path.join(os.getcwd(), item)
        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
        shutil.move(src, dst)

    shutil.rmtree(temp)
    print("¡Descomprimido completado!\n")

def menu():
    while True:
        print("===== MENU =====")
        print("1. Eliminar archivos y carpetas")
        print("2. Descargar & descomprimir desde GitHub")
        print("3. Comprobar version")
        print("4. Salir")
        opt = input("Elige (1-4): ").strip()

        if opt == "1":
            eliminar_archivos()
        elif opt == "2":
            print("\nDescargando archivos desde GitHub...")
            if descargar_github_file(ZIP_NAME, ZIP_NAME):
                print("ZIP descargado.")
                descomprimir_zip()
            else:
                print("No se pudo descargar el ZIP.")
        elif opt == "3":
            local_ver = None
            if descargar_github_file(VERSION_FILE, VERSION_FILE):
                with open(VERSION_FILE) as f:
                    local_ver = f.read().strip()

            release = get_latest_release_info()
            if release:
                latest_ver = release.get("tag_name", "")
                print(f"\nVersion local: {local_ver}")
                print(f"Ultima version: {latest_ver}")
                if local_ver == latest_ver:
                    print("Estas actualizado ✅\n")
                else:
                    print("Hay una version nueva ❗\n")
            else:
                print("Error al comprobar version.\n")

        elif opt == "4":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida.\n")

if __name__ == "__main__":
    menu()
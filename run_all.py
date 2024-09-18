import threading
import subprocess
import os
import time
from tqdm import tqdm
import shutil
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import *
import requests
import httpx
import asyncio

pasta = r"./dados"

# Verificar se a pasta existe
if os.path.exists(pasta):
    # Iterar sobre todos os itens na pasta
    for item in os.listdir(pasta):
        item_path = os.path.join(pasta, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Pasta removida: {item_path}")
        except Exception as e:
            print(f"Erro ao remover {item_path}: {e}")
else:
    print(f"A pasta {pasta} não existe.")
    
if os.path.exists(r"./dados_extraidos.docx"):
    os.remove(r"./dados_extraidos.docx")

def run_command(args):
    subprocess.run(args)

def make_req():
    cookie = ""
    pasta = r"./dados"


    commands = [
        ["python", "rodar.py", "Fonte Usina Bob 60A", cookie],
        ["python", "rodar.py", "Fonte Usina Bob 120A", cookie],
        ["python", "rodar.py", "Fonte Usina Bob 200A", cookie],
        ["python", "rodar.py", "Fonte Usina Battery Meter 50A", cookie],
        ["python", "rodar.py", "Fonte Usina Battery Meter 70A", cookie],
        ["python", "rodar.py", "Fonte Usina Battery Meter 100A", cookie],
        ["python", "rodar.py", "Fonte Usina Battery Meter 120A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 50A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 70A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 100A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 120A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 200A MONO", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 200A", cookie],
        ["python", "rodar.py", "Fonte Usina 220A", cookie],
        ["python", "rodar.py", "Carregador de Baterias Charger 60A", cookie],
    ]


    threads = []


    for cmd in commands:
        thread = threading.Thread(target=run_command, args=(cmd,))
        thread.start()
        threads.append(thread)


    for thread in tqdm(threads):
        thread.join()

    subprocess.run(["python", r"./ordenar.py"])

make_req()
    
    
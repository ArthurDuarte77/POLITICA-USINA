import requests
import keyboard
from lxml import html
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from datetime import datetime
import pygetwindow as gw
import pyautogui
import time
import re
import json
import requests
import pandas
from tqdm import tqdm

fonteBob60Marketplace = 351.00;
fonteBob60Classico = 383.00;
fonteBob60Premium = 414.00;

fonteBob120Marketplace = 476.00;
fonteBob120Classico = 517.00;
fonteBob120Premium = 559.00;

fonteBob200Marketplace = 611.00;
fonteBob200Classico = 653.00;
fonteBob200Premium = 694.00;


fonteBaterryMeter50Marketplace = 424.00;
fonteBaterryMeter50Classico = 455.00;
fonteBaterryMeter50Premium = 486.00;

fonteBaterryMeter70Marketplace = 355.00;
fonteBaterryMeter70Classico = 487.00;
fonteBaterryMeter70Premium = 517.00;

fonteBaterryMeter100Marketplace = 539.00;
fonteBaterryMeter100Classico = 580.00;
fonteBaterryMeter100Premium = 621.00;

fonteBaterryMeter120Marketplace = 600.00;
fonteBaterryMeter120Classico = 642.00;
fonteBaterryMeter120Premium = 684.00;

fonteSmart50Marketplace = 455.00;
fonteSmart50Classico = 487.00;
fonteSmart50Premium = 517.00;

fonteSmart70Marketplace = 487.00;
fonteSmart70Classico = 517.00;
fonteSmart70Premium = 548.00;

fonteSmart100Marketplace = 570.00;
fonteSmart100Classico = 611.00;
fonteSmart100Premium = 652.00;

fonteSmart120Marketplace = 632.00;
fonteSmart120Classico = 674.00;
fonteSmart120Premium = 714.00;

fonteSmart160Marketplace = 778.00;
fonteSmart160Classico = 818.00;
fonteSmart160Premium = 859.00;

fonteSmart200MonoMarketplace = 767.00;
fonteSmart200MonoClassico = 808.00;
fonteSmart200MonoPremium = 850.00;

fonteSmart200Marketplace = 798.00;
fonteSmart200Classico = 838.00;
fonteSmart200Premium = 880.00;

fonteHeavyDuty220Marketplace = 865.00;
fonteHeavyDuty220Classico = 905.00;
fonteHeavyDuty220Premium = 946.00;

fonte30Marketplace = 582.00;
fonte30Classico = 624.00;
fonte30Premium = 664.00;

fonte70Marketplace = 753.00;
fonte70Classico = 805.00;
fonte70Premium = 854.00;

fonte100Marketplace = 924.00;
fonte100Classico = 986.00;
fonte100Premium = 1046.00;

ConversorDeTensao30AMarketplace = 411.00;
ConversorDeTensao30AClassico = 452.00;
ConversorDeTensao30APremium = 492.00;

ConversorDeTensao60AMarketplace = 764.00;
ConversorDeTensao60AClassico = 805.00;
ConversorDeTensao60APremium = 885.00;

ConversorDeTensao120AMarketplace = 995.00;
ConversorDeTensao120AClassico = 1036.00;
ConversorDeTensao120APremium = 1127.00;

ConversorDeTensao240AMarketplace = 1711.00;
ConversorDeTensao240AClassico = 1761.00;
ConversorDeTensao240APremium = 1912.00;

CarregadorDeBateriasCharger60AMarketplace = 643.00;
CarregadorDeBateriasCharger60AClassico = 673.00;
CarregadorDeBateriasCharger60APremium = 734.00;

        
#"search_filters": "BRAND=2466336@category=MLB3381@", #MLB2227, 22292586

def get_diferenca(price, previsto):
    return (price / previsto) * 100;
 
options_req = [
    "Fonte Usina Bob 60A",
    "Fonte Usina Bob 120A",
    "Fonte Usina Bob 200A",
    "Fonte Usina Battery Meter 50A",
    "Fonte Usina Battery Meter 70A",
    "Fonte Usina Battery Meter 100A",
    "Fonte Usina Battery Meter 120A",
    "Fonte Usina Smart 50A",
    "Fonte Usina Smart 70A",
    "Fonte Usina Smart 100A",
    "Fonte Usina Smart 120A",
    "Fonte Usina Smart 200A MONO",
    "Fonte Usina Smart 200A",
    "Fonte Usina 220A",
    "Carregador de Baterias Charger 60A",
]
        
url = "https://app.nubimetrics.com/api/search/items"



service = Service()
options = webdriver.ChromeOptions()
titulo_arquivo = ""
# options.add_argument("--headless=new")

options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com.br/?hl=pt-BR")
time.sleep(3)
try:
    driver.get("https://app.nubimetrics.com/account/login?ReturnUrl=%2fopportunity%2fcategoryDetail#?category=MLB5672")#https://app.nubimetrics.com/opportunity/categoryDetail#?category=MLB263532
    counter = 0
    while True:
        test = driver.find_elements(By.XPATH, '//*[@id="content"]/div[1]/div/form/div/div[1]/fieldset/section[1]/label/input')
        if test:
            break
        else:
            counter += 1
            if counter > 20:
                break;
            time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/form/div/div[1]/fieldset/section[1]/label/input').send_keys("carlosbartojr@yahoo.com")
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/form/div/div[1]/fieldset/section[2]/label/input').send_keys("JFA2004")
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/form/div/footer/button').click()
except TimeoutException as e:
    print(f"Timeout ao tentar carregar a página ou encontrar um elemento: {e}")
except NoSuchElementException as e:
    print(f"Elemento não encontrado na página: {e}")
except WebDriverException as e:
    print(f"Erro no WebDriver: {e}")

driver.get("https://app.nubimetrics.com/search/layout#?op1=q-searchTypeOption3-icPubliActivas&op2=fonte%2060a%20jfa&category=")

time.sleep(5)
cookies_list = []

cookies = driver.get_cookies()
for cookie in cookies:
    objeto = cookie['name']
    value = cookie['value']
    cookies_list.append(f"{objeto}={value};")

cookies = "".join(cookies_list)
driver.quit()

headers = {
    "Cookie": cookies
}

base_params = {
    "site_id": "MLB",
    "buying_mode": "buy_it_now",
    "limit": 50,
    "offset": 0,
    "attributes": "results,available_filters,paging,filters",
    "seller_id": 1242763049,
    "order": "relevance",
    "typeSearch": "q",
    "exportData": "false",
    "language": "pt_BR",
    "isControlPrice": "true"
}
#@category=MLB3381@
#category=MLB2227@
#ITEM_CONDITION=2230284@
# Parâmetros específicos
params_list = [
    {"search_filters": "ITEM_CONDITION=2230284@"},
]

# Lista para armazenar todos os resultados filtrados
all_filtered_results = []

# Loop para cada opção e para cada conjunto de parâmetros
for option in tqdm(options_req):
    for params in params_list:
        # Atualizar o campo 'to_search' com a opção atual
        params.update(base_params)
        params['to_search'] = option

        # Inicializar offset para paginação
        offset = 0
        while True:
            params['offset'] = offset

            # Fazer a requisição GET
            try:
                response = requests.get(url, params=params, headers=headers)
            except:
                time.sleep(10)
                response = requests.get(url, params=params, headers=headers)
                

            # Verificar se a requisição foi bem-sucedida
            if response.status_code != 200:
                print(f"Erro ao fazer a requisição para {option} com {params['search_filters']}: {response.status_code}")
                break

            data = response.json()
            results = data.get('data', {}).get('results', [])
            total = data.get('data', {}).get('paging', {}).get('total', 0)

            # Filtrar os resultados
            for item in results:
                title = item.get('title', '').lower()
                price = item.get('price', float('inf'))
                real_price = item.get('original_price', float('inf'))
                link = item.get('permalink', '')
                sellernickname = item.get('sellernickname', '')
                listing_type_id = item.get('listing_type_id', '')
                if real_price:
                    real_price = float(real_price)
                
                
                if option == "Fonte Usina Bob 60A":
                    item['modelo'] = "Fonte Usina Bob 60A"
                    if "bob" in title and "usina" in title and "smart" not in title and "samrt" not in title and "battery" not in title and "meter" not in title and "24v" not in title:          
                        if "60a" in title or "60" in title or "60 amperes" in title or "60amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteBob60Premium:
                                item['diferenca'] = get_diferenca(price, fonteBob60Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBob60Premium
                                all_filtered_results.append(item) 

                            elif price < fonteBob60Classico:
                                item['diferenca'] = get_diferenca(price, fonteBob60Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBob60Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Bob 120A":
                    item['modelo'] = "Fonte Usina Bob 120A"
                    if "bob" in title and "usina" in title and "smart" not in title and "samrt" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                        if "120a" in title or "120" in title or "120 amperes" in title or "120amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteBob120Premium:
                                item['diferenca'] = get_diferenca(price, fonteBob120Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBob120Premium
                                all_filtered_results.append(item) 

                            elif price < fonteBob120Classico:
                                item['diferenca'] = get_diferenca(price, fonteBob120Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBob120Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Bob 200A":
                    item['modelo'] = "Fonte Usina Bob 200A"
                    if "bob" in title and "usina" in title and "smart" not in title and "samrt" not in title and "battery" not in title and "meter" not in title and "24v" not in title and "24v" not in title:
                        if "200a" in title or "200" in title or "200 amperes" in title or "200amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteBob200Premium:
                                item['diferenca'] = get_diferenca(price, fonteBob200Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBob200Premium
                                all_filtered_results.append(item) 

                            elif price < fonteBob200Classico:
                                item['diferenca'] = get_diferenca(price, fonteBob200Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBob200Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Battery Meter 50A":
                    item['modelo'] = "Fonte Usina Battery Meter 50A"
                    if "usina" in title and "battery" in title and "meter" in title and "bob" not in title and "24v" not in title:
                        if "50a" in title or "50" in title or "50 amperes" in title or "50amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteBaterryMeter50Premium:
                                item['diferenca'] = get_diferenca(price, fonteBaterryMeter50Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBaterryMeter50Premium
                                all_filtered_results.append(item) 

                            elif price < fonteBaterryMeter50Classico:
                                item['diferenca'] = get_diferenca(price, fonteBaterryMeter50Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBaterryMeter50Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Battery Meter 70A":
                    item['modelo'] = "Fonte Usina Battery Meter 70A"
                    if "usina" in title and "battery" in title and "meter" in title and "bob" not in title and "24v" not in title:
                        if "70a" in title or "70" in title or "70 amperes" in title or "70amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteBaterryMeter70Premium:
                                item['diferenca'] = get_diferenca(price, fonteBaterryMeter70Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBaterryMeter70Premium
                                all_filtered_results.append(item) 

                            elif price < fonteBaterryMeter70Classico:
                                item['diferenca'] = get_diferenca(price, fonteBaterryMeter70Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBaterryMeter70Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Battery Meter 100A":
                    item['modelo'] = "Fonte Usina Battery Meter 100A"
                    if "usina" in title and "battery" in title and "meter" in title and "bob" not in title and "24v" not in title:
                        if "100a" in title or "100" in title or "100 amperes" in title or "100amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteBaterryMeter100Premium:
                                item['diferenca'] = get_diferenca(price, fonteBaterryMeter100Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBaterryMeter100Premium
                                all_filtered_results.append(item) 

                            elif price < fonteBaterryMeter100Classico:
                                item['diferenca'] = get_diferenca(price, fonteBaterryMeter100Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBaterryMeter100Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Battery Meter 120A":
                    item['modelo'] = "Fonte Usina Battery Meter 120A"
                    if "usina" in title and "battery" in title and "meter" in title and "bob" not in title and "24v" not in title:
                        if "120a" in title or "120" in title or "120 amperes" in title or "120amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteBaterryMeter120Premium:
                                item['diferenca'] = get_diferenca(price, fonteBaterryMeter120Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBaterryMeter120Premium
                                all_filtered_results.append(item) 

                            elif price < fonteBaterryMeter120Classico:
                                item['diferenca'] = get_diferenca(price, fonteBaterryMeter120Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteBaterryMeter120Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Smart 50A":
                    item['modelo'] = "Fonte Usina Smart 50A"
                    if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                        if "50a" in title or "50" in title or "50 amperes" in title or "50amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteSmart50Premium:
                                item['diferenca'] = get_diferenca(price, fonteSmart50Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart50Premium
                                all_filtered_results.append(item) 

                            elif price < fonteSmart50Classico:
                                item['diferenca'] = get_diferenca(price, fonteSmart50Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart50Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Smart 70A":
                    item['modelo'] = "Fonte Usina Smart 70A"
                    if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                        if "70a" in title or "70" in title or "70 amperes" in title or "70amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteSmart70Premium:
                                item['diferenca'] = get_diferenca(price, fonteSmart70Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart70Premium
                                all_filtered_results.append(item) 

                            elif price < fonteSmart70Classico:
                                item['diferenca'] = get_diferenca(price, fonteSmart70Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart70Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Smart 100A":
                    item['modelo'] = "Fonte Usina Smart 100A"
                    if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                        if "100a" in title or "100" in title or "100 amperes" in title or "100amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteSmart100Premium:
                                item['diferenca'] = get_diferenca(price, fonteSmart100Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart100Premium
                                all_filtered_results.append(item) 

                            elif price < fonteSmart100Classico:
                                item['diferenca'] = get_diferenca(price, fonteSmart100Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart100Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Smart 120A":
                    item['modelo'] = "Fonte Usina Smart 120A"
                    if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                        if "120a" in title or "120" in title or "120 amperes" in title or "120amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteSmart120Premium:
                                item['diferenca'] = get_diferenca(price, fonteSmart120Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart120Premium
                                all_filtered_results.append(item) 

                            elif price < fonteSmart120Classico:
                                item['diferenca'] = get_diferenca(price, fonteSmart120Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart120Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Smart 160A":
                    item['modelo'] = "Fonte Usina Smart 160A"
                    if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                        if "160a" in title or "160" in title or "160 amperes" in title or "160amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteSmart160Premium:
                                item['diferenca'] = get_diferenca(price, fonteSmart160Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart160Premium
                                all_filtered_results.append(item) 

                            elif price < fonteSmart160Classico:
                                item['diferenca'] = get_diferenca(price, fonteSmart160Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart160Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Smart 200A MONO":
                    item['modelo'] = "Fonte Usina Smart 200A MONO"
                    if "usina" in title and ("smart" in title or "samrt" in title) and ("mono" in title or "220v" in title or "monovolt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                        if "200a" in title or "200" in title or "200 amperes" in title or "200amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteSmart200MonoPremium:
                                item['diferenca'] = get_diferenca(price, fonteSmart200MonoPremium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart200MonoPremium
                                all_filtered_results.append(item) 

                            elif price < fonteSmart200MonoClassico:
                                item['diferenca'] = get_diferenca(price, fonteSmart200MonoClassico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart200MonoClassico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina Smart 200A":
                    item['modelo'] = "Fonte Usina Smart 200A"
                    if "usina" in title and ("samrt" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                        if "200a" in title or "200" in title or "200 amperes" in title or "200amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteSmart200Premium:
                                item['diferenca'] = get_diferenca(price, fonteSmart200Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart200Premium
                                all_filtered_results.append(item) 

                            elif price < fonteSmart200Classico:
                                item['diferenca'] = get_diferenca(price, fonteSmart200Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteSmart200Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina 220A":
                    item['modelo'] = "Fonte Usina 220A"
                    if "usina" in title and "bob" not in title and "battery" not in title and "meter" not in title and "smart" not in title and "samrt" not in title and "24v" not in title:
                        if "220a" in title or "220" in title or "220 amperes" in title or "220amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonteHeavyDuty220Premium:
                                item['diferenca'] = get_diferenca(price, fonteHeavyDuty220Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteHeavyDuty220Premium
                                all_filtered_results.append(item) 

                            elif price < fonteHeavyDuty220Classico:
                                item['diferenca'] = get_diferenca(price, fonteHeavyDuty220Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonteHeavyDuty220Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina 30A":
                    item['modelo'] = "Fonte Usina 30A"
                    if "usina" in title and "bob" not in title and "battery" not in title and "meter" not in title and "smart" not in title and "samrt" not in title and "24v" in title:
                        if "30a" in title or "30" in title or "30 amperes" in title or "30amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonte30Premium:
                                item['diferenca'] = get_diferenca(price, fonte30Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonte30Premium
                                all_filtered_results.append(item) 

                            elif price < fonte30Classico:
                                item['diferenca'] = get_diferenca(price, fonte30Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonte30Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina 70A":
                    item['modelo'] = "Fonte Usina 70A"
                    if "usina" in title and "bob" not in title and "battery" not in title and "meter" not in title and "smart" not in title and "samrt" not in title and "24v" in title:
                        if "70a" in title or "70" in title or "70 amperes" in title or "70amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonte70Premium:
                                item['diferenca'] = get_diferenca(price, fonte70Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonte70Premium
                                all_filtered_results.append(item) 

                            elif price < fonte70Classico:
                                item['diferenca'] = get_diferenca(price, fonte70Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonte70Classico
                                all_filtered_results.append(item)
                
                
                if option == "Fonte Usina 100A":
                    item['modelo'] = "Fonte Usina 100A"
                    if "usina" in title and "bob" not in title and "battery" not in title and "meter" not in title and "smart" not in title and "samrt" not in title and "24v" in title:
                        if "100a" in title or "100" in title or "100 amperes" in title or "100amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < fonte100Premium:
                                item['diferenca'] = get_diferenca(price, fonte100Premium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonte100Premium
                                all_filtered_results.append(item) 

                            elif price < fonte100Classico:
                                item['diferenca'] = get_diferenca(price, fonte100Classico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = fonte100Classico
                                all_filtered_results.append(item)
                
                
                if option == "Conversor de Tensao 30A":
                    item['modelo'] = "Conversor de Tensao 30A"
                    if "usina" in title and "conversor" in title:
                        if "30a" in title or "30" in title or "30 amperes" in title or "30amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < ConversorDeTensao30APremium:
                                item['diferenca'] = get_diferenca(price, ConversorDeTensao30APremium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = ConversorDeTensao30APremium
                                all_filtered_results.append(item) 

                            elif price < ConversorDeTensao30AClassico:
                                item['diferenca'] = get_diferenca(price, ConversorDeTensao30AClassico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = ConversorDeTensao30AClassico
                                all_filtered_results.append(item)
                
                
                if option == "Conversor de Tensao 60A":
                    item['modelo'] = "Conversor de Tensao 60A"
                    if "usina" in title and "conversor" in title:
                        if "60a" in title or "60" in title or "60 amperes" in title or "60amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < ConversorDeTensao60APremium:
                                item['diferenca'] = get_diferenca(price, ConversorDeTensao60APremium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = ConversorDeTensao60APremium
                                all_filtered_results.append(item) 

                            elif price < ConversorDeTensao60AClassico:
                                item['diferenca'] = get_diferenca(price, ConversorDeTensao60AClassico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = ConversorDeTensao60AClassico
                                all_filtered_results.append(item)
                
                
                if option == "Conversor de Tensao 120A":
                    item['modelo'] = "Conversor de Tensao 120A"
                    if "usina" in title and "conversor" in title:
                        if "120a" in title or "120" in title or "120 amperes" in title or "120amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < ConversorDeTensao120APremium:
                                item['diferenca'] = get_diferenca(price, ConversorDeTensao120APremium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = ConversorDeTensao120APremium
                                all_filtered_results.append(item) 

                            elif price < ConversorDeTensao120AClassico:
                                item['diferenca'] = get_diferenca(price, ConversorDeTensao120AClassico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = ConversorDeTensao120AClassico
                                all_filtered_results.append(item)
                
                
                if option == "Conversor de Tensao 240A":
                    item['modelo'] = "Conversor de Tensao 240A"
                    if "usina" in title and "conversor" in title:
                        if "240a" in title or "240" in title or "240 amperes" in title or "240amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < ConversorDeTensao240APremium:
                                item['diferenca'] = get_diferenca(price, ConversorDeTensao240APremium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = ConversorDeTensao240APremium
                                all_filtered_results.append(item) 

                            elif price < ConversorDeTensao240AClassico:
                                item['diferenca'] = get_diferenca(price, ConversorDeTensao240AClassico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = ConversorDeTensao240AClassico
                                all_filtered_results.append(item)
                
                
                if option == "Carregador de Baterias Charger 60A":
                    item['modelo'] = "Carregador de Baterias Charger 60A"
                    if "usina" in title and "charger" in title and "24v" not in title:
                        if "60a" in title or "60" in title or "60 amperes" in title or "60amperes" in title:
                            # isWrong = False
                            # for attribute in item['attributes']:
                            #     if "bob" in attribute.lower() or "lite" in attribute.lower():
                            #         isWrong = True
                            # if isWrong:
                            #     continue
                            if listing_type_id == "gold_pro" and price < CarregadorDeBateriasCharger60APremium:
                                item['diferenca'] = get_diferenca(price, CarregadorDeBateriasCharger60APremium)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = CarregadorDeBateriasCharger60APremium
                                all_filtered_results.append(item) 

                            elif price < CarregadorDeBateriasCharger60AClassico:
                                item['diferenca'] = get_diferenca(price, CarregadorDeBateriasCharger60AClassico)
                                if item['diferenca'] < 70:
                                    continue
                                item['price_previsto'] = CarregadorDeBateriasCharger60AClassico
                                all_filtered_results.append(item)

                    

            # Atualizar o offset para a próxima página
            offset += params['limit']

            # Verificar se todos os itens foram processados
            if offset >= total:
                break

def get_loja(loja):
    # Formatar a URL com o nome da loja
    location_url = f'https://www.mercadolivre.com.br/perfil/{loja.replace(" ", "+")}'
    
    # Fazer a requisição HTTP
    response = requests.get(location_url)
    
    if response.status_code == 200:
        # Parsear o conteúdo HTML da resposta
        tree = html.fromstring(response.content)
        
        # Extrair o texto do elemento especificado pelo XPath
        loja_info = tree.xpath('//*[@id="profile"]/div/div[2]/div[1]/div[3]/p/font/font/text()')
        
        if loja_info:
            return loja_info[0].strip() 
        else:
            return "Informação não encontrada"
    else:
        return f"Erro ao acessar a página: {response.status_cod}"
    

def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Bom dia!"
    elif 12 <= current_hour < 18:
        return "Boa tarde!"
    else:
        return "Boa noite!"

def enviar(grouped_by_seller):
    requests.post("http://localhost:3000/api/sendText", {
        "chatId": "120363319076884647@g.us",
        "text": f"{get_greeting()} \n Segue anúncios fora da política",
        "session": "default"
    })
    try:
        for seller, items in grouped_by_seller.items():
            dados = f"*{seller}* \n"
            time.sleep(1)
            for item in items:
                if item['listing_type'] == "gold_special":
                    item['listing_type'] = "Clássico"
                else:
                    item['listing_type'] = "Premium"
                
                loja_info = get_loja(item['seller'])
                dados =  dados + f"{item['model']} - {item['seller']} - {loja_info} - Preço Anúncio: {item['price']} - Preço Política: {item['predicted_price']} ({item['listing_type']}) \n {item['link']} \n"
            requests.post("http://localhost:3000/api/sendText", {
            "chatId": "120363319076884647@g.us",
            "text": dados,
            "session": "default"
            })
    except Exception as e:
        print(f"Erro ao enviar mensagens: {e}")


formatted_results = [
    {
        "image": result['thumbnail'],
        "model": result['modelo'],
        "seller": result['sellernickname'],
        "title": result['title'],
        "price": result['price'],   
        "predicted_price": result['price_previsto'],
        "listing_type": result['listing_type_id'],
        "link": result['permalink'],
    }
    for result in all_filtered_results
]

# requests.delete('https://expertinvest.com.br/api/v1/politica-usina/deletar-todos')
# time.sleep(5)

# for result in formatted_results:
#     response = requests.post('https://expertinvest.com.br/api/v1/politica-usina', json=result)
#     if response.status_code != 200:
#         print(f"Erro ao enviar dados para a API: {response.status_code}")

grouped_by_seller = defaultdict(list)

for item in formatted_results:
    seller = item['seller']
    grouped_by_seller[seller].append(item)
    
grouped_by_seller = dict(grouped_by_seller)
    
enviar(grouped_by_seller)




# Salva os dados em um arquivo JSON
# with open('filtered_results.json', 'w', encoding='utf-8') as json_file:
#     json.dump(formatted_results, json_file, ensure_ascii=False, indent=4)

# print("Dados salvos em 'filtered_results.json'")


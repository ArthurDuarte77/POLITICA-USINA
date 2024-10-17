import requests
import keyboard
from lxml import html
from collections import defaultdict
from datetime import datetime
import schedule
import time
import subprocess
import requests
import pandas
from tqdm import tqdm

fonteBob60Marketplace = 316.00;
fonteBob60Classico = 345.00;
fonteBob60Premium = 373.00;

fonteBob120Marketplace = 428.00;
fonteBob120Classico = 465.00;
fonteBob120Premium = 503.00;

fonteBob200Marketplace = 550.00;
fonteBob200Classico = 588.00;
fonteBob200Premium = 625.00;


fonteBaterryMeter50Marketplace = 382.00;
fonteBaterryMeter50Classico = 410.00;
fonteBaterryMeter50Premium = 437.00;

fonteBaterryMeter70Marketplace = 410.00;
fonteBaterryMeter70Classico = 438.00;
fonteBaterryMeter70Premium = 465.00;

fonteBaterryMeter100Marketplace = 485.00;
fonteBaterryMeter100Classico = 522.00;
fonteBaterryMeter100Premium = 559.00;

fonteBaterryMeter120Marketplace = 540.00;
fonteBaterryMeter120Classico = 578.00;
fonteBaterryMeter120Premium = 616.00;

fonteSmart50Marketplace = 410.00;
fonteSmart50Classico = 438.00;
fonteSmart50Premium = 465.00;

fonteSmart70Marketplace = 438.00;
fonteSmart70Classico = 465.00;
fonteSmart70Premium = 493.00;

fonteSmart100Marketplace = 513.00;
fonteSmart100Classico = 550.00;
fonteSmart100Premium = 587.00;

fonteSmart120Marketplace = 569.00;
fonteSmart120Classico = 607.00;
fonteSmart120Premium = 643.00;

fonteSmart160Marketplace = 700.00;
fonteSmart160Classico = 736.00;
fonteSmart160Premium = 773.00;

fonteSmart200MonoMarketplace = 690.00;
fonteSmart200MonoClassico = 727.00;
fonteSmart200MonoPremium = 765.00;

fonteSmart200Marketplace = 718.00;
fonteSmart200Classico = 754.00;
fonteSmart200Premium = 792.00;

fonteHeavyDuty220Marketplace = 779.00;
fonteHeavyDuty220Classico = 815.00;
fonteHeavyDuty220Premium = 851.00;

fonte30Marketplace = 524.00;
fonte30Classico = 562.00;
fonte30Premium = 598.00;

fonte70Marketplace = 678.00;
fonte70Classico = 725.00;
fonte70Premium = 769.00;

fonte100Marketplace = 832.00;
fonte100Classico = 887.00;
fonte100Premium = 941.00;

ConversorDeTensao30AMarketplace = 370.00;
ConversorDeTensao30AClassico = 407.00;
ConversorDeTensao30APremium = 443.00;

ConversorDeTensao60AMarketplace = 688.00;
ConversorDeTensao60AClassico = 725.00;
ConversorDeTensao60APremium = 797.00;

ConversorDeTensao120AMarketplace = 896.00;
ConversorDeTensao120AClassico = 932.00;
ConversorDeTensao120APremium = 1014.00;

ConversorDeTensao240AMarketplace = 1540.00;
ConversorDeTensao240AClassico = 1585.00;
ConversorDeTensao240APremium = 1721.00;

CarregadorDeBateriasCharger60AMarketplace = 596.00;
CarregadorDeBateriasCharger60AClassico = 692.00;
CarregadorDeBateriasCharger60APremium = 754.00;

        
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


def get_loja(loja):
    response = requests.get(f"https://api.mercadolibre.com/sites/MLB/search?nickname={loja}")
    user_id = response.json()['results'][0]['seller']['id']
    user_response = requests.get(f"https://api.mercadolibre.com/users/{user_id}")
    address = user_response.json()['address']['city']
    state = user_response.json()['address']['state']
    return address + " - " + state
    

def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Bom dia!"
    elif 12 <= current_hour < 18:
        return "Boa tarde!"
    else:
        return "Boa noite!"

def enviar(grouped_by_seller):
    requests.post("http://172.16.34.205:3000/api/sendText", {
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
            requests.post("http://172.16.34.205:3000/api/sendText", {
            "chatId": "120363319076884647@g.us",
            "text": dados,
            "session": "default"
            })
    except Exception as e:
        print(f"Erro ao enviar mensagens: {e}")


def politica():
        
    urls = [
        "https://api.mercadolibre.com/sites/MLB/search?ITEM_CONDITION=2230284",
    ]

    # Lista para armazenar todos os resultados filtrados
    all_filtered_results = []

    for option in tqdm(options_req):
        for url in urls:
            # Atualizar parâmetros com a opção atual
            params = {"q": option}

            # Inicializar offset para paginação
            offset = 0
            while True:
                # Atualizar parâmetros com o offset atual
                params['offset'] = offset

                # Fazer a requisição GET
                try:
                    response = requests.get(url, params=params)
                except Exception as e:
                    # Tentar novamente após 10 segundos em caso de erro
                    time.sleep(10)
                    response = requests.get(url, params=params)
                    print(f"Erro ao fazer a requisição para {option}: {e}")

                # Verificar se a requisição foi bem-sucedida
                if response.status_code != 200:
                    print(f"Erro ao fazer a requisição para {option} com {params}: {response.status_code}")
                    break

                data = response.json()
                results = data.get('results', [])
                total = data.get('paging', {}).get('total', 0)
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonteBob60Premium:
                                    item['diferenca'] = get_diferenca(price, fonteBob60Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteBob60Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteBob60Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonteBob120Premium:
                                    item['diferenca'] = get_diferenca(price, fonteBob120Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteBob120Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteBob120Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonteBob200Premium:
                                    item['diferenca'] = get_diferenca(price, fonteBob200Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteBob200Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteBob200Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonteBaterryMeter50Premium:
                                    item['diferenca'] = get_diferenca(price, fonteBaterryMeter50Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteBaterryMeter50Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteBaterryMeter50Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonteBaterryMeter70Premium:
                                    item['diferenca'] = get_diferenca(price, fonteBaterryMeter70Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteBaterryMeter70Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteBaterryMeter70Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonteBaterryMeter100Premium:
                                    item['diferenca'] = get_diferenca(price, fonteBaterryMeter100Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteBaterryMeter100Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteBaterryMeter100Classico:
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
                                #     if "battery" in attribute['value_name'].lower() or "meter" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonteBaterryMeter120Premium:
                                    item['diferenca'] = get_diferenca(price, fonteBaterryMeter120Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteBaterryMeter120Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteBaterryMeter120Classico:
                                    item['diferenca'] = get_diferenca(price, fonteBaterryMeter120Classico)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteBaterryMeter120Classico
                                    all_filtered_results.append(item)
                    
                    
                    if option == "Fonte Usina Smart 50A":
                        item['modelo'] = "Fonte Usina Smart 50A"
                        if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                            if "50a" in title or "50" in title or "50 amperes" in title or "50amperes" in title:
                                isWrong = False
                                for attribute in item['attributes']:
                                    if attribute['value_name'] is not None:
                                        if "battery" in attribute['value_name'].lower() or "meter" in attribute['value_name'].lower():
                                            isWrong = True
                                if isWrong:
                                    continue
                                if listing_type_id == "gold_pro" and price < fonteSmart50Premium:
                                    item['diferenca'] = get_diferenca(price, fonteSmart50Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart50Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteSmart50Classico:
                                    item['diferenca'] = get_diferenca(price, fonteSmart50Classico)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart50Classico
                                    all_filtered_results.append(item)
                    
                    
                    if option == "Fonte Usina Smart 70A":
                        item['modelo'] = "Fonte Usina Smart 70A"
                        if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                            if "70a" in title or "70" in title or "70 amperes" in title or "70amperes" in title:
                                isWrong = False
                                for attribute in item['attributes']:
                                    if attribute['value_name'] is not None:
                                        if "battery" in attribute['value_name'].lower() or "meter" in attribute['value_name'].lower():
                                            isWrong = True
                                if isWrong:
                                    continue
                                if listing_type_id == "gold_pro" and price < fonteSmart70Premium:
                                    item['diferenca'] = get_diferenca(price, fonteSmart70Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart70Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteSmart70Classico:
                                    item['diferenca'] = get_diferenca(price, fonteSmart70Classico)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart70Classico
                                    all_filtered_results.append(item)
                    
                    
                    if option == "Fonte Usina Smart 100A":
                        item['modelo'] = "Fonte Usina Smart 100A"
                        if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                            if "100a" in title or "100" in title or "100 amperes" in title or "100amperes" in title:
                                isWrong = False
                                for attribute in item['attributes']:
                                    if attribute['value_name'] is not None:
                                        if "battery" in attribute['value_name'].lower() or "meter" in attribute['value_name'].lower():
                                            isWrong = True
                                if isWrong:
                                    continue
                                if listing_type_id == "gold_pro" and price < fonteSmart100Premium:
                                    item['diferenca'] = get_diferenca(price, fonteSmart100Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart100Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteSmart100Classico:
                                    item['diferenca'] = get_diferenca(price, fonteSmart100Classico)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart100Classico
                                    all_filtered_results.append(item)
                    
                    
                    if option == "Fonte Usina Smart 120A":
                        item['modelo'] = "Fonte Usina Smart 120A"
                        if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                            if "120a" in title or "120" in title or "120 amperes" in title or "120amperes" in title:
                                isWrong = False
                                for attribute in item['attributes']:
                                    if attribute['value_name'] is not None:
                                        if "battery" in attribute['value_name'].lower() or "meter" in attribute['value_name'].lower():
                                            isWrong = True
                                if isWrong:
                                    continue
                                if listing_type_id == "gold_pro" and price < fonteSmart120Premium:
                                    item['diferenca'] = get_diferenca(price, fonteSmart120Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart120Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteSmart120Classico:
                                    item['diferenca'] = get_diferenca(price, fonteSmart120Classico)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart120Classico
                                    all_filtered_results.append(item)
                    
                    
                    if option == "Fonte Usina Smart 160A":
                        item['modelo'] = "Fonte Usina Smart 160A"
                        if "usina" in title and ("smart" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                            if "160a" in title or "160" in title or "160 amperes" in title or "160amperes" in title:
                                isWrong = False
                                for attribute in item['attributes']:
                                    if attribute['value_name'] is not None:
                                        if "battery" in attribute['value_name'].lower() or "meter" in attribute['value_name'].lower():
                                            isWrong = True
                                if isWrong:
                                    continue
                                if listing_type_id == "gold_pro" and price < fonteSmart160Premium:
                                    item['diferenca'] = get_diferenca(price, fonteSmart160Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart160Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteSmart160Classico:
                                    item['diferenca'] = get_diferenca(price, fonteSmart160Classico)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart160Classico
                                    all_filtered_results.append(item)
                    
                    
                    if option == "Fonte Usina Smart 200A MONO":
                        item['modelo'] = "Fonte Usina Smart 200A MONO"
                        if "usina" in title and ("smart" in title or "samrt" in title) and ("mono" in title or "220v" in title or "monovolt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                            if "200a" in title or "200" in title or "200 amperes" in title or "200amperes" in title:
                                isWrong = False
                                for attribute in item['attributes']:
                                    if attribute['value_name'] is not None:
                                        if "battery" in attribute['value_name'].lower() or "meter" in attribute['value_name'].lower():
                                            isWrong = True
                                if isWrong:
                                    continue
                                if listing_type_id == "gold_pro" and price < fonteSmart200MonoPremium:
                                    item['diferenca'] = get_diferenca(price, fonteSmart200MonoPremium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart200MonoPremium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteSmart200MonoClassico:
                                    item['diferenca'] = get_diferenca(price, fonteSmart200MonoClassico)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart200MonoClassico
                                    all_filtered_results.append(item)
                    
                    
                    if option == "Fonte Usina Smart 200A":
                        item['modelo'] = "Fonte Usina Smart 200A"
                        if "usina" in title and ("samrt" in title or "samrt" in title) and "bob" not in title and "battery" not in title and "meter" not in title and "24v" not in title:
                            if "200a" in title or "200" in title or "200 amperes" in title or "200amperes" in title:
                                isWrong = False
                                for attribute in item['attributes']:
                                    if attribute['value_name'] is not None:
                                        if "battery" in attribute['value_name'].lower() or "meter" in attribute['value_name'].lower():
                                            isWrong = True
                                if isWrong:
                                    continue
                                if listing_type_id == "gold_pro" and price < fonteSmart200Premium:
                                    item['diferenca'] = get_diferenca(price, fonteSmart200Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteSmart200Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteSmart200Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonteHeavyDuty220Premium:
                                    item['diferenca'] = get_diferenca(price, fonteHeavyDuty220Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonteHeavyDuty220Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonteHeavyDuty220Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonte30Premium:
                                    item['diferenca'] = get_diferenca(price, fonte30Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonte30Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonte30Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonte70Premium:
                                    item['diferenca'] = get_diferenca(price, fonte70Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonte70Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonte70Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < fonte100Premium:
                                    item['diferenca'] = get_diferenca(price, fonte100Premium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = fonte100Premium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < fonte100Classico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < ConversorDeTensao30APremium:
                                    item['diferenca'] = get_diferenca(price, ConversorDeTensao30APremium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = ConversorDeTensao30APremium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < ConversorDeTensao30AClassico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < ConversorDeTensao60APremium:
                                    item['diferenca'] = get_diferenca(price, ConversorDeTensao60APremium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = ConversorDeTensao60APremium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < ConversorDeTensao60AClassico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < ConversorDeTensao120APremium:
                                    item['diferenca'] = get_diferenca(price, ConversorDeTensao120APremium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = ConversorDeTensao120APremium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < ConversorDeTensao120AClassico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < ConversorDeTensao240APremium:
                                    item['diferenca'] = get_diferenca(price, ConversorDeTensao240APremium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = ConversorDeTensao240APremium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < ConversorDeTensao240AClassico:
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
                                #     if "bob" in attribute['value_name'].lower() or "lite" in attribute['value_name'].lower():
                                #         isWrong = True
                                # if isWrong:
                                #     continue
                                if listing_type_id == "gold_pro" and price < CarregadorDeBateriasCharger60APremium:
                                    item['diferenca'] = get_diferenca(price, CarregadorDeBateriasCharger60APremium)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = CarregadorDeBateriasCharger60APremium
                                    all_filtered_results.append(item) 

                                elif listing_type_id == "gold_special" and  price < CarregadorDeBateriasCharger60AClassico:
                                    item['diferenca'] = get_diferenca(price, CarregadorDeBateriasCharger60AClassico)
                                    if item['diferenca'] < 70:
                                        continue
                                    item['price_previsto'] = CarregadorDeBateriasCharger60AClassico
                                    all_filtered_results.append(item)

                        

                # Atualizar o offset para a próxima página
                offset += 50

                # Verificar se todos os itens foram processados
                if offset >= total:
                    break
                
    formatted_results = [
        {
            "image": result['thumbnail'],
            "model": result['modelo'],
            "seller": result['seller']['nickname'],
            "title": result['title'],
            "price": result['price'],   
            "predicted_price": result['price_previsto'],
            "listing_type": result['listing_type_id'],
            "link": result['permalink'],
        }
        for result in all_filtered_results
    ]
    
    grouped_by_seller = defaultdict(list)

    for item in formatted_results:
        seller = item['seller']
        grouped_by_seller[seller].append(item)
        
    grouped_by_seller = dict(grouped_by_seller)
        
    enviar(grouped_by_seller)

    
    # with open('filtered_results.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(formatted_results, json_file, ensure_ascii=False, indent=4)

    # print("Dados salvos em 'filtered_results.json'")


def executar_codigo():
    politica()

# Agendar a execução nos horários especificados
schedule.every().day.at("07:40").do(executar_codigo)

while True:
    schedule.run_pending()
    time.sleep(60) 
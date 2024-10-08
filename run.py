from datetime import datetime
import schedule
import time
import subprocess

def executar_codigo():
    subprocess.run(['python', 'main.py'])

# Agendar a execução nos horários especificados
schedule.every().day.at("07:50").do(executar_codigo)
schedule.every().day.at("10:50").do(executar_codigo)
schedule.every().day.at("13:50").do(executar_codigo)
schedule.every().day.at("15:50").do(executar_codigo)
schedule.every().day.at("19:50").do(executar_codigo)
schedule.every().day.at("23:50").do(executar_codigo)

while True:
    schedule.run_pending()
    time.sleep(60) 
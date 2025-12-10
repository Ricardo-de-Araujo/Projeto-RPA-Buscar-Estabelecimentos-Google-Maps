import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.path_utils import DIR_CONFIG


def criar_driver():

    config_file = DIR_CONFIG / "config.json"
    with open(config_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
        
        logging.info(f"=========================================================")
        logging.info(f"   Lendo arquivo de configuracao: {config_file}")
    
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") #inicializa o chrome maximizado
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    if settings["headless"]:
        chrome_options.add_argument("--headless=new") #executa sem interface gráfica
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={settings['chrome_window_size']}") #necessário para evitar elementos fora da tela
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    
    return driver

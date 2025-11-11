import time
import json
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from config.path_utils import DIR_CONFIG


def buscar_estabelecimentos(driver, tipo, cidade, quantidade):
    config_file = DIR_CONFIG / "config.json"
    with open(config_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
    
    logging.info(f"Buscando: {tipo} em {cidade} (quantidade: {quantidade})")

    driver.get(settings['link_google_maps'])
    time.sleep(3)

    campo_busca = driver.find_element(By.ID, "searchboxinput")
    campo_busca.send_keys(f"{tipo} em {cidade}")
    campo_busca.send_keys(Keys.ENTER)
    time.sleep(3)

    resultados = []
    lista = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK")
    scroll_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label*='Resultados']")

    while len(lista) < quantidade:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_div)
        time.sleep(1)
        lista = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK")
        try:
            driver.find_element(By.CSS_SELECTOR, ".HlvSq")
            break
        except NoSuchElementException:
            pass

    lista = lista[:quantidade]

    for item in lista:
        item.click()
        time.sleep(2)

        def safe(css, default="Não encontrado"):
            try:
                return driver.find_element(By.CSS_SELECTOR, css).text
            except:
                return default

        nome = safe("h1.DUwDvf")
        endereco = safe("button[data-item-id='address'] .Io6YTe")
        telefone = safe("button[data-item-id^='phone:'] .Io6YTe")

        try:
            bloco = driver.find_element(By.CSS_SELECTOR, ".F7nice")
            spans = bloco.find_elements(By.TAG_NAME, "span")

            try:
                nota = spans[0].find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
            except:
                nota = "Não informada"

            qtd_avaliacoes = "Não informada"
            for s in spans:
                txt = s.get_attribute("aria-label")
                if txt and "avalia" in txt.lower():
                    qtd_avaliacoes = txt.split()[0]
                    break
        except:
            nota = "Não informada"
            qtd_avaliacoes = "Não informada"

        try:
            link_pagina = driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']").get_attribute("href")
        except:
            link_pagina = "Não disponível"

        resultados.append({
            "Nome": nome,
            "Nota": nota,
            "Qtd. Avaliações": qtd_avaliacoes,
            "Endereço": endereco,
            "Telefone": telefone,
            "Link da Página": link_pagina
        })

    return resultados

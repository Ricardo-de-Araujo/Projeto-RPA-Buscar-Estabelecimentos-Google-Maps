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
    logging.info(f"=========================================================")
    logging.info(f"   Buscando: {tipo} em {cidade} (quantidade: {quantidade})")

    #Verifica se já está na página do Google Maps
    if (settings['link_google_maps']) not in driver.current_url:
        driver.get(settings['link_google_maps'])
        time.sleep(3)

    #Realiza a busca no Google Maps
    campo_buscar = driver.find_element(By.XPATH, settings['path_campo_buscar'])
    campo_buscar.clear()
    campo_buscar.send_keys(f"{tipo} em {cidade}")
    campo_buscar.send_keys(Keys.ENTER)
    time.sleep(3)

    resultados = []

    #lista_resultados = driver.find_elements(By.CSS_SELECTOR, settings['selector_lista_resultados'])
    lista_resultados = driver.find_elements(By.XPATH, settings['selector_lista_resultados'])


    while len(lista_resultados) < quantidade:
        #Rola a lista de resultados para carregar todos os estabelecimentos até a quantidade desejada
        #scroll_div = driver.find_element(By.CSS_SELECTOR, settings['selector_scroll_div'])
        scroll_div = driver.find_element(By.XPATH, settings['selector_scroll_div'])
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_div)

        time.sleep(1)

        #lista_resultados = driver.find_elements(By.CSS_SELECTOR, settings['selector_lista_resultados'])
        lista_resultados = driver.find_elements(By.XPATH, settings['selector_lista_resultados'])

        try:
            #busca elemento que indica o fim da lista
            #driver.find_element(By.CSS_SELECTOR, settings['selector_final_lista'])
            driver.find_element(By.XPATH, settings['selector_final_lista'])
            break
        except NoSuchElementException:
            pass

    lista_resultados = lista_resultados[:quantidade]

    for item in lista_resultados:
        item.click()
        time.sleep(2)

        def pegar_texto(path, default="Não encontrado"):
            try:
                return driver.find_element(By.XPATH, path).text.strip()
            except:
                return default

        def pegar_Atributo(path, attr, default="Não encontrado"):
            try:
                return driver.find_element(By.XPATH, path).get_attribute(attr)
            except:
                return default

        def pegar_nota_e_avaliacoes():
            try:
                #bloco = driver.find_element(By.CSS_SELECTOR, settings['selector_bloco'])
                bloco = driver.find_element(By.XPATH, settings['selector_bloco'])

                # Nota
                try:
                    nota = bloco.find_element(By.XPATH, settings['path_nota']).text.strip()
                    #nota = bloco.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text.strip()
                except:
                    nota = "Não informada"

                # Avaliações
                qtd_avaliacoes = "Não informada"
                qtd_avaliacoes = bloco.find_element(By.XPATH, settings['path_qtd_avaliacoes']).get_attribute("aria-label").split()[0]
                #qtd_avaliacoes = elem.get_attribute("aria-label").split()[0]


                return nota, qtd_avaliacoes

            except:
                return "Não informada", "Não informada"


        nome = pegar_texto(settings['path_nome'])
        endereco = pegar_texto(settings['path_endereco'])
        telefone = pegar_texto(settings['path_telefone'])

        nota, qtd_avaliacoes = pegar_nota_e_avaliacoes()

        link_pagina = pegar_Atributo(settings['path_link_pagina'], "href", "Não disponível")

        # logs
        logging.info("=========================================================")
        logging.info(f"Nome: {nome}")
        logging.info(f"Endereço: {endereco}")
        logging.info(f"Telefone: {telefone}")
        logging.info(f"Nota: {nota}")
        logging.info(f"Qtd. de Avaliações: {qtd_avaliacoes}")
        logging.info(f"Link da Página: {link_pagina}")


        resultados.append({
            "Nome": nome,
            "Nota": nota,
            "Qtd. Avaliações": qtd_avaliacoes,
            "Endereço": endereco,
            "Telefone": telefone,
            "Link da Página": link_pagina
        })

    return resultados

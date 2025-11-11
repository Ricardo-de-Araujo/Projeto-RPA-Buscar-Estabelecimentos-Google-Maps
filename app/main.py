import json
from tarefa.criar_log import log
from tarefa.criar_driver import criar_driver
from tarefa.salvar_excel import salvar_resultados_excel
from tarefa.criar_log import log
from config.path_utils import DIR_ENTRADA, DIR_SAIDA, DIR_CONFIG


def main():
    logging = log()
    logging.info("===== Execução iniciada =====")


    input_file = DIR_ENTRADA / "input.json"
    with open(input_file, "r", encoding="utf-8") as f:
        dados_entrada = json.load(f)

    logging.info(f"Arquivo de entrada carregado: {input_file.name}")


    driver = criar_driver()


    config_file = DIR_CONFIG / "config.json"
    with open(config_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
    output_file = DIR_SAIDA / (f"{settings['output_file_name']}")
    salvar_resultados_excel(driver, dados_entrada, output_file)


    driver.quit()

    logging.info(f"Arquivo gerado com sucesso: {output_file}")
    logging.info("===== Execução finalizada =====")


if __name__ == "__main__":
    main()

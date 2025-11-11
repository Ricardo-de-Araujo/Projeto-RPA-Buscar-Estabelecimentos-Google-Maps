import pandas as pd
import logging
from .buscar_maps import buscar_estabelecimentos


def ajustar_largura_colunas(writer, sheet_name, df):
    worksheet = writer.sheets[sheet_name]
    for i, col in enumerate(df.columns):
        max_len = max(df[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.column_dimensions[chr(65 + i)].width = max_len


def salvar_resultados_excel(driver, dados_entrada, output_file):
    logging.info(f"Iniciando geração do Excel: {output_file}")

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for item in dados_entrada:
            tipo = item["tipo_estabelecimento"]
            cidade = item["cidade"]
            quantidade = item["quantidade"]


            resultados = buscar_estabelecimentos(driver, tipo, cidade, quantidade)
            df = pd.DataFrame(resultados)

            nome_aba = f"{tipo} - {cidade}".replace("/", "_")[:31]

            df.to_excel(writer, sheet_name=nome_aba, index=False)
            ajustar_largura_colunas(writer, nome_aba, df)

            logging.info(f"Aba adicionada ao Excel: {nome_aba}")

    logging.info("Excel gerado com sucesso")

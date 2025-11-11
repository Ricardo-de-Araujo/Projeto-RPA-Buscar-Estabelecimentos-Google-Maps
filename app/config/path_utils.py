from pathlib import Path

#Define a pasta raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent  # projeto_rpa_maps/

DIR_CONFIG = BASE_DIR / "config"
DIR_ENTRADA = BASE_DIR / "entrada"
DIR_SAIDA = BASE_DIR / "saida"
DIR_LOG = BASE_DIR / "logs"
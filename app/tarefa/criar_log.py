import logging
from datetime import datetime
from config.path_utils import DIR_LOG
from zoneinfo import ZoneInfo


def log():
    DIR_LOG.mkdir(exist_ok=True)
    
    #Cria arquivo de log com timestamp
    time = datetime.now(ZoneInfo("America/Sao_Paulo"))
    timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
    log_path = DIR_LOG / f"log_{timestamp}.txt"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(filename)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("rpa_maps_logger")
# módulos nativos
import argparse
import logging
import os
from datetime import date

# módulos baixados
import pandas as pd


# variáveis globais
PASTA = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(PASTA, "01.raw")
PROCESSED = os.path.join(PASTA, "02.processed")
LOGS = os.path.join(PASTA, "logs")

# garantia de existência dos diretórios
os.makedirs(RAW, exist_ok=True)
os.makedirs(PROCESSED, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)

# configurando logger
def get_logger():
    logger = logging.getLogger(__name__) # cria um objeto de log para rastrear o arquivo que gerou os registros

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO) # estabelece o nível mínimo para levantar os registros

    # configura a formatação dos registros de log
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # configura os registros de logs no terminal
    console_handler = logging.StreamHandler() # inicializa o handler
    console_handler.setFormatter(formatter) # estabelece a formatação do handler
    logger.addHandler(console_handler) # conecta o handler ao logger

    # configura os registros de logs da pasta logs
    log_path = os.path.join(LOGS, f"{date.today():%Y-%m-%d}.log")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def extract(pasta_entrada):
    """
    Lê todos os CSVs da pasta de entrada e devolve um único DataFrame
    com todos os dados empilhados, adicionando uma coluna
    `arquivo_origem` com o nome do arquivo de onde cada linha veio. 
    """
    logger = get_logger()

    arquivos = os.listdir(pasta_entrada)
    lista_dataframes = []

    logger.info(f"Iniciando extração da pasta {os.path.basename(pasta_entrada)}")
    for f in arquivos:
        if f.endswith(".csv"):
            df = pd.read_csv(os.path.join(pasta_entrada, f))
            logger.info(f"Lendo arquivo: {f}")
            df["arquivo_origem"] = f # preenche a coluna com o nome do arquivo
            lista_dataframes.append(df)

    if not lista_dataframes:
        logger.warning(f"Nenhum arquivo .csv encontrado na pasta {os.path.basename(pasta_entrada)}.")

    df_unificado = pd.concat(lista_dataframes)
    logger.info(f"Extração concluída: {len(lista_dataframes)} arquivos lidos, {len(df_unificado)} linhas no total.")

    return df_unificado
# módulos nativos
import argparse
import logging
import os
from unicodedata import combining, normalize
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


def remover_acentos(texto):
    nfd = normalize("NFD", texto) # separa os acentos das letras
    return "".join(c for c in nfd if not combining(c))


def transform(df: pd.DataFrame):
    """
    Recebe o DataFrame bruto e aplica os seguintes tratamentos:
    - Remove linhas duplicadas
    - Padroniza strings
    - Padroniza formatos de data
    - Converte valores em float
    - Converte quantidades em int
    - Remove linhas com valores nulos
    """
    logger = get_logger()

    linhas_antes = len(df)
    df_limpo = df.drop_duplicates()
    linhas_depois = len(df_limpo)
    logger.info(f"Removendo linhas duplicadas: {linhas_antes - linhas_depois} linhas removidas")

    df_limpo["categoria"] = df_limpo["categoria"].str.strip().str.title()
    df_limpo["cat_normalizada"] = df_limpo["categoria"].map(remover_acentos) # coluna de categorias sem acento

    # solução inteligente: ao invés de dicionário fixo com versão normalizada (sem acento) e versão correta,
    # agrupa por categoria normalizada e devolve a versão de categoria mais frequente em cada normalização,
    # a qual geralmente é a categoria correta. Reaplicável caso as categorias mudem.
    correcoes = (
        df_limpo.groupby("cat_normalizada")["categoria"]
        .agg(lambda s: s.value_counts().idxmax())
        .to_dict()
    )

    categoria_antes = df_limpo["categoria"].copy()
    df_limpo["categoria"] = df_limpo["cat_normalizada"].map(correcoes)
    df_limpo = df_limpo.drop(columns=["cat_normalizada"])
    linhas_alteradas = (categoria_antes != df_limpo["categoria"]).sum()
    logger.info(f"Categorias corrigidas: {linhas_alteradas} linhas")

    df_limpo["data_venda"] = pd.to_datetime(df_limpo["data_venda"], errors="coerce", dayfirst=True, format="mixed")
    logger.info(f"Datas inválidas/vazias: {df_limpo["data_venda"].isna().sum()}")

    df_limpo["valor"] = pd.to_numeric(df_limpo["valor"], errors="coerce")
    val_nulos =  df_limpo["valor"].isna().sum()
    logger.info(f"Valores inválidos encontrados: {val_nulos}")

    zeros_antes_qtd = (df_limpo["quantidade"] == 0).sum()
    df_limpo["quantidade"] = pd.to_numeric(df_limpo["quantidade"], errors="coerce").fillna(0).astype(int)
    zeros_depois_qtd = (df_limpo["quantidade"] == 0).sum()
    logger.info(f"Quantidades inválidas preenchidas com zero: {zeros_depois_qtd - zeros_antes_qtd}")

    df_limpo = df_limpo.dropna(subset=["valor"])
    logger.info(f"Linhas removidas por valor nulo: {val_nulos} linhas.")

    return df_limpo


def load(df_limpo: pd.DataFrame, pasta_saida):
    logger = get_logger()
    df_limpo.to_csv(os.path.join(pasta_saida, f"{date.today()}_vendas_filiais.csv"), index=False)
    logger.info(f"Arquivo de vendas processado e gravado em {os.path.basename(pasta_saida)}")

    with open(os.path.join(pasta_saida, f"{date.today()}_resumo.txt"), "w", encoding="utf-8") as r:
        r.write(f"Total de linhas: {len(df_limpo)}\n")
        r.write(f"Data da execução: {date.today()}")
    logger.info(f"Resumo gravado em {os.path.basename(pasta_saida)}")


def main():
    parser = argparse.ArgumentParser(description="Pipeline ETL: lê CSVs de vendas brutos, limpa e padroniza os dados e grava o resultado.")
    parser.add_argument("--entrada", default=RAW, help="Pasta com os CSVs brutos (padrão: 01.raw)")
    parser.add_argument("--saida", default=PROCESSED, help="Pasta onde os arquivos processados serão gravados CSVs (padrão: 02.processed)")
    args = parser.parse_args()

    pasta_entrada = os.path.abspath(args.entrada)
    pasta_saida = os.path.abspath(args.saida)
    os.makedirs(pasta_saida, exist_ok=True)

    df_bruto = extract(pasta_entrada)
    df_limpo = transform(df_bruto)
    load(df_limpo, pasta_saida)


if __name__ == "__main__":
    main()
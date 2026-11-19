# Pipeline CSV de Vendas

## Descrição
Simular uma mini pipeline ETL (Extract → Transform → Load) que recebe CSVs "sujos" de vendas de várias filiais, limpa, padroniza os dados e gera:
- um CSV limpo e unificado, pronto para análise
- um resumo simples com data da execução e total de linhas final
- um log de execução estruturado com timestamps (substituindo `print()`)

## Funcionalidades
- Lê todos os arquivos CSV da pasta `01.raw`
- Remove linhas duplicadas
- Trata valores nulos
- Padroniza formato de datas
- Corrige categorias inconsistentes (ex: eletronico -> Eletrônico)
- Padroniza os dados
- Gera um relatório unificado das vendas em `02.processed`
- Gera um relatório de qualidade com estatísticas do que foi tirado

## Como Usar
1. Clone o repositório e entre na pasta  
    ```bash
    git clone https://github.com/AntonioAugustoF/csv-pipeline.git
    cd csv-pipeline
    ```

2. Crie e ative o ambiente virtual  
    ```bash
    python -m venv .venv # cria pasta .venv

    # ativa venv
    .venv\Scripts\activate # Windows  
    source .venv/bin/activate # Linux/Mac
    ``` 
3. Instale as dependências
    ```bash
    pip install -r requirements.txt
    ```

4. Gere os dados de exemplo
    ```bash
    python gerar_dados.py
    ```

5. Rode o pipeline
    ```bash
    python pipeline.py # execução normal
    python pipeline.py --help # dúvidas sobre argumentos da execução
    python pipeline.py --entrada 01.raw --saida resultados # execução especificando os argumentos
    ```

## Pré-requisitos
- Python 3.10+
- pandas 

## Estrutura de pastas
```
csv_pipeline/
├─── 01.raw/
├─── 02.processed/
├─── logs/
├─── .gitignore
├─── gerar_dados.py
├─── pipeline.py
├─── README.md
└─── requirements.txt
```

## Exemplos de Uso

```text
2026-11-19 18:52:25 | INFO | __main__ | Iniciando extração da pasta 01.raw
2026-11-19 18:52:25 | INFO | __main__ | Lendo arquivo: vendas_filial_mg.csv
2026-11-19 18:52:25 | INFO | __main__ | Lendo arquivo: vendas_filial_pr.csv
2026-11-19 18:52:25 | INFO | __main__ | Lendo arquivo: vendas_filial_rj.csv
2026-11-19 18:52:25 | INFO | __main__ | Lendo arquivo: vendas_filial_sp.csv
2026-11-19 18:52:25 | INFO | __main__ | Extração concluída: 4 arquivos lidos, 1438 linhas no total.
2026-11-19 18:52:25 | INFO | __main__ | Removendo linhas duplicadas: 68 linhas removidas
2026-11-19 18:52:25 | INFO | __main__ | Categorias corrigidas: 209 linhas
2026-11-19 18:52:25 | INFO | __main__ | Datas inválidas/vazias: 25
2026-11-19 18:52:25 | INFO | __main__ | Valores inválidos encontrados: 24
2026-11-19 18:52:25 | INFO | __main__ | Quantidades inválidas preenchidas com zero: 42
2026-11-19 18:52:25 | INFO | __main__ | Linhas removidas por valor nulo: 24 linhas.
2026-11-19 18:52:25 | INFO | __main__ | Arquivo de vendas processado e gravado em 02.processed
2026-11-19 18:52:25 | INFO | __main__ | Resumo gravado em 02.processed
```

## Autor

**Antonio Augusto Fernandes**  
Analista de Dados em transição para Engenharia de Dados / Analytics Engineering

- Github: [AntonioAugustoF](https://github.com/AntonioAugustoF)
- LinkedIn: [antonioafernandes](https://www.linkedin.com/in/antonioafernandes)

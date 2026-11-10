# Pipeline CSV de Vendas

## Descrição
Simular uma mini pipeline ETL (Extract → Transform → Load) que recebe CSV's "sujos" de vendas de várias filiais, limpa, padroniza os dados e gera:
- um CSV limpo e unificado, pronto para análise
- um relatório de qualidade com estatísticas do que foi tirado
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

## Pré-requisitos
- Python 3.10+
- pandas 

## Passos

## Estrutura de pastas
```
csv_pipeline/
├─── 01.raw/
├─── 02.processed/
├─── .gitignore
├─── README.md
└─── requirements.txt
```

## Exemplos de Uso

## Autor

**Antonio Augusto Fernandes**  
Analista de Dados em transsição para Engenharia de Dados / Analytics Engineering

- Github: [AntonioAugustoF](https://github.com/AntonioAugustoF)
- LinkedIn: [antonioafernandes](https://www.linkedin.com/in/antonioafernandes)
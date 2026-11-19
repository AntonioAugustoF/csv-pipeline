"""
Script auxiliar para gerar os CSVs fictícios "sujos" do Projeto 3.
Rode uma vez: python -I gerar_dados.py
Depois pode apagar ou ignorar — os CSVs ficam em dados_brutos/
"""

import os
import csv
import random

PASTA = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(PASTA, "dados_brutos")
os.makedirs(SAIDA, exist_ok=True)

# ── Dados base ──────────────────────────────────────────────

produtos = [
    ("Mouse Gamer", "Periférico", 89.90),
    ("Teclado Mecânico", "Periférico", 249.90),
    ("Monitor 24pol", "Eletrônico", 899.00),
    ("Notebook i5", "Eletrônico", 3299.00),
    ("Cabo HDMI 2m", "Acessório", 29.90),
    ("Mousepad XL", "Acessório", 45.00),
    ("Webcam HD", "Periférico", 189.90),
    ("Headset Bluetooth", "Eletrônico", 199.90),
    ("Hub USB-C", "Acessório", 79.90),
    ("SSD 480GB", "Eletrônico", 219.00),
    ("Caixa de Som", "Eletrônico", 149.90),
    ("Suporte Notebook", "Acessório", 69.90),
    ("Pen Drive 64GB", "Acessório", 39.90),
    ("Carregador USB", "Acessório", 49.90),
    ("Roteador Wi-Fi", "Eletrônico", 179.90),
    ("Cadeira Gamer", "Mobiliário", 899.00),
    ("Mesa Gamer", "Mobiliário", 649.00),
    ("Apoio de Pé", "Mobiliário", 89.90),
    ("Luminária LED", "Acessório", 59.90),
    ("Filtro de Linha", "Acessório", 34.90),
]

filiais = ["filial_sp", "filial_rj", "filial_mg", "filial_pr"]

# Variações sujas de categorias (erros de digitação, capitalização)
# Pesos: a forma correta (com acento) deve dominar amplamente — erro de
# digitação é minoria nos dados reais, não metade dos registros.
categorias_sujas = {
    "Periférico": ["Periférico", "periferico", "PERIFERICO", "Periferico", " periférico ", "Periférico"],
    "Eletrônico": ["Eletrônico", "eletronico", "ELETRONICO", "Eletronico", "eletrônico", " Eletrônico"],
    "Acessório":  ["Acessório", "acessorio", "ACESSORIO", "Acessorio", " acessório ", "Acessório"],
    "Mobiliário":  ["Mobiliário", "mobiliario", "MOBILIARIO", "Mobiliario", " mobiliário ", "Mobiliário"],
}
# pesos correspondentes, na mesma ordem das 6 variações de cada lista acima:
# [correta, minúscula sem acento, maiúscula sem acento, título sem acento, com espaço, correta de novo]
PESOS_CATEGORIA = [30, 5, 5, 5, 15, 30]

# Formatos de data misturados
meses = list(range(1, 13))
meses_abrev = {
    1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun",
    7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez",
}

def data_aleatoria():
    """Gera uma data de 2024 em um de 3 formatos aleatórios."""
    dia = random.randint(1, 28)
    mes = random.choice(meses)
    ano = 2024
    formato = random.choice(["dmy_slash", "iso", "dmy_abrev"])
    if formato == "dmy_slash":
        return f"{dia:02d}/{mes:02d}/{ano}"
    elif formato == "iso":
        return f"{ano}-{mes:02d}-{dia:02d}"
    else:
        return f"{dia:02d}-{meses_abrev[mes]}-{ano}"

def gerar_csv_filial(nome_filial, num_linhas):
    """Gera um CSV com dados sujos para uma filial."""
    caminho = os.path.join(SAIDA, f"vendas_{nome_filial}.csv")
    linhas = []

    for _ in range(num_linhas):
        produto, cat_limpa, preco_base = random.choice(produtos)
        categoria = random.choices(categorias_sujas[cat_limpa], weights=PESOS_CATEGORIA, k=1)[0]
        data = data_aleatoria()
        valor = round(preco_base * random.uniform(0.8, 1.2), 2)
        quantidade = random.randint(1, 15)

        linha = {
            "produto": produto,
            "categoria": categoria,
            "data_venda": data,
            "valor": str(valor),
            "quantidade": str(quantidade),
            "filial": nome_filial,
        }

        # ── Injetar sujeira ──

        # ~3% das linhas: valor não numérico
        if random.random() < 0.03:
            linha["valor"] = random.choice(["abc", "N/A", "--", "erro", ""])

        # ~4% das linhas: quantidade vazia ou inválida
        if random.random() < 0.04:
            linha["quantidade"] = random.choice(["", "null", "?"])

        # ~2% das linhas: data vazia
        if random.random() < 0.02:
            linha["data_venda"] = ""

        linhas.append(linha)

    # Injetar ~5% de duplicatas (copiar linhas existentes)
    num_duplicatas = int(num_linhas * 0.05)
    for _ in range(num_duplicatas):
        linhas.append(random.choice(linhas[:num_linhas]).copy())

    # Embaralhar
    random.shuffle(linhas)

    # Gravar
    campos = ["produto", "categoria", "data_venda", "valor", "quantidade", "filial"]
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow(linha)

    print(f"  ✔ {caminho} — {len(linhas)} linhas")
    return len(linhas)

# ── Gerar ──────────────────────────────────────────────────

random.seed(42)

print("Gerando CSVs fictícios...\n")
total = 0
total += gerar_csv_filial("filial_sp", 400)
total += gerar_csv_filial("filial_rj", 350)
total += gerar_csv_filial("filial_mg", 300)
total += gerar_csv_filial("filial_pr", 320)

print(f"\nTotal: {total} linhas (incluindo duplicatas)")
print(f"Pasta: {SAIDA}")
print("\nProblemas injetados:")
print("  • ~3% com valor inválido (abc, N/A, --, erro, vazio)")
print("  • ~4% com quantidade inválida (vazio, null, ?)")
print("  • ~2% com data vazia")
print("  • ~5% de linhas duplicadas por arquivo")
print("  • Categorias com capitalização/acentuação inconsistente (4 categorias)")
print("  • Datas em 3 formatos misturados (DD/MM/YYYY, YYYY-MM-DD, DD-mmm-YYYY)")
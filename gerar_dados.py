"""Gera uma base de vendas fictícia e realista (vendas.csv) para o dashboard."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

produtos = {
    "Eletrônicos": [("Smartphone", 1899.0), ("Notebook", 3999.0), ("Fone Bluetooth", 249.0), ("Smartwatch", 899.0)],
    "Informática": [("Mouse Gamer", 159.0), ("Teclado Mecânico", 349.0), ("Monitor 24\"", 999.0), ("SSD 1TB", 429.0)],
    "Casa": [("Air Fryer", 459.0), ("Cafeteira", 289.0), ("Aspirador Robô", 1299.0), ("Liquidificador", 199.0)],
    "Moda": [("Tênis Esportivo", 399.0), ("Jaqueta", 259.0), ("Mochila", 179.0), ("Relógio", 329.0)],
    "Esporte": [("Bicicleta", 1599.0), ("Halteres 10kg", 189.0), ("Esteira", 2799.0), ("Tapete Yoga", 99.0)],
}
regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
peso_regioes = [0.42, 0.18, 0.20, 0.12, 0.08]
canais = ["Site", "App", "Loja Física"]

datas = pd.date_range("2024-01-01", "2025-12-31", freq="D")
linhas, pedido = [], 10000
for d in datas:
    # sazonalidade: pico em novembro (Black Friday) e dezembro (Natal) + crescimento anual
    base = 4 + (1.5 if d.year == 2025 else 0)
    if d.month == 11: base *= 2.2
    elif d.month == 12: base *= 1.8
    elif d.month in (5, 6): base *= 1.2
    for _ in range(rng.poisson(base)):
        pedido += 1
        cat = rng.choice(list(produtos))
        prod, preco = produtos[cat][rng.integers(len(produtos[cat]))]
        qtd = int(rng.integers(1, 4))
        desconto = rng.choice([0, 0.05, 0.10, 0.15], p=[0.6, 0.2, 0.15, 0.05])
        preco_final = round(preco * (1 - desconto), 2)
        linhas.append({
            "data": d.date(), "pedido_id": pedido, "categoria": cat, "produto": prod,
            "regiao": rng.choice(regioes, p=peso_regioes), "canal": rng.choice(canais, p=[0.45, 0.35, 0.20]),
            "quantidade": qtd, "preco_unitario": preco_final, "receita": round(preco_final * qtd, 2),
        })

df = pd.DataFrame(linhas)
df.to_csv("vendas.csv", index=False)
print(df.shape); print(df.head())

# 📊 Dashboard de Vendas — Streamlit

Painel de Business Intelligence interativo desenvolvido com **Streamlit** e **Pandas**.

## Funcionalidades
- Carga de dados otimizada com `@st.cache_data`
- Filtros laterais por categoria, região e período
- Métricas de receita, pedidos, ticket médio e itens vendidos, com variação vs. período anterior
- Gráfico de área com a evolução mensal da receita por categoria e gráfico de barras por região
- Tabela interativa com ordenação e exportação do recorte filtrado em CSV

## Como executar localmente
```bash
pip install -r requirements.txt
streamlit run meu_dashboard.py
```

## Estrutura
| Arquivo | Descrição |
|---|---|
| `meu_dashboard.py` | Aplicação principal |
| `vendas.csv` | Base de vendas (fictícia, 2024–2025) |
| `gerar_dados.py` | Script que gera a base fictícia |
| `requirements.txt` | Dependências para o deploy |
| `.streamlit/config.toml` | Tema visual do painel |

## Deploy
Publicado no Streamlit Community Cloud: **[cole aqui o link do seu app]**

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import load_datas, api_ipca, integrate_transactions_ipca

def analyze_and_plot():
    datasets = load_datas()
    df_transacoes = datasets["TRANSACOES"]

    # Carregar IPCA
    df_ipca = api_ipca()

    # Integrar os dados de transações com IPCA
    df = integrate_transactions_ipca(df_transacoes, df_ipca)

    # Converter a coluna de data para datetime
    df["data_transacao"] = pd.to_datetime(df["data_transacao"], errors="coerce").dt.tz_localize(None)

    df["trimestre"] = df["data_transacao"].dt.to_period("Q").astype(str)

    # Agrupar por trimestre e calcular a média de transações e volume movimentado
    df_resultado = df.groupby("trimestre").agg(
        media_transacoes=("cod_transacao", "count"),
        media_valor_movimentado=("valor_transacao", "mean")
    ).reset_index()

    # Criar gráfico de barras
    fig, ax1 = plt.subplots(figsize=(15, 6))

    ax1.bar(df_resultado["trimestre"], df_resultado["media_transacoes"],
            color="blue", alpha=0.5, label="Média de Transações")

    ax1.set_xlabel("Trimestre")
    ax1.set_ylabel("Média de Transações", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.set_xticklabels(df_resultado["trimestre"], rotation=45, ha="right")  # Rotação para legibilidade

    # Criar um segundo eixo para volume movimentado
    ax2 = ax1.twinx()
    ax2.plot(df_resultado["trimestre"], df_resultado["media_valor_movimentado"],
             marker="o", color="red", linestyle="-", linewidth=2, label="Média do Valor Movimentado")

    ax2.set_ylabel("Média do Valor Movimentado", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # Adicionar grade para melhorar a leitura
    ax1.grid(True, linestyle="--", alpha=0.6)

    plt.title("Média de Transações e Valor Movimentado por Trimestre")
    fig.tight_layout()
    plt.show()

def plot_ipca_transacoes():
    """
        Função para carregar os dados, integrar as transações com o IPCA e gerar gráficos.
        """
    # Carregar os dados das planilhas CSV
    planilhas = load_datas()

    # Verificar se a planilha de transações está disponível
    if "TRANSACOES" not in planilhas:
        raise ValueError("Erro: A planilha de transações não foi encontrada!")

    df_transacoes = planilhas["TRANSACOES"]

    # Carregar os dados do IPCA
    df_ipca = api_ipca()

    # Integrar os dados das transações com o IPCA
    df_final = integrate_transactions_ipca(df_transacoes, df_ipca)

    # Verificar as colunas disponíveis no DataFrame integrado
    print("Colunas disponíveis no DataFrame integrado:", df_final.columns)

    # Garantir que a coluna 'data_transacao' está presente e converter para datetime
    if "data_transacao" in df_final.columns:
        df_final["data_transacao"] = pd.to_datetime(df_final["data_transacao"], errors="coerce")
    else:
        raise KeyError("Erro: A coluna 'data_transacao' não foi encontrada no DataFrame integrado!")

    # Garantir que a coluna 'Valor do Índice' existe e converter para numérico
    if "Valor do Índice" in df_final.columns:
        df_final["Valor do Índice"] = pd.to_numeric(df_final["Valor do Índice"], errors="coerce")
    else:
        raise KeyError("Erro: A coluna 'Valor do Índice' não foi encontrada no DataFrame integrado!")

    # Garantir que a coluna 'valor_transacao' existe e converter para numérico
    if "valor_transacao" in df_final.columns:
        df_final["valor_transacao"] = pd.to_numeric(df_final["valor_transacao"], errors="coerce")
    else:
        raise KeyError("Erro: A coluna 'valor_transacao' não foi encontrada no DataFrame integrado!")

    # Criar gráfico de dispersão entre IPCA e valor das transações
    plt.figure(figsize=(10, 6))
    plt.scatter(df_final["Valor do Índice"], df_final["valor_transacao"], alpha=0.5, c="blue", label="Transações")
    plt.xlabel("Índice IPCA")
    plt.ylabel("Valor das Transações")
    plt.title("Relação entre IPCA e Valor das Transações")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    analyze_and_plot()
    plot_ipca_transacoes()

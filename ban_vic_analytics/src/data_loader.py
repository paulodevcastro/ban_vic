import pandas as pd
import requests
from src.config import share_datas

def load_datas():
    files = share_datas()

    if not files:
        print("Nenhum arquivo encontrado")
        return

    for name, path, in files.items():
        try:
            df = pd.read_csv(path)
            print(f"PLANILHA: {name}")
            print(df.head(20))
            print("-" * 100)

            null_counts = df.isnull().sum()
            null_columns = null_counts[null_counts > 0]

            if not null_columns.empty:
                print("Valores nulos encontrados nas colunas:")
                print(null_columns)
            else:
                print("Nenhum valor nulo encontrado.")

            print("=" * 50)

        except FileNotFoundError:
            print(f"Arquivo não encontrado: {path}")
        except pd.errors.EmptyDataError:
            print(f"Arquivo vazio: {path}")
        except Exception as e:
            print(f"Erro ao carregar {name}", e)


def api_ipca():
    url = "https://apisidra.ibge.gov.br/values/t/1419/n1/all/v/all/p/all/c315/7169,7170,7445,7486,7558,7625,7660,7712,7766,7786/d/v63%202,v66%204,v69%202,v2265%202?formato=json"
    response = requests.get(url)

    if response.status_code == 200:
        dados_ipca = response.json()

        # Remoçao do cabeçalho
        dados_ipca = dados_ipca[1:]
        df_ipca = pd.DataFrame(dados_ipca)

        # Renomeando colunas para facilitar a leitura
        df_ipca = df_ipca.rename(columns={
            "NC": "Niv. Terri. (Cod)",
            "NN": "Niv. Terri.",
            "MC": "Uni. Med (Cod)",
            "MN": "Unid. Medida",
            "V": "Valor do Índice",
            "D1C": "Brasil (Cod)",
            "D1N": "Brasil",
            "D2C": "Cod Variável",
            "D2N": "Nome Variável",
            "D3C": "Mês (Cod)",
            "D3N": "Nome Mês",
            "D4C": "Cod. Agrupamento",
            "D4N": "Agrupamento"
        })

        # Configurações para exibir todas as colunas e linhas
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", 100)
        pd.set_option("display.expand_frame_repr", False)

        # Verificar se a coluna "Valor do Índice" existe antes de converter
        if "Valor do Índice" in df_ipca.columns:
            print("Valores antes da conversão:", df_ipca["Valor do Índice"].head(10))
            df_ipca["Valor do Índice"] = pd.to_numeric(df_ipca["Valor do Índice"], errors="coerce")
            print("Valores depois da conversão:", df_ipca["Valor do Índice"].head(10))
        else:
            print("Erro: A coluna 'Valor do Índice' não foi encontrada!")

        # print(df_ipca.info())
        print(df_ipca.head(10))

        return df_ipca

    else:
        print(f"Erro ao acessar a API: {response.status_code}")
        return None

def integrate_transactions_ipca(df_transacoes, df_ipca):
    df_transacoes["mes_ano"] = df_transacoes["data_transacao"].dt.strftime("%Y-%m")
    # Extrai ano-mês
    df_ipca["mes_ano"] = df_ipca["Mes"].str.extract(r'(\d{4}-\d{2})')

    # Fazendo a junção (merge) dos dois DataFrames
    df_final = df_transacoes.merge(df_ipca, on="mes_ano", how="left")

    print(df_final.head(10))  # Exibir algumas linhas para conferir
    return df_final

if __name__ == "__main__":
    api_ipca()
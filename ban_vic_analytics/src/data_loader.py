import pandas as pd
import requests
import os
from src.config import share_datas

def load_datas():
    files = share_datas()

    if not files:
        print("Nenhum arquivo encontrado.")
        return {}

    # DataFrames carregados
    dataframes = {}

    for name, path in files.items():
        try:
            df = pd.read_csv(path)

            # Substituir valores NaN por "Sem dado"
            df = df.fillna("Sem dado")

            print(f"\n🔹 PLANILHA: {name}\n")
            print(df.head(10))
            print("-" * 100)

            null_counts = df.isnull().sum()
            null_columns = null_counts[null_counts > 0]

            if not null_columns.empty:
                print("Valores nulos encontrados nas colunas:")
                print(null_columns)
            else:
                print("Nenhum valor nulo encontrado.")

            print("=" * 50)

            # Armazenar DataFrame no dicionário
            dataframes[name] = df

        except FileNotFoundError:
            print(f"Arquivo não encontrado: {path}")
        except pd.errors.EmptyDataError:
            print(f"Arquivo vazio: {path}")
        except Exception as e:
            print(f"Erro ao carregar {name}: {e}")

    return dataframes

def api_ipca():
    url = "https://apisidra.ibge.gov.br/values/t/1419/n1/all/v/all/p/all/c315/7169,7170,7445,7486,7558,7625,7660,7712,7766,7786/d/v63%202,v66%204,v69%202,v2265%202?formato=json"
    response = requests.get(url)

    if response.status_code == 200:
        dados_ipca = response.json()

        # Remoção do cabeçalho
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

        # Configuração de exibição
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", 100)
        pd.set_option("display.expand_frame_repr", False)

        # Verificar se a coluna "Valor do Índice" existe antes de converter
        if "Valor do Índice" in df_ipca.columns:
            df_ipca["Valor do Índice"] = pd.to_numeric(df_ipca["Valor do Índice"], errors="coerce")
        else:
            print("Erro: A coluna 'Valor do Índice' não foi encontrada!")

        # Ajustar o formato do "Nome Mês" para "YYYY-MM"
        meses = {
            "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
            "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
            "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
        }

        # Extrair o mês e ano corretamente
        df_ipca[["Nome Mês", "Ano"]] = df_ipca["Nome Mês"].str.extract(r"(\w+) (\d{4})")
        df_ipca["mes_ano"] = df_ipca.apply(lambda x: f"{x['Ano']}-{meses.get(x['Nome Mês'].lower(), '00')}", axis=1)

        # Substituir NaN por "Sem dado"
        df_ipca = df_ipca.fillna("Sem dado")

        print("\nDados do IPCA carregados com sucesso!")
        print(df_ipca[["Nome Mês", "Ano", "mes_ano"]].head())

        return df_ipca

    else:
        print(f"Erro ao acessar a API: {response.status_code}")
        return None


def integrate_transactions_ipca(df_transacoes, df_ipca):
    # Garantindo que a coluna de data seja do tipo datetime
    df_transacoes["data_transacao"] = pd.to_datetime(df_transacoes["data_transacao"], errors="coerce")

    # Criando a coluna mes_ano no formato "YYYY-MM"
    df_transacoes["mes_ano"] = df_transacoes["data_transacao"].dt.strftime("%Y-%m")

    # Merge dos dados das transações com o IPCA
    df_final = df_transacoes.merge(df_ipca, on="mes_ano", how="left")

    # Substituir NaN por "Sem dado"
    df_final = df_final.fillna("Sem dado")

    print("\nIntegração realizada com sucesso!")
    print(df_final.head(10))  # Exibe algumas linhas para conferência

    return df_final


if __name__ == "__main__":
    print("\nCarregando planilhas CSV")
    planilhas = load_datas()  # Carregar todas as planilhas

    # Carregar dados do IPCA
    df_ipca = api_ipca()

    if df_ipca is not None and "TRANSACOES" in planilhas:
        df_transacoes = planilhas["TRANSACOES"]

        print("\nDados das transações carregados com sucesso!")

        # Integrar com IPCA
        df_final = integrate_transactions_ipca(df_transacoes, df_ipca)

        base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do script
        output_path = os.path.join(os.path.dirname(base_dir), "dados_integrados.csv")

        # Se o arquivo já existir, removê-lo antes de criar um novo
        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"Arquivo anterior removido: {output_path}")

        # Salvar o novo arquivo CSV
        df_final.to_csv(output_path, index=False)

        print(f"\nDados integrados salvos em: {output_path}")
    else:
        print("Erro: Não foi possível carregar os dados necessários para a integração!")
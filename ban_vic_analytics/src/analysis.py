import pandas as pd
import requests
import os
from data_loader import load_datas  # Supondo que esta função esteja no seu módulo


def api_ipca():
    url = "https://apisidra.ibge.gov.br/values/t/1419/n1/all/v/all/p/all/c315/7169,7170,7445,7486,7558,7625,7660,7712,7766,7786/d/v63%202,v66%204,v69%202,v2265%202?formato=json"
    response = requests.get(url)

    if response.status_code == 200:
        dados_ipca = response.json()[1:]  # Remove cabeçalho
        df_ipca = pd.DataFrame(dados_ipca)

        # Renomeação de colunas
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

        # Conversão da coluna "Valor do Índice" para numérico
        df_ipca["Valor do Índice"] = pd.to_numeric(df_ipca["Valor do Índice"], errors="coerce")

        # Ajustar o formato "Nome Mês" para "YYYY-MM"
        meses = {
            "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
            "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
            "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
        }

        df_ipca[["Nome Mês", "Ano"]] = df_ipca["Nome Mês"].str.extract(r"(\w+) (\d{4})")
        df_ipca["mes_ano"] = df_ipca.apply(lambda x: f"{x['Ano']}-{meses.get(x['Nome Mês'].lower(), '00')}", axis=1)
        df_ipca = df_ipca.fillna("Sem dado")

        print("\nDados do IPCA carregados com sucesso!")
        return df_ipca

    print(f"Erro ao acessar a API: {response.status_code}")
    return None


def get_documents_folder():
    """ Retorna o caminho correto da pasta 'Documentos' no sistema operacional """
    if os.name == "nt":  # Windows
        return os.path.join(os.environ["USERPROFILE"], "Documents")
    else:  # Linux/Mac
        return os.path.expanduser("~/Documents")


def integrate_transactions_ipca(df_transacoes, df_ipca):
    df_transacoes["data_transacao"] = pd.to_datetime(df_transacoes["data_transacao"], errors="coerce")
    df_transacoes["mes_ano"] = df_transacoes["data_transacao"].dt.strftime("%Y-%m")

    df_final = df_transacoes.merge(df_ipca, on="mes_ano", how="left").fillna("Sem dado")
    print("\nIntegração realizada com sucesso!")

    # Definir o caminho na pasta Documentos
    output_path = os.path.join(get_documents_folder(), "dados_integrados.csv")

    # Remover arquivo antigo se existir
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"Arquivo anterior removido: {output_path}")

    # Salvar novo CSV na pasta Documentos
    df_final.to_csv(output_path, index=False)
    print(f"\nDados integrados salvos em: {output_path}")
    return df_final


if __name__ == "__main__":
    print("\nCarregando planilhas CSV")
    planilhas = load_datas()  # Carregar todas as planilhas

    df_ipca = api_ipca()  # Carregar dados do IPCA

    if df_ipca is not None and "TRANSACOES" in planilhas:
        df_transacoes = planilhas["TRANSACOES"]

        print("\nDados das transações carregados com sucesso!")

        # Integrar com IPCA e salvar na pasta Documentos
        integrate_transactions_ipca(df_transacoes, df_ipca)

    else:
        print("Erro: Não foi possível carregar os dados necessários para a integração!")

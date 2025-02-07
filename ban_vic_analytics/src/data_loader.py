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

            # Configuração de exibição
            pd.set_option("display.max_columns", None)
            pd.set_option("display.max_rows", 100)
            pd.set_option("display.expand_frame_repr", False)

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

            print("=" * 100)

            # Armazenar DataFrame no dicionário
            dataframes[name] = df

        except FileNotFoundError:
            print(f"Arquivo não encontrado: {path}")
        except pd.errors.EmptyDataError:
            print(f"Arquivo vazio: {path}")
        except Exception as e:
            print(f"Erro ao carregar {name}: {e}")

    return dataframes

if __name__ == "__main__":
    print("\nCarregando planilhas CSV")
    load_datas()
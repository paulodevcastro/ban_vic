import pandas as pd
from src.config import AGENCIAS, CLIENTES, COLAB_AGENCIA, COLABORADORES, CONTAS, PROPOSTA_CREDITO, TRANSACOES

def load_datas():
    files = {
        "Agencias": AGENCIAS,
        "Clientes": CLIENTES,
        "Colab_Agencia": COLAB_AGENCIA,
        "Colaboradores": COLABORADORES,
        "Contas": CONTAS,
        "Propostas de Crédito": PROPOSTA_CREDITO,
        "Transações": TRANSACOES
    }

    for name, path, in files.items():
        try:
            df = pd.read_csv(path)
            print(f"PLANILHA: {name}")
            print(df.head(10))
            print("-" * 50)
        except Exception as e:
            print(f"Erro ao carregar {name}", e)

if __name__ == "__main__":
    load_datas()

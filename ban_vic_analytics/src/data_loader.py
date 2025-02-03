import pandas as pd
from src.config import AGENCIAS, CLIENTES, COLAB_AGENCIA, COLABORADORES, CONTAS, PROPOSTA_CREDITO, TRANSACOES

def load_datas():
    tables = pd.read_csv(AGENCIAS)
    print(tables)

if __name__ == "__main__":
    load_datas()

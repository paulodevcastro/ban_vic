import os

# Global
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "banvic_data")

def share_datas():
    """Retorna um dicionário com os caminhos dos arquivos CSV."""
    files = {
        "AGÊNCIAS": os.path.join(DATA_DIR, "agencias.csv"),
        "CLIENTES": os.path.join(DATA_DIR, "clientes.csv"),
        "COLAB_AGENCIA": os.path.join(DATA_DIR, "colaborador_agencia.csv"),
        "COLABORADORES": os.path.join(DATA_DIR, "colaboradores.csv"),
        "CONTAS": os.path.join(DATA_DIR, "contas.csv"),
        "PROPOSTA_CREDITO": os.path.join(DATA_DIR, "propostas_credito.csv"),
        "TRANSACOES": os.path.join(DATA_DIR, "transacoes.csv"),
    }
    return files
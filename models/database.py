import sqlite3
from datetime import datetime

class TesteModel:
    def __init__(self, nome_banco="data/laboratorio.db"):
        self.conn = sqlite3.connect(nome_banco, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leituras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_transf TEXT,
                timestamp TEXT,
                tensao REAL,
                status TEXT
            )
        ''')
        self.conn.commit()

    def salvar_leitura(self, codigo, tensao):
        status = "OPERACIONAL" if tensao >= 200.0 else "CRÍTICO"
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO leituras (codigo_transf, timestamp, tensao, status)
            VALUES (?, ?, ?, ?)
        ''', (codigo, data_hora, tensao, status))
        self.conn.commit()
        return status

    def buscar_ultimo_teste(self, codigo):
        self.cursor.execute('''
            SELECT timestamp FROM leituras 
            WHERE codigo_transf = ? 
            ORDER BY id DESC LIMIT 1
        ''', (codigo,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else None
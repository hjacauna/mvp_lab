import customtkinter as ctk
import threading
import time
import random
import sqlite3
from datetime import datetime

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
class GerenciadorBanco:
    def __init__(self, nome_banco="dados_laboratorio.db"):
        self.conn = sqlite3.connect(nome_banco, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
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

    def salvar_leitura(self, codigo, tensao, status):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO leituras (codigo_transf, timestamp, tensao, status)
            VALUES (?, ?, ?, ?)
        ''', (codigo, data_hora, tensao, status))
        self.conn.commit()

    def buscar_ultimo_teste(self, codigo):
        # Busca a data do último teste realizado para este código específico
        self.cursor.execute('''
            SELECT timestamp FROM leituras 
            WHERE codigo_transf = ? 
            ORDER BY id DESC LIMIT 1
        ''', (codigo,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else None

# --- INTERFACE E LÓGICA ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppAutomacao(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = GerenciadorBanco()
        
        self.title("Sistema de Gestão de Ensaios")
        self.geometry("600x600") 

        # --- UI: IDENTIFICAÇÃO ---
        self.label_id = ctk.CTkLabel(self, text="CÓDIGO DO TRANSFORMADOR:", font=("Roboto", 12, "bold"))
        self.label_id.pack(pady=(20, 0))

        self.entry_codigo = ctk.CTkEntry(self, placeholder_text="Ex: TR-2026-X", width=250)
        self.entry_codigo.pack(pady=10)
        self.entry_codigo.bind("<KeyRelease>", self.verificar_historico) # Verifica enquanto digita

        self.label_historico = ctk.CTkLabel(self, text="", text_color="gray")
        self.label_historico.pack(pady=5)

        # --- UI: MONITORAMENTO ---
        self.frame_status = ctk.CTkFrame(self)
        self.frame_status.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_valor = ctk.CTkLabel(self.frame_status, text="Aguardando Início...", font=("Roboto", 32))
        self.label_valor.pack(pady=30)

        # --- BOTÕES ---
        self.btn_iniciar = ctk.CTkButton(self, text="Iniciar Ensaio", command=self.iniciar_teste)
        self.btn_iniciar.pack(pady=10)

        self.btn_parar = ctk.CTkButton(self, text="Parar e Finalizar", command=self.parar_teste, fg_color="red")
        self.btn_parar.pack(pady=10)

        self.coletando = False

    def verificar_historico(self, event=None):
        codigo = self.entry_codigo.get().strip()
        if codigo:
            ultima_data = self.db.buscar_ultimo_teste(codigo)
            if ultima_data:
                self.label_historico.configure(text=f"⚠️ Último teste: {ultima_data}", text_color="#FFCC00")
            else:
                self.label_historico.configure(text="✅ Novo Transformador (Sem histórico)", text_color="#00FF00")
        else:
            self.label_historico.configure(text="")

    def iniciar_teste(self):
        self.codigo_atual = self.entry_codigo.get().strip()
        
        if not self.codigo_atual:
            self.label_historico.configure(text="❌ ERRO: Insira o código antes de iniciar!", text_color="red")
            return

        if not self.coletando:
            self.coletando = True
            self.entry_codigo.configure(state="disabled") # Trava o campo durante o teste
            threading.Thread(target=self.loop_leitura, daemon=True).start()
            self.after(10000, self.parar_teste) # Para automaticamente após 10 segundos

    def loop_leitura(self):
        while self.coletando:
            valor = random.triangular(119.0, 221.0,221.0) # Simula leitura de tensão
            self.label_valor.configure(text=f"Tensão: {valor:.2f}V")
            
            status = "OPERACIONAL" if valor >= 200.0 else "CRÍTICO"
            
            # SALVANDO NO BANCO COM O CÓDIGO DO TRANSFORMADOR
            self.db.salvar_leitura(self.codigo_atual, valor, status)

            time.sleep(1)

    def parar_teste(self):
        self.coletando = False
        self.entry_codigo.configure(state="normal")
        self.label_valor.configure(text="Teste Finalizado")

if __name__ == "__main__":
    app = AppAutomacao()
    app.mainloop()
import customtkinter as ctk

class TesteView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.title("Sistema de Gestão de Ensaios")
        self.geometry("600x600")
        ctk.set_appearance_mode("dark")

        # UI Components
        self.label_id = ctk.CTkLabel(self, text="CÓDIGO DO TRANSFORMADOR:", font=("Roboto", 12, "bold"))
        self.label_id.pack(pady=(20, 0))

        self.entry_codigo = ctk.CTkEntry(self, placeholder_text="Ex: TR-2026-X", width=250)
        self.entry_codigo.pack(pady=10)
        # O bind envia o texto para o controller processar
        self.entry_codigo.bind("<KeyRelease>", lambda e: self.controller.verificar_historico(self.entry_codigo.get()))

        self.label_historico = ctk.CTkLabel(self, text="", text_color="gray")
        self.label_historico.pack(pady=5)

        self.frame_status = ctk.CTkFrame(self)
        self.frame_status.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_valor = ctk.CTkLabel(self.frame_status, text="Aguardando Início...", font=("Roboto", 32))
        self.label_valor.pack(pady=30)

        self.btn_iniciar = ctk.CTkButton(self, text="Iniciar Ensaio", command=self.controller.iniciar_teste)
        self.btn_iniciar.pack(pady=10)

        self.btn_parar = ctk.CTkButton(self, text="Parar e Finalizar", command=self.controller.parar_teste, fg_color="red")
        self.btn_parar.pack(pady=10)

    def atualizar_valor(self, texto):
        self.label_valor.configure(text=texto)

    def atualizar_historico(self, texto, cor):
        self.label_historico.configure(text=texto, text_color=cor)

    def set_entrada_estado(self, estado):
        self.entry_codigo.configure(state=estado)
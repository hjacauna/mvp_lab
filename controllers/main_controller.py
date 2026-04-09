import threading
import time
import random
from models.database import TesteModel
from views.main_view import TesteView

class TesteController:
    def __init__(self):
        self.model = TesteModel()
        self.view = TesteView(self)
        self.coletando = False

    def verificar_historico(self, codigo):
        codigo = codigo.strip()
        if not codigo:
            self.view.atualizar_historico("", "gray")
            return

        ultima_data = self.model.buscar_ultimo_teste(codigo)
        if ultima_data:
            self.view.atualizar_historico(f"⚠️ Último teste: {ultima_data}", "#FFCC00")
        else:
            self.view.atualizar_historico("✅ Novo Transformador (Sem histórico)", "#00FF00")

    def iniciar_teste(self):
        codigo = self.view.entry_codigo.get().strip()
        if not codigo:
            self.view.atualizar_historico("❌ ERRO: Insira o código!", "red")
            return

        if not self.coletando:
            self.coletando = True
            self.view.set_entrada_estado("disabled")
            threading.Thread(target=self._loop_leitura, args=(codigo,), daemon=True).start()
            self.view.after(10000, self.parar_teste)

    def _loop_leitura(self, codigo):
        while self.coletando:
            valor = random.triangular(119.0, 221.0, 221.0)
            self.model.salvar_leitura(codigo, valor)
            self.view.atualizar_valor(f"Tensão: {valor:.2f}V")
            time.sleep(1)

    def parar_teste(self):
        if self.coletando:
            self.coletando = False
            self.view.set_entrada_estado("normal")
            self.view.atualizar_valor("Teste Finalizado")

    def run(self):
        self.view.mainloop()
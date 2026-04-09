import os
from controllers.main_controller import TesteController

# Garante que a pasta 'data' existe para o banco de dados
if not os.path.exists('data'):
    os.makedirs('data')

if __name__ == "__main__":
    app = TesteController()
    app.run()
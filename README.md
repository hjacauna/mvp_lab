# MVP Lab — Sistema de Gestão de Ensaios

Aplicação desktop em **Python + CustomTkinter** para simular ensaios de transformadores, monitorar valores de tensão em tempo real e registrar leituras em banco de dados SQLite.

## Funcionalidades

- Cadastro do código do transformador antes de iniciar o ensaio.
- Consulta automática de histórico do último teste por código informado.
- Simulação contínua de leitura de tensão durante o ensaio.
- Classificação do status da leitura:
  - `OPERACIONAL` para tensão maior ou igual a `200.0V`
  - `CRÍTICO` para tensão abaixo de `200.0V`
- Persistência dos dados em banco local `SQLite` (`dados_laboratorio.db`).
- Finalização automática do ensaio após 10 segundos (ou manual pelo botão de parada).

## Estrutura do projeto

```text
.
├── main.py
└── README.md
```

## Requisitos

- Python 3.10+
- Dependências Python:
  - `customtkinter`

## Instalação

1. (Opcional) Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
```

2. Instale as dependências:

```bash
pip install customtkinter
```

## Como executar

```bash
python main.py
```

## Banco de dados

Ao iniciar a aplicação, a tabela `leituras` é criada automaticamente (se não existir) com os seguintes campos:

- `id` (INTEGER, PK, autoincrement)
- `codigo_transf` (TEXT)
- `timestamp` (TEXT)
- `tensao` (REAL)
- `status` (TEXT)

O arquivo do banco é criado no diretório do projeto com o nome `dados_laboratorio.db`.

## Observações

- A leitura de tensão é simulada (não há integração com hardware real nesta versão).
- A interface usa tema escuro por padrão.
- O botão **Parar e Finalizar** interrompe o ciclo de coleta e reabilita o campo de código.

## Próximos passos sugeridos

- Exportação dos dados para CSV.
- Dashboard com gráfico de tendência de tensão.
- Filtros por período e por código de transformador.
- Integração com sensores/dispositivos reais.

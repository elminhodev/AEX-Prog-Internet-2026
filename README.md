# Funilaria Preço

Sistema web para apoiar a organização de uma funilaria. A aplicação registra orçamentos e serviços, estima custos e lucros, organiza a fila de trabalho e oferece relatórios sobre os serviços concluídos.

O projeto foi desenvolvido com **Python**, **Django** e **SQLite**.

## Funcionalidades

- Autenticação de usuários para acesso ao sistema.
- Cadastro, edição e exclusão de serviços.
- Registro de cliente, veículo, tipo de serviço, urgência, prazo, valor e responsáveis por cada etapa.
- Inclusão de materiais e seus respectivos custos em cada serviço.
- Cálculo de custo previsto, lucro previsto, lucro por dia e lucro real.
- Fila de serviços em execução priorizada por lucro diário e nível de urgência.
- Fixação manual de serviços no topo da fila.
- Marcação de serviços concluídos.
- Configuração de custos fixos, dias úteis, vagas do pátio e margem de lucro padrão.
- Cadastro e remoção de integrantes da equipe.
- Registro de retrabalho/prejuízo, etapa responsável e custo do erro.
- Relatório de faturamento, lucro, perdas por atraso ou erro, desempenho da equipe e rentabilidade por tipo de serviço.

## Regra de priorização da fila

Os serviços em execução são ordenados pela seguinte lógica:

1. Serviços fixados manualmente aparecem primeiro.
2. Os demais são classificados pelo *score* de prioridade:

   `lucro previsto por dia × peso da urgência`

Os pesos de urgência são:

| Urgência | Peso |
| --- | ---: |
| Normal | 1,0 |
| Alta | 1,5 |
| Urgente | 2,5 |

## Tecnologias

- Python 3
- Django 5
- SQLite
- HTML e CSS

## Como executar

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd AEX-Prog-Internet-2026
```

### 2. Crie e ative um ambiente virtual

No Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Aplique as migrações do banco de dados

```bash
python manage.py migrate
```

### 5. Carregue os dados de demonstração (opcional)

```bash
python manage.py seed
```

Esse comando cria custos iniciais, funcionários, serviços de exemplo e o usuário abaixo:

| Campo | Valor |
| --- | --- |
| Usuário | `joaodev` |
| Senha | `123123` |

### 6. Inicie o servidor

```bash
python manage.py runserver
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/) no navegador e entre com um usuário cadastrado.

## Estrutura do projeto

```text
.
├── config/                 # Configurações e rotas principais do Django
├── oficina/                # Aplicação principal
│   ├── management/commands/# Comando para carga de dados de exemplo
│   ├── migrations/         # Migrações do banco de dados
│   ├── static/css/         # Estilos da interface
│   ├── templates/          # Páginas HTML
│   ├── forms.py            # Formulários e validações
│   ├── models.py           # Modelos e regras de cálculo
│   └── views.py            # Fluxos e páginas da aplicação
├── manage.py               # Comandos administrativos do Django
├── requirements.txt        # Dependências do projeto
└── RELATORIO.md            # Relatório acadêmico do trabalho
```

## Rotas principais

| Rota | Descrição |
| --- | --- |
| `/` | Fila de serviços em execução |
| `/servicos/novo/` | Cadastro de orçamento/serviço |
| `/custos/` | Configuração de custos e equipe |
| `/relatorio/` | Indicadores e relatórios |
| `/admin/` | Administração nativa do Django |

## Observações

- O banco de dados é criado localmente no arquivo `db.sqlite3` após a execução das migrações.
- As chaves e configurações atuais foram preparadas para desenvolvimento local. Antes de publicar a aplicação, atualize a `SECRET_KEY`, defina `DEBUG = False` e configure `ALLOWED_HOSTS`.

## Autores

Projeto acadêmico de Programação para Internet. Inclua aqui os nomes dos integrantes da equipe.

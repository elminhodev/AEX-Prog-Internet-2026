# Funilaria Preço

Sistema web para apoiar a organização de uma funilaria. A aplicação registra orçamentos e serviços, estima custos e lucros, organiza a fila de trabalho e oferece relatórios sobre os serviços que foram concluídos.

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
- Validação do formato da placa no campo "Veículo e placa" (padrão antigo e Mercosul).

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

## Validação da placa do veículo

O campo **Veículo e placa** aceita o modelo junto com a placa (por exemplo, `Gol, ABC-1234`), mas exige que exista uma placa em um dos formatos brasileiros:

| Padrão | Formato | Exemplo |
| --- | --- | --- |
| Antigo | 3 letras + 4 números (hífen opcional) | `ABC-1234` ou `ABC1234` |
| Mercosul | 3 letras + número + letra + 2 números | `BRA2E19` |

- Letras minúsculas são aceitas e convertidas para maiúsculas.
- A placa é padronizada ao salvar: padrão antigo com hífen (`ABC-1234`) e Mercosul sem hífen (`BRA2E19`).
- Valores como `XXX-XXXX-`, `Gol` ou `ABC-12` são recusados com a mensagem "Informe uma placa válida (ex.: ABC-1234 ou ABC1D23).".
- O campo continua opcional: se ficar vazio, o serviço é salvo normalmente.
- A validação confere apenas o **formato**; ela não verifica se a placa existe de fato.
- Serviços cadastrados antes dessa validação só serão checados quando forem editados e salvos novamente.

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

Se o PowerShell bloquear a ativação com a mensagem de que a execução de scripts está desabilitada, libere os scripts apenas para a janela atual e ative novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Quando o ambiente virtual estiver ativo, o terminal mostra `(.venv)` no início da linha. Execute o `pip install` e os comandos `python manage.py ...` somente com ele ativo.

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

> **Atenção:** o usuário `joaodev` já existe no `db.sqlite3` que acompanha o repositório. O comando `seed`, por sua vez, cria o usuário `dono` com a senha `funilaria123` quando ele não existe. Se você começar com um banco novo (apagando o `db.sqlite3` e rodando `migrate`), use `dono` / `funilaria123`. Para criar outro acesso, use `python manage.py createsuperuser`.

### 6. Inicie o servidor

```bash
python manage.py runserver
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/) no navegador e entre com um usuário cadastrado.

O servidor de desenvolvimento já vem com o Django, não é preciso instalar nada além do `requirements.txt`. Para pará-lo, volte ao terminal e pressione `Ctrl + C`.

### 7. Rode os testes automatizados

```bash
python manage.py test
```

O resultado esperado termina com `OK`. Os testes ficam em `oficina/tests.py` e cobrem a validação da placa.

## Como usar a aplicação

1. **Entrar:** acesse `/` e faça login. Sem login, o sistema redireciona para a tela de entrada.
2. **Configurar custos e equipe:** em **Custos**, informe aluguel, energia, água, salários, outros custos, dias úteis, vagas do pátio e margem de lucro padrão. Cadastre também os funcionários que executam cada etapa.
3. **Criar um orçamento:** em **Orçamento**, preencha cliente, veículo e placa (por exemplo, `Gol, ABC-1234`), tipo de serviço, urgência, responsáveis, prazo e materiais. O valor total é sugerido a partir do custo do pátio, dos materiais e da margem, e pode ser ajustado manualmente.
4. **Acompanhar a fila:** em **Serviços**, os serviços em execução aparecem ordenados por prioridade. É possível editar, fixar no topo, concluir ou excluir cada um.
5. **Concluir um serviço:** ao concluir, informe os valores reais (materiais gastos e, se houver, o custo e a etapa de um erro ou retrabalho) editando o serviço.
6. **Consultar o relatório:** em **Relatório**, veja faturamento, lucro real, perdas por atraso e erro, erros por funcionário e lucro por tipo de serviço.

## Solução de problemas

| Problema | O que fazer |
| --- | --- |
| `ModuleNotFoundError: No module named 'django'` | O Django não está instalado no Python em uso. Ative o ambiente virtual (`(.venv)` no terminal) e rode `pip install -r requirements.txt`. |
| PowerShell diz que a execução de scripts está desabilitada | Rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` e ative o ambiente novamente. |
| `python manage.py` não faz nada | Falta o comando. Use, por exemplo, `python manage.py runserver` ou `python manage.py test`. |
| O campo de placa rejeita um valor que parece correto | Confira o formato: 3 letras + 4 números, ou 3 letras + número + letra + 2 números. Veja a seção "Validação da placa do veículo". |
| Não consigo entrar no sistema | Use `joaodev` / `123123` com o banco do repositório, ou `dono` / `funilaria123` após o `seed` em um banco novo. |

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
│   ├── tests.py            # Testes automatizados
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
- O arquivo `db.sqlite3` está versionado no repositório. Ao testar, evite enviar dados de teste ao GitHub: adicione ao commit apenas os arquivos que você alterou, em vez de usar `git add .`.
- A pasta do ambiente virtual (`.venv/`) é local e não deve ser enviada ao repositório.

## Autores

Projeto acadêmico de Programação para Internet. Inclua aqui os nomes dos integrantes da equipe.

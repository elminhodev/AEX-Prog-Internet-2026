# Funilaria Preço

Sistema web para uma funilaria: orçamento, fila de serviços priorizada pelo **lucro por dia de pátio**, custos fixos, equipe e relatório de lucro/erros.

Projeto da AEX — Programação para Internet (UENP, Campus Luiz Meneghel), em conjunto com Engenharia de Software II.

## Integrantes
- (nome 1)
- (nome 2)
- (nome 3)

## Tecnologias
Python 3 · Django 5 · SQLite · HTML/CSS (templates Django)

## Como executar
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed           # cria usuário de teste e dados de exemplo
python manage.py runserver
```
Abra http://127.0.0.1:8000/

**Usuário de teste:** `dono` / `funilaria123`  (também acessa /admin/)

## Funcionalidades
- Login/logout
- **Serviços (CRUD completo):** cadastrar orçamento com materiais, listar a fila, editar, concluir, fixar e excluir
- Fila ordenada por lucro/dia × urgência
- **Custos:** custos fixos e cadastro da equipe
- **Relatório:** faturamento, lucro real, erros por funcionário e lucro por tipo

## Estrutura
- `config/` — configurações do projeto
- `oficina/models.py` — tabelas e regras de cálculo
- `oficina/views.py`, `urls.py`, `forms.py` — lógica das telas
- `oficina/templates/` — páginas HTML

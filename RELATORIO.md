# Relatório — Funilaria Preço

**Integrantes:** João Gabriel de Araujo Meira, José Elmo de Oliveira Filho, Murilo Costa da Silva, MUrilo Aba Ferraz, Murilo Dias

## O que foi implementado
(login, CRUD de serviços com materiais, fila por lucro/dia, custos e equipe, relatório) + prints das telas.

## O que ficou de fora
(ex.: perfis Dono/Gerente com permissões diferentes, responsável "Patrão" na pintura)

## O que mudou em relação à modelagem
- O protótipo guardava os dados no navegador (localStorage); agora usa banco de dados SQLite via Django.
- (outras mudanças)

## Dificuldades encontradas
- Encontrar a melhor maneira de precificar cada serviço, e após um longo diálogo chegamos a encontrar o valor de custo de cada carro por dia por vaga no patio da empresa.
- Tratamento de erros nos formulários relacionados: compreender como o Django identifica dados inválidos e utiliza ValidationError e add_error() para apresentar mensagens específicas ao usuário.
- Integração com o banco de dados: entender como os formulários utilizam os modelos Serviço, Material e ConfiguracaoCustos para validar e preparar os dados que serão armazenados no SQLite.

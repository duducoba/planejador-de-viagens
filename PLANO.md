# Planejamento — Planejador de viagens

Trabalho final de Computação 2 da UFRJ. Trabalho individual.

Atualizado em 26/11/2026. Prazo de entrega e data da apresentação: a confirmar.
Validação do tema e do plano pelo professor: pendente.

## 1. Problema e resultado esperado

O projeto ajudará uma pessoa a organizar os gastos de viagens e verificar se
eles cabem no orçamento. O usuário informará manualmente destino, duração,
orçamento e despesas em reais. O aplicativo mostrará custo total, saldo e
custo médio diário. A comparação visual e a recuperação dos cadastros por arquivos JSON estão implementadas.

O resultado esperado é um aplicativo simples, funcional, documentado e
publicado, cujo código o aluno consiga compreender e explicar.

Não fazem parte desta versão: pesquisa automática de preços, passagens ou
hospedagem, reservas, login e IA dentro do aplicativo.

## 2. Objetivos de aprendizagem e ferramentas

- Compreender classes, objetos, atributos, métodos e composição.
- Separar regras e cálculos da interface, mantendo código organizado e reutilizável.
- Validar entradas e tratar exceções com mensagens compreensíveis.
- Aprender a construir formulários e manter o estado da sessão no Streamlit.
- Explorar gráficos interativos com Plotly.
- Aprender a exportar e importar dados em JSON.
- Usar Git e GitHub e publicar no Streamlit Community Cloud.
- Testar o programa e comunicar suas decisões, limitações e aprendizados.

Python, Streamlit, Plotly e JSON já são usados. Os testes existentes usam `unittest` e o `AppTest`
do Streamlit. GitHub e Community Cloud já são usados na publicação.

## 3. Organização e diagrama de classes

As regras e os cálculos ficam em `modelos.py`. A interface em `app.py` cria
e utiliza os objetos, mostra resultados e trata erros. O exemplo executável
fica em `exemplo.py`; o teste de interface, em `test_interface.py`.

```text
PlanejadorViagens
  atributo: viagens
  métodos: adicionar_viagem(viagem)
           encontrar_viagens(destino)
           comparar_viagens()
           exportar_json()
           importar_json(conteudo)
        |
        | contém 0 ou mais
        v
Viagem
  atributos: destino, duracao, orcamento, despesas
  métodos: adicionar_despesa(despesa)
           custo_total()
           saldo()
           custo_medio_diario()
           gastos_por_categoria()
        |
        | contém 0 ou mais
        v
Despesa
  atributos: descricao, categoria, valor
```

`Despesa` representa um gasto. `Viagem` reúne gastos e calcula seus resultados.
`PlanejadorViagens` reúne viagens, busca destinos e compara custos.
A organização usa composição: objetos são reunidos em outros objetos.
Não há necessidade identificada de acrescentar herança neste modelo.

## 4. Requisitos e progresso

| Requisito | Situação |
| --- | --- |
| Cadastrar destino, duração e orçamento | Implementado |
| Adicionar despesas com descrição, categoria e valor | Implementado |
| Calcular total, saldo e custo médio diário nas classes | Implementado |
| Rejeitar textos vazios, duração inválida e valores negativos ou não finitos | Implementado nas classes |
| Selecionar uma viagem, consultar despesas e avisar sobre saldo negativo | Implementado na interface |
| Preservar cadastros durante as interações da sessão | Implementado com `st.session_state` |
| Encontrar e comparar viagens no núcleo | Implementado |
| Exibir comparação e gráficos na interface | Implementado; testes automatizados passaram e o agente conferiu tabela e gráficos locais com a demonstração |
| Exportar e importar viagens em JSON | Implementado e verificado por testes automatizados; arquivo inválido mantém os dados atuais |
| Documentar instalação e execução no Windows | Implementado no README |
| Apresentar diagrama das classes | Diagrama textual disponível |
| Conferir visualmente o aplicativo no navegador | Realizada pelo aluno em `localhost:8501`, com funcionamento relatado; funções experimentadas não detalhadas |
| Validar tema e plano inicial com o professor | Pendente |
| Publicar código no GitHub e aplicativo no Community Cloud | Concluído; código e aplicativo publicados, links conferidos |
| Responder ao formulário atual | Respondido pelo aluno, conforme seu relato |
| Acompanhar futuros formulários e registrar aprendizados | Pendente de acompanhamento |
| Preparar apresentação presencial e conferir links de entrega | Roteiro, demonstração e perguntas preparados em material pessoal do aluno; links públicos conferidos; ensaio pendente |

Na Parte 3, os quatro testes automatizados passaram, assim como o exemplo
do núcleo. Foram conferidos os valores da tabela e dos gráficos contra as
classes, categorias, destinos iguais, mudança de ordenação e seleção, sessão,
ausência de despesas e valores zero. `pip check` não encontrou conflitos.
Esses resultados não indicam quais funções o aluno experimentou manualmente.

O aluno informou que abriu o aplicativo em `localhost:8501`, utilizou a
interface e ela funcionou em sua conferência visual. Como não detalhou as
funções experimentadas, esse relato não confirma teste manual de cada
cadastro, cálculo, validação, aviso ou comportamento da sessão. Não foram
marcadas funções específicas como testadas manualmente. Esse relato é anterior
à Parte 3. Depois da Parte 4, o agente carregou a demonstração em uma sessão
local separada e conferiu visualmente os dois gráficos e os valores da tabela.
Isso não registra novas funções como testadas pelo aluno.

O formulário atual foi respondido pelo aluno. Isso não confirma aprovação
do professor nem substitui eventuais formulários futuros. A validação do
professor e os prazos continuam pendentes.

O repositório local está conectado a https://github.com/duducoba/planejador-de-viagens.
O código e os dados fictícios foram publicados na branch main. O aplicativo
está publicado em https://planejador-de-viagens-duducoba.streamlit.app/

## 5. Orientações acadêmicas e diferenças em relação ao plano inicial

O documento do trabalho final pede programa funcional, foco em orientação a
objetos, exploração de ferramentas novas, código comentado e documentado,
facilidade de execução, apresentação e respostas aos formulários. Também pede
reflexão sobre acertos, dificuldades e aprendizados. O aluno precisa explicar
o código, inclusive quando recebe auxílio de ferramentas de IA.

O plano inicial deve apresentar problema, objetivos de aprendizagem,
ferramentas, resultado esperado, organização com diagrama, forma de
apresentação, divisão de tarefas quando houver grupo e cronograma que
considere as provas. Este documento formaliza esses itens; as datas continuam
pendentes e a aprovação do professor não deve ser presumida.

A ementa inclui orientação a objetos, exceções, interfaces, persistência e
código organizado. É uma proposta de conteúdo do curso, não uma exigência
explícita de que todo projeto use herança, todas as bibliotecas ou IA.

O aviso recente do Classroom orienta esta entrega:

- Apresentação presencial cronometrada de 2 minutos, seguida de perguntas.
- Quem usa Streamlit deve publicar no Streamlit Community Cloud.
- Enviar links do aplicativo, GitHub e dados usados antes da apresentação,
  com acesso conferido.
- Explicar por que o projeto foi feito, como foi organizado e o que faz.
- Mostrar as classes e preparar a demonstração; slides com pouco texto.

Assim, a apresentação presencial substitui neste planejamento as alternativas
de vídeo ou relatório citadas no PDF. A publicação passa a ser requisito.
O diagrama será mantido: ele já integra a orientação do plano inicial.

## 6. Decisões sobre dados e persistência

Os preços são informados pelo usuário; não existe uma base externa de preços.
Os exemplos em `dados/demonstracao.json` são fictícios e identificados como tais.
Será proposto ao professor um link para o JSON demonstrativo no GitHub como
link dos dados usados. A aceitação dessa forma de entrega ainda será confirmada.

A Parte 4 implementou importação/exportação JSON: o usuário baixa
um arquivo e pode carregá-lo depois. O estado da sessão não é salvamento
permanente, e o armazenamento local do Community Cloud não tem permanência
garantida. Não será criado banco externo nesta versão.

A importação valida todo o conteúdo antes de substituir os cadastros
da sessão. Um arquivo inválido produz mensagem de erro sem apagar
as viagens existentes. Essas funções estão implementadas e testadas. O arquivo completo é validado em um novo planejador antes de substituir a sessão.

## 7. Etapas e cronograma por marcos

| Ordem | Etapa | Critério de conclusão | Prazo |
| --- | --- | --- | --- |
| 1 | Formalizar e validar o planejamento | Documento preparado e plano discutido com o professor; aprovação registrada quando ocorrer | A confirmar |
| 2 | Encerrar a revisão da interface | Conferência visual geral relatada pelo aluno; ainda detalhar cenários experimentados e revisar a compreensão do fluxo entre tela e classes | A confirmar |
| 3 | Comparação e gráficos | Implementação, testes e conferência local dos gráficos com a demonstração concluídos | Concluída tecnicamente |
| 4 | Importação/exportação JSON | Implementada; sete testes passaram, incluindo upload inválido sem perda dos cadastros | Concluída tecnicamente |
| 5 | Publicação e conferência | GitHub e Community Cloud acessíveis, dependências declaradas e links públicos conferidos | Concluída tecnicamente |
| 6 | Documentação e apresentação | README e diagrama atualizados; roteiro, demonstração e perguntas preparados; reflexão pessoal e ensaio pendentes | Antes da apresentação; data a confirmar |

Os cálculos permanecem nas classes: `gastos_por_categoria()` soma por categoria
em `Viagem`, e a comparação visual aproveita `comparar_viagens()`. Cada resumo
inclui o número original do cadastro para distinguir destinos iguais sem
depender da ordenação. Tabela e gráfico de custos usam os mesmos resumos.
Categorias com grafias diferentes são mantidas separadas. Sem despesas, a
interface orienta o usuário em vez de mostrar um gráfico de categorias vazio.

Na publicação, `app.py` é a entrada do Community Cloud, com Python 3.12 e
dependências declaradas em `requirements.txt`. O funcionamento publicado foi
conferido pelo agente; os links responderam sem autenticação.

O trabalho é individual: planejamento, implementação, testes, documentação,
publicação e apresentação ficam sob responsabilidade do aluno. As datas serão
definidas após confirmação do prazo, considerando disponibilidade e provas.

## 8. Apresentação e entrega final

| Tempo | Conteúdo |
| --- | --- |
| 0:00–0:20 | Por quê: organizar gastos e verificar se a viagem cabe no orçamento |
| 0:20–0:50 | Como: diagrama das três classes, ferramentas e separação entre lógica e interface |
| 0:50–1:40 | O quê: demonstrar viagens previamente carregadas, adicionar despesa e mostrar resultados e comparação |
| 1:40–2:00 | Principal aprendizado e limitação dos valores informados manualmente |

Preparar no máximo dois slides com pouco texto, além do aplicativo. Ensaiar
com cronômetro e manter capturas da demonstração para eventual falha de conexão.
Preparar respostas sobre objetos, métodos, cálculos, validação, sessão e JSON.

Checklist de entrega:

- [ ] Código organizado, comentado e compreendido pelo aluno.
- [x] README atualizado com instalação, execução e limitações.
- [x] Diagrama atualizado com métodos de importação/exportação.
- [x] Testes automatizados dos cálculos, interface, comparação e importação/exportação.
- [ ] Registro do que funcionou, dificuldades e aprendizados reais.
- [x] Formulário atual respondido, conforme relato do aluno (prazo não confirmado).
- [ ] Acompanhar e responder eventuais novos formulários nos prazos definidos.
- [x] Links do aplicativo, GitHub e dados demonstrativos conferidos.
- [ ] Links enviados pelo Classroom antes da apresentação.
- [x] Demonstração fictícia e roteiro de 2 minutos preparados.
- [ ] Apresentação ensaiada pelo aluno em até 2 minutos.

## 9. Decisões pendentes

1. Validar tema e plano inicial com o professor.
2. Confirmar entrega, apresentação e prazos dos formulários.
3. Informar disponibilidade e provas para preencher o cronograma.
4. Confirmar com o professor como informar o link de dados de entrada manual.

## 10. Fontes do planejamento

- `TRABALHO FINAL.pdf`, fornecido pelo aluno: objetivos, plano inicial,
  entregáveis, apresentação e exemplos de ferramentas.
- `Ementa e Proposta de plano de curso.pdf`, fornecido pelo aluno: conteúdos
  do curso e proposta de organização, sem tratar sugestões como exigências
  adicionais específicas deste projeto.
- Aviso recente do Classroom transcrito pelo aluno: apresentação presencial,
  publicação e entrega dos links.
- [Publicação no Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).
- [Persistência local no Community Cloud](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data).

Este documento registra planejamento e progresso; não comprova aprovação do
professor nem envio dos links finais ao Classroom. As Partes 1 a 3 e a persistência JSON estão implementadas.
Código publicado no GitHub; aplicativo publicado no Community Cloud e links conferidos. O material da Parte 5
está preparado; aprovação, envio ao Classroom e ensaio continuam pendentes.


## 11. Verificação das Partes 4 e 5

- JSON exporta entradas e reconstrói objetos pelas validações existentes.
- Dados fictícios disponíveis em `dados/demonstracao.json` e no botão da interface.
- Sete testes passaram: núcleo, gráficos, sessão e upload JSON. Incluem importação
  parcialmente inválida, versão incompatível, tipos incorretos, UTF-8, lista vazia
  e limite de tamanho. A sessão só é substituída depois de validar todo o arquivo.
- O roteiro, as ações e as perguntas para estudo ficam em material pessoal, fora do repositório público.
- README e diagrama atualizados. Dependências diretas fixadas nas versões testadas.
- GitHub criado pelo aluno e código publicado pelo agente via plugin conectado.
  Aplicativo publicado no Streamlit Community Cloud com Python 3.12.
- Aprovação do professor, prazo, envio ao Classroom e ensaio do aluno permanecem pendentes.

Conferência local pelo agente: demonstração carregada e dois gráficos inspecionados
no navegador; custos de Petrópolis R$ 850 e Paraty R$ 1.150, categorias de Paraty
R$ 300, R$ 600 e R$ 250. Isso não comprova ensaio do aluno ou acesso público.

Links do código e dos dados publicados:

- https://github.com/duducoba/planejador-de-viagens
- https://github.com/duducoba/planejador-de-viagens/blob/main/dados/demonstracao.json

URL pública do aplicativo: https://planejador-de-viagens-duducoba.streamlit.app/

Conferência final em 26/11/2026: aplicativo, repositório e JSON bruto responderam
HTTP 200 sem autenticação. No navegador, o agente carregou a demonstração,
conferiu gráficos e tabela, adicionou passeio de R$ 100 a Paraty e verificou
total R$ 1.250, saldo R$ 250 e média R$ 416,67. Selecionou Petrópolis e
conferiu R$ 850, saldo R$ -50, média R$ 425 e aviso de orçamento ultrapassado.
Importação/exportação foi verificada nos testes locais; não foi feita conferência
manual completa de upload/download na nuvem. Isso não equivale ao ensaio do aluno.

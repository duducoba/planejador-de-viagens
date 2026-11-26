# Planejador de viagens — Computação 2 / UFRJ

Núcleo em Python do trabalho de Computação 2 da UFRJ. Os valores são
informados manualmente em reais. O núcleo usa a biblioteca padrão do Python;
a interface usa Streamlit e os gráficos usam Plotly, declarados em `requirements.txt`.

## Aplicativo publicado

[Abrir planejador de viagens](https://planejador-de-viagens-duducoba.streamlit.app/) — funciona no navegador, sem instalar Python.
Para experimentar, clique em **Carregar demonstração fictícia** na barra lateral.

## Instalar e executar no Windows

Instale o Python 3.12 pelo [site oficial](https://www.python.org/downloads/windows/),
incluindo o launcher `py`. Abra o PowerShell na pasta do projeto e execute:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Esses comandos criam um ambiente virtual na pasta `.venv`, instalam as
dependências nele e iniciam a interface. Não é preciso ativar o ambiente nem
alterar a política de execução do PowerShell. Se `py` não existir, mas
`python --version` indicar Python 3.12, use `python -m venv .venv` no primeiro comando.

Abra o endereço local exibido no terminal (normalmente `http://localhost:8501`).
Para encerrar, pressione `Ctrl+C` no terminal. Nas próximas execuções, basta
usar o terceiro comando. Não envie a pasta `.venv` com o trabalho; ela pode
ser recriada com os dois primeiros comandos em outro computador.

Para executar apenas o exemplo da Parte 1:

```powershell
.\.venv\Scripts\python.exe exemplo.py
```

## Como usar a tela

1. Preencha destino, duração e orçamento e clique em **Cadastrar viagem**.
2. Use **Selecione uma viagem** para consultar um cadastro. O número distingue
   viagens com o mesmo destino; a viagem recém-criada é selecionada automaticamente.
3. Preencha descrição, categoria e valor total e clique em **Adicionar despesa**.
4. Consulte as despesas e o resumo. Um aviso aparece se o saldo for negativo.
5. Veja o gráfico de gastos por categoria da viagem selecionada.
6. Consulte a tabela comparativa e o gráfico de custo total de todas as viagens,
   ordenados pelo menor custo total. Os números dos cadastros distinguem destinos iguais.

Se já tinha o ambiente virtual da Parte 2, instale a nova dependência antes de abrir:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

A tabela mostra duração, orçamento, total, saldo e média diária. Ela e o gráfico
de custos usam os mesmos resumos de `comparar_viagens()`. O método
`Viagem.gastos_por_categoria()` soma os gastos para o outro gráfico. A interface
apenas apresenta esses resultados com Plotly; não repete os cálculos.

Os gráficos são de barras e mostram valores em reais ao passar o mouse.
Sem despesas, aparece uma orientação em lugar do gráfico por categoria.
Despesas de valor zero são permitidas. Categorias com grafias diferentes,
como `Alimentação` e `alimentação`, são separadas; use a mesma grafia para agrupá-las.
O número de cada viagem é sua posição original de cadastro, não sua posição
na ordenação por custo. A numeração não muda ao adicionar despesas.

Referências dos gráficos: [barras no Plotly](https://plotly.com/python/bar-charts/)
e [Plotly no Streamlit](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart).

Os formulários só enviam os valores ao clicar no botão. Os campos são limpos
após o envio; se aparecer uma mensagem de erro, preencha novamente.

`st.session_state` guarda o objeto `PlanejadorViagens` entre as reexecuções
da interface. Assim, selecionar uma viagem ou enviar um formulário não apaga
os cadastros. Isso **não é salvamento permanente**: recarregar ou fechar a aba,
ou reiniciar o servidor, pode perder os dados; outra sessão começa vazia.

A tela cria objetos `Viagem` e os entrega ao planejador. Para adicionar um
gasto, cria uma `Despesa` e a entrega à viagem selecionada. Os resultados
vêm dos métodos de `Viagem`; a interface apenas formata os valores em reais.

Referências: [instalação do Streamlit](https://docs.streamlit.io/get-started/installation/command-line)
e [estado de sessão](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state).

## Exemplo da Parte 1

O exemplo cria duas viagens, adiciona despesas, busca um destino e compara
os custos. Também verifica os cálculos e a rejeição de duração zero e despesa
negativa. Ao final, deve aparecer `Todas as verificações passaram.`

| Destino | Dias | Orçamento | Custo total | Saldo | Média diária |
| --- | --- | --- | --- | --- | --- |
| Petrópolis | 2 | R$ 800,00 | R$ 850,00 | -R$ 50,00 | R$ 425,00 |
| Paraty | 3 | R$ 1.500,00 | R$ 1.150,00 | R$ 350,00 | R$ 383,33 |

O terminal exibe os números com ponto decimal. Os cálculos usam `float`,
o tipo numérico decimal básico do Python; a exibição tem duas casas decimais.
`isclose` compara resultados considerando pequenas aproximações desse tipo.

## Organização e conceitos

- `modelos.py`: classes e validações, sem entrada de teclado ou interface.
- `app.py`: interface Streamlit e estado da sessão.
- `requirements.txt`: dependências diretas fixadas nas versões testadas.
- `test_interface.py`: teste automatizado das interações e do estado de sessão.
- `test_modelos.py`: testes de categorias e identificação na comparação.
- `.gitignore`: evita incluir ambiente virtual e caches no Git.
- `exemplo.py`: demonstração de uso e verificações executáveis.
- `README.md`: instruções e diagrama inicial.

Uma **classe** é um molde; um **objeto** é uma instância concreta desse molde.
Por exemplo, `paraty` é um objeto da classe `Viagem`. Os **atributos** guardam
dados e os **métodos** são funções que pertencem ao objeto. `__init__` prepara
o objeto quando ele é criado; `self` representa o próprio objeto.

## Diagrama de classes

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

Essa relação é composição: objetos maiores reúnem objetos menores.
Não é necessário usar herança neste modelo.

## Regras desta versão

- Duração: número inteiro de dias maior que zero.
- Orçamento e despesas: números finitos e não negativos; zero é permitido.
- Destino, descrição e categoria: textos não vazios. Categorias são livres.
- Cada despesa representa um valor total, sem multiplicação automática pelos dias.
- Custo total é a soma das despesas; saldo é orçamento menos custo total;
  média diária é custo total dividido pela duração.
- Saldo negativo é permitido e indica orçamento ultrapassado.
- A busca usa o destino completo, ignora maiúsculas e retorna todas as
  correspondências (ou uma lista vazia). Acentos continuam significativos.
- A comparação retorna uma lista de dicionários ordenada pelo custo total,
  incluindo orçamento, duração, saldo e média diária. Não altera a ordem do cadastro.
- As validações acontecem na criação dos objetos e nos métodos de inclusão.
  Neste núcleo didático, use esses métodos e evite alterar atributos diretamente.

Os dados da sessão podem ser exportados e importados em JSON pela barra lateral.
O código e os dados estão no GitHub, e o aplicativo está publicado no Streamlit Community Cloud.

## Verificar a interface

O Streamlit inclui a ferramenta `AppTest`, que simula interações sem abrir
um navegador. Para rodar o teste:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
```

O teste verifica cadastro, campos vazios, inclusão de despesa, resumo e aviso
de saldo negativo, seleção entre destinos iguais, manutenção dos dados após
reexecução e isolamento de uma nova sessão. Não substitui a conferência visual
da tela no navegador.

Verificação da Parte 3: Python 3.12, Streamlit 1.67.0 e Plotly 7.2.0 em `.venv`.
Os quatro testes passaram, assim como `exemplo.py`. `pip check` não encontrou
conflitos de dependências. Os testes conferem todas as colunas da comparação
e os rótulos e valores efetivamente enviados aos gráficos, incluindo destinos
iguais, reordenação após despesa, troca da seleção, categorias repetidas,
valores zero e ausência de despesas. O uso de JSON no teste apenas lê o formato
interno do gráfico Plotly. Na Parte 4, a persistência JSON também foi implementada.

O aluno relatou conferência visual da interface anterior em `localhost:8501`,
sem detalhar funções experimentadas. Depois da Parte 4, o agente carregou a
demonstração no navegador local e conferiu a tabela e os dois gráficos: custos
de R$ 850 e R$ 1.150; categorias de Paraty de R$ 300, R$ 600 e R$ 250.
Essa verificação não equivale a um ensaio do aluno nem a publicação na nuvem.


## Parte 4 — Salvar, recuperar e demonstrar

Na barra lateral, clique em **Baixar minhas viagens (JSON)** para guardar uma
cópia no computador. Para recuperar, selecione o arquivo e clique em
**Importar e substituir viagens**. Escolher o arquivo sozinho não altera dados.
Uma importação válida substitui a lista inteira; baixe seus cadastros antes se
quiser preservá-los. Um arquivo inválido mostra erro e mantém a lista anterior.
Um arquivo válido com lista vazia limpa a sessão.

O formato aceita UTF-8, até 2 MB, com `versao: 1` e uma lista `viagens`.
Cada viagem tem `destino`, `duracao`, `orcamento` e `despesas`; cada despesa tem
`descricao`, `categoria` e `valor`. Campos ausentes/desconhecidos, versão
incompatível, valores negativos, não finitos ou tipos incorretos são rejeitados.
O exemplo completo está em [dados/demonstracao.json](dados/demonstracao.json).

`exportar_json()` salva entradas, não os totais. `importar_json()` é um método
de classe (`@classmethod`): cria outro planejador, validando todos os objetos.
Só depois a interface substitui o planejador da sessão. Os resultados são
recalculados pelos métodos existentes. Não há salvamento automático no servidor.

Clique em **Carregar demonstração fictícia** para carregar Paraty e Petrópolis,
com os totais da tabela acima. O botão substitui a sessão. Todos os valores são
inventados para ensino; não representam pesquisas, ofertas ou cotações reais.
As sessões são independentes, e o JSON baixado é a cópia persistente do usuário.

Arquivos adicionais:

- `test_json.py`: testes da persistência, inclusive upload simulado e erros sem perda de dados.
- `dados/demonstracao.json`: dados fictícios, carregáveis na interface.

Sete testes automatizados passaram após implementar a Parte 4. Incluem
exportação/importação, UTF-8, arquivo vazio, versão incorreta, dados inválidos,
limite de tamanho e seleção após substituir viagens. Isso não comprova o ensaio
do aluno ou a inspeção visual de todas as funções.

## Publicação e entrega

O projeto está preparado para o Streamlit Community Cloud: entrada `app.py`,
Python 3.12 e dependências diretas fixadas em `requirements.txt` (Streamlit
1.67.0 e Plotly 7.2.0). O módulo `json` já faz parte do Python. Não há chaves
ou segredos necessários. Instale novamente `requirements.txt` ao atualizar.

Código publicado em [GitHub](https://github.com/duducoba/planejador-de-viagens).
Dados fictícios disponíveis em [demonstracao.json](https://github.com/duducoba/planejador-de-viagens/blob/main/dados/demonstracao.json).
Aplicativo publicado: [Planejador de viagens](https://planejador-de-viagens-duducoba.streamlit.app/).

Links do aplicativo, repositório e JSON bruto responderam HTTP 200 sem autenticação
em 26/11/2026. Na interface publicada, o agente carregou a demonstração,
conferiu tabela e gráficos e adicionou um passeio de R$ 100 a Paraty:
total R$ 1.250, saldo R$ 250 e média diária R$ 416,67. Ao selecionar
Petrópolis, conferiu total R$ 850, saldo R$ -50, média R$ 425 e o aviso.
A importação/exportação JSON foi verificada pelos testes locais; não se afirma
teste manual completo de upload/download na nuvem. Aprovação do professor,
envio ao Classroom e ensaio do aluno continuam pendentes.

"""Interface Streamlit. As regras e os cálculos ficam em modelos.py."""

import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

from modelos import Despesa, PlanejadorViagens, Viagem


def carregar_dados(conteudo):
    """Troca a sessão somente depois de validar o arquivo completo."""
    try:
        novo = PlanejadorViagens.importar_json(conteudo)
    except ValueError as erro:
        st.session_state.aviso_dados = ("error", f"Não foi possível importar: {erro} Seus cadastros foram mantidos.")
    else:
        st.session_state.planejador = novo
        # A nova lista pode ter menos viagens que a seleção anterior.
        st.session_state.pop("viagem_selecionada", None)
        st.session_state.aviso_dados = ("success", "Dados carregados. A lista anterior foi substituída.")


def importar_arquivo():
    """Callback do botão: o envio do arquivo sozinho não altera os dados."""
    arquivo = st.session_state.get("arquivo_json")
    if arquivo is None:
        st.session_state.aviso_dados = ("error", "Selecione um arquivo JSON primeiro.")
    else:
        carregar_dados(arquivo.getvalue())


def carregar_demonstracao():
    """Carrega somente os exemplos fictícios distribuídos com o projeto."""
    caminho = Path(__file__).parent / "dados" / "demonstracao.json"
    carregar_dados(caminho.read_bytes())


def mostrar_exportacao(planejador):
    """Gera o download após processar os cadastros desta execução."""
    st.sidebar.download_button(
        "Baixar minhas viagens (JSON)",
        data=planejador.exportar_json().encode("utf-8"),
        file_name="minhas_viagens.json", mime="application/json", key="exportar_json",
    )


def reais(valor):
    """Formata um número para exibição, sem alterar os cálculos."""
    return "R$ " + f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def grafico_barras(rotulos, valores, titulo, eixo_x):
    """Prepara a apresentação de valores já calculados pelas classes."""
    figura = go.Figure(go.Bar(
        x=rotulos,
        y=valores,
        text=[reais(valor) for valor in valores],
        textposition="auto",
        hovertemplate="%{x}<br>%{text}<extra></extra>",
    ))
    figura.update_layout(
        title=titulo,
        xaxis_title=eixo_x,
        yaxis_title="Valor (R$)",
        separators=",.",
    )
    figura.update_xaxes(type="category", categoryorder="array", categoryarray=rotulos)
    figura.update_yaxes(rangemode="tozero", tickprefix="R$ ", tickformat=",.2f")
    return figura


def main():
    st.set_page_config(page_title="Planejador de viagens", page_icon="🧳")
    st.title("Planejador de viagens")
    st.caption("Informe seus valores em reais e acompanhe o orçamento da viagem.")
    st.info("Baixe suas viagens em JSON para guardá-las. Recarregar ou fechar a aba pode encerrar a sessão.")

    # Só cria o planejador na primeira execução desta sessão.
    # Nas demais interações, recupera o mesmo objeto e suas viagens.
    if "planejador" not in st.session_state:
        st.session_state.planejador = PlanejadorViagens()
    planejador = st.session_state.planejador

    with st.sidebar:
        st.header("Salvar e carregar")
        st.caption("Importar ou carregar a demonstração substitui todas as viagens da sessão. Baixe uma cópia antes, se quiser mantê-las.")
        st.file_uploader("Arquivo de viagens (.json, até 2 MB)", type=["json"], max_upload_size=2, key="arquivo_json")
        st.button("Importar e substituir viagens", key="importar_json", on_click=importar_arquivo)
        st.button("Carregar demonstração fictícia", key="carregar_demo", on_click=carregar_demonstracao)
        st.caption("A demonstração usa preços inventados, sem pesquisa de mercado.")
        if "aviso_dados" in st.session_state:
            tipo, mensagem = st.session_state.pop("aviso_dados")
            if tipo == "error":
                st.error(mensagem)
            else:
                st.success(mensagem)

    st.header("Cadastrar viagem")
    with st.form("cadastro_viagem", clear_on_submit=True):
        destino = st.text_input("Destino")
        duracao = st.number_input("Duração (dias)", min_value=1, value=1, step=1)
        orcamento = st.number_input("Orçamento (R$)", min_value=0.0, step=50.0, format="%.2f")
        cadastrar = st.form_submit_button("Cadastrar viagem")

    if cadastrar:
        try:
            viagem = Viagem(destino, duracao, orcamento)
            planejador.adicionar_viagem(viagem)
        except (ValueError, TypeError) as erro:
            st.error(str(erro))
        else:
            # O seletor ainda não foi desenhado nesta execução.
            st.session_state.viagem_selecionada = len(planejador.viagens) - 1
            st.success("Viagem cadastrada!")

    if not planejador.viagens:
        mostrar_exportacao(planejador)
        st.info("Cadastre uma viagem para começar a adicionar despesas.")
        return

    st.header("Consultar viagem")
    indice = st.selectbox(
        "Selecione uma viagem",
        options=list(range(len(planejador.viagens))),
        format_func=lambda i: f"{i + 1}. {planejador.viagens[i].destino}",
        key="viagem_selecionada",
    )
    # O índice permite distinguir duas viagens com o mesmo destino.
    viagem = planejador.viagens[indice]
    st.write(f"Duração: {viagem.duracao} dias | Orçamento: {reais(viagem.orcamento)}")

    st.subheader("Adicionar despesa")
    # Um formulário por índice evita misturar campos entre viagens.
    with st.form(f"despesa_{indice}", clear_on_submit=True):
        descricao = st.text_input("Descrição")
        categoria = st.text_input("Categoria", placeholder="Ex.: Transporte, Hospedagem, Alimentação")
        valor = st.number_input("Valor total (R$)", min_value=0.0, step=10.0, format="%.2f")
        adicionar = st.form_submit_button("Adicionar despesa")

    if adicionar:
        try:
            despesa = Despesa(descricao, categoria, valor)
            viagem.adicionar_despesa(despesa)
        except (ValueError, TypeError) as erro:
            st.error(str(erro))
        else:
            st.success("Despesa adicionada!")

    # Exibe depois do formulário para refletir a despesa recém-adicionada.
    st.subheader("Resumo da viagem")
    total, saldo, media = st.columns(3)
    total.metric("Custo total", reais(viagem.custo_total()))
    saldo.metric("Saldo", reais(viagem.saldo()))
    media.metric("Custo médio diário", reais(viagem.custo_medio_diario()))
    if viagem.saldo() < 0:
        st.warning("Atenção: as despesas ultrapassaram o orçamento desta viagem.")

    st.subheader("Despesas cadastradas")
    if viagem.despesas:
        st.table([
            {"Descrição": despesa.descricao, "Categoria": despesa.categoria, "Valor": reais(despesa.valor)}
            for despesa in viagem.despesas
        ])
    else:
        st.info("Esta viagem ainda não tem despesas.")

    st.subheader("Gastos por categoria")
    categorias = viagem.gastos_por_categoria()
    if categorias:
        st.plotly_chart(grafico_barras(
            list(categorias), list(categorias.values()),
            f"Gastos de {indice + 1}. {viagem.destino}", "Categoria",
        ), key="grafico_categorias")
    else:
        st.info("Adicione despesas à viagem selecionada para ver o gráfico por categoria.")

    st.header("Comparação de viagens")
    st.caption("Ordenação pelo menor custo total. O número identifica o cadastro da viagem.")
    # A tabela e o gráfico usam a mesma comparação, calculada pelo planejador.
    comparacao = planejador.comparar_viagens()
    rotulos = [f"{resumo['numero']}. {resumo['destino']}" for resumo in comparacao]
    st.table([
        {
            "Viagem": rotulo,
            "Duração (dias)": resumo["duracao"],
            "Orçamento": reais(resumo["orcamento"]),
            "Custo total": reais(resumo["custo_total"]),
            "Saldo": reais(resumo["saldo"]),
            "Custo médio diário": reais(resumo["custo_medio_diario"]),
        }
        for rotulo, resumo in zip(rotulos, comparacao)
    ])
    st.plotly_chart(grafico_barras(
        rotulos, [resumo["custo_total"] for resumo in comparacao],
        "Custo total por viagem", "Viagem",
    ), key="grafico_viagens")
    mostrar_exportacao(planejador)


if __name__ == "__main__":
    main()

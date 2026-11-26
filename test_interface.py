"""Verifica o fluxo da interface sem abrir um navegador."""

import unittest
import json
from pathlib import Path

from streamlit.testing.v1 import AppTest
from modelos import Despesa, PlanejadorViagens, Viagem


class TestInterface(unittest.TestCase):
    def conferir_comparacao(self, tela):
        """Inspeciona os dados enviados ao Streamlit, incluindo o gráfico Plotly."""
        self.assertFalse(tela.exception)
        resumos = tela.session_state.planejador.comparar_viagens()
        tabela = tela.table[-1].value.to_dict("records")
        # O JSON aqui é apenas o formato interno do gráfico, não persistência do app.
        figura = json.loads(tela.get("plotly_chart")[-1].proto.spec)
        barras = figura["data"][0]
        for linha, resumo, rotulo, valor in zip(tabela, resumos, barras["x"], barras["y"]):
            esperado = f"{resumo['numero']}. {resumo['destino']}"
            self.assertEqual(linha["Viagem"], esperado)
            self.assertEqual(rotulo, esperado)
            self.assertEqual(linha["Duração (dias)"], resumo["duracao"])
            self.assertAlmostEqual(valor, resumo["custo_total"])
            for coluna, campo in [("Orçamento", "orcamento"), ("Custo total", "custo_total"),
                                  ("Saldo", "saldo"), ("Custo médio diário", "custo_medio_diario")]:
                exibido = float(linha[coluna].replace("R$ ", "").replace(".", "").replace(",", "."))
                self.assertAlmostEqual(exibido, round(resumo[campo], 2))
        self.assertEqual(len(tabela), len(resumos))
        self.assertEqual(len(barras["x"]), len(resumos))
        self.assertEqual(len(barras["y"]), len(resumos))

    def test_comparacao_e_categorias(self):
        tela = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run()
        self.assertEqual(len(tela.get("plotly_chart")), 0)
        planejador = PlanejadorViagens()
        primeira = Viagem("Paraty", 3, 100)
        primeira.adicionar_despesa(Despesa("Almoço", "Alimentação", 80.25))
        primeira.adicionar_despesa(Despesa("Jantar", "Alimentação", 40.50))
        primeira.adicionar_despesa(Despesa("Ônibus", "Transporte", 30))
        segunda = Viagem("Paraty", 2, 500)
        terceira = Viagem("Recife", 1, 0)
        terceira.adicionar_despesa(Despesa("Passeio gratuito", "Passeios", 0))
        for viagem in [primeira, segunda, terceira]:
            planejador.adicionar_viagem(viagem)
        tela.session_state.planejador = planejador
        tela.run()
        self.conferir_comparacao(tela)
        self.assertEqual(tela.table[-1].value["Viagem"].tolist(), ["2. Paraty", "3. Recife", "1. Paraty"])
        figura = json.loads(tela.get("plotly_chart")[0].proto.spec)
        self.assertEqual(dict(zip(figura["data"][0]["x"], figura["data"][0]["y"])),
                         primeira.gastos_por_categoria())
        self.assertEqual(len(tela.warning), 1)

        tela.selectbox[0].set_value(1).run()
        self.assertEqual(len(tela.get("plotly_chart")), 1)
        self.assertTrue(any("Adicione despesas" in aviso.value for aviso in tela.info))
        self.conferir_comparacao(tela)
        tela.text_input[1].set_value("Hotel")
        tela.text_input[2].set_value("Hospedagem")
        tela.number_input[2].set_value(200.0)
        tela.button[1].click().run()
        self.conferir_comparacao(tela)
        figura = json.loads(tela.get("plotly_chart")[0].proto.spec)
        self.assertEqual(figura["data"][0]["x"], ["Hospedagem"])
        self.assertEqual(figura["data"][0]["y"], [200.0])
        self.assertEqual(tela.table[-1].value["Viagem"].tolist(), ["3. Recife", "1. Paraty", "2. Paraty"])

        tela.selectbox[0].set_value(2).run()
        figura = json.loads(tela.get("plotly_chart")[0].proto.spec)
        self.assertEqual(figura["data"][0]["x"], ["Passeios"])
        self.assertEqual(figura["data"][0]["y"], [0.0])
        tela.run()
        self.conferir_comparacao(tela)
        self.assertEqual(len(tela.session_state.planejador.viagens), 3)

    def test_cadastro_despesas_e_sessao(self):
        tela = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run()
        self.assertFalse(tela.exception)
        self.assertEqual(len(tela.selectbox), 0)

        # Destino vazio deve mostrar erro e não criar cadastro.
        tela.button[0].click().run()
        self.assertEqual(len(tela.error), 1)
        self.assertEqual(len(tela.session_state.planejador.viagens), 0)

        tela.text_input[0].set_value("Paraty")
        tela.number_input[0].set_value(2)
        tela.number_input[1].set_value(100.0)
        tela.button[0].click().run()
        self.assertEqual(tela.metric[0].value, "R$ 0,00")
        self.conferir_comparacao(tela)

        # Descrição vazia deve ser rejeitada pela classe Despesa.
        tela.button[1].click().run()
        self.assertEqual(len(tela.error), 1)
        self.assertEqual(len(tela.session_state.planejador.viagens[0].despesas), 0)

        tela.text_input[1].set_value("Pousada")
        tela.text_input[2].set_value("Hospedagem")
        tela.number_input[2].set_value(150.0)
        tela.button[1].click().run()
        self.assertEqual([item.value for item in tela.metric],
                         ["R$ 150,00", "R$ -50,00", "R$ 75,00"])
        self.assertEqual(len(tela.warning), 1)
        self.assertEqual(tela.table[0].value.iloc[0]["Descrição"], "Pousada")
        self.conferir_comparacao(tela)

        # Mesmo destino, mas outro objeto Viagem e outra lista de despesas.
        tela.text_input[0].set_value("Paraty")
        tela.button[0].click().run()
        self.assertEqual(tela.selectbox[0].value, 1)
        self.assertEqual(tela.metric[0].value, "R$ 0,00")
        self.assertEqual(len(tela.warning), 0)
        tela.selectbox[0].set_value(0).run()
        self.assertEqual(tela.metric[0].value, "R$ 150,00")

        # Reexecutar não apaga cadastros nem duplica a última despesa.
        tela.run()
        self.assertEqual(len(tela.session_state.planejador.viagens), 2)
        self.assertEqual(len(tela.session_state.planejador.viagens[0].despesas), 1)
        self.assertFalse(tela.exception)

        outra_sessao = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run()
        self.assertEqual(len(outra_sessao.session_state.planejador.viagens), 0)


if __name__ == "__main__":
    unittest.main()

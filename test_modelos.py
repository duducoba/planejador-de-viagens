"""Testes dos cálculos usados na comparação e nos gráficos."""

import unittest

from modelos import Despesa, PlanejadorViagens, Viagem


class TestModelos(unittest.TestCase):
    def test_categorias(self):
        viagem = Viagem("Paraty", 3, 500)
        self.assertEqual(viagem.gastos_por_categoria(), {})
        viagem.adicionar_despesa(Despesa("Almoço", "Alimentação", 20.25))
        viagem.adicionar_despesa(Despesa("Jantar", "Alimentação", 30.50))
        viagem.adicionar_despesa(Despesa("Café", "alimentação", 10))
        viagem.adicionar_despesa(Despesa("Passeio", "Passeios", 0))
        self.assertEqual(viagem.gastos_por_categoria(),
                         {"Alimentação": 50.75, "alimentação": 10, "Passeios": 0})
        self.assertAlmostEqual(sum(viagem.gastos_por_categoria().values()), viagem.custo_total())

    def test_numeros_e_ordenacao(self):
        planejador = PlanejadorViagens()
        self.assertEqual(planejador.comparar_viagens(), [])
        primeira = Viagem("Paraty", 2, 50)
        primeira.adicionar_despesa(Despesa("Hotel", "Hospedagem", 100))
        segunda = Viagem("Paraty", 1, 200)
        planejador.adicionar_viagem(primeira)
        planejador.adicionar_viagem(segunda)
        resumos = planejador.comparar_viagens()
        self.assertEqual([item["numero"] for item in resumos], [2, 1])
        self.assertEqual(resumos[1]["saldo"], -50)
        self.assertEqual(resumos[1]["custo_medio_diario"], 50)
        self.assertEqual(planejador.viagens, [primeira, segunda])
        segunda.adicionar_despesa(Despesa("Hotel", "Hospedagem", 300))
        self.assertEqual([item["numero"] for item in planejador.comparar_viagens()], [1, 2])


if __name__ == "__main__":
    unittest.main()

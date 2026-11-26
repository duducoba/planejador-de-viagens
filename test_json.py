"""Persistência e proteção dos cadastros durante importações inválidas."""

import json
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest
from modelos import PlanejadorViagens

DEMO = Path(__file__).parent / "dados" / "demonstracao.json"


class TestJSON(unittest.TestCase):
    def test_ida_e_volta(self):
        original = PlanejadorViagens.importar_json(DEMO.read_bytes())
        recuperado = PlanejadorViagens.importar_json(original.exportar_json())
        self.assertEqual(original.comparar_viagens(), recuperado.comparar_viagens())
        self.assertEqual(json.loads(original.exportar_json()), json.loads(recuperado.exportar_json()))
        self.assertEqual(recuperado.viagens[0].custo_total(), 1150)
        self.assertEqual(recuperado.viagens[1].saldo(), -50)
        self.assertEqual(PlanejadorViagens.importar_json('{"versao":1,"viagens":[]}').viagens, [])
        self.assertEqual(PlanejadorViagens.importar_json(b'\xef\xbb\xbf' + DEMO.read_bytes()).viagens[1].destino, "Petrópolis")

    def test_arquivos_invalidos(self):
        invalido = json.loads(DEMO.read_text(encoding="utf-8"))
        invalido["viagens"][1]["despesas"][0]["valor"] = -1
        exemplos = [b'\xff', "{", "[]", "null", '{"versao":2,"viagens":[]}',
                    '{"versao":true,"viagens":[]}', '{"versao":1,"viagens":{}}',
                    json.dumps(invalido), " " * (2 * 1024 * 1024 + 1)]
        for campo, valor in [("duracao", 0), ("duracao", True), ("duracao", 1.5),
                             ("orcamento", "100"), ("orcamento", float("nan")),
                             ("orcamento", float("inf")), ("destino", ""), ("despesas", {})]:
            dados = json.loads(DEMO.read_text(encoding="utf-8"))
            dados["viagens"][0][campo] = valor
            exemplos.append(json.dumps(dados))
        exemplos.append('{"versao":1,"viagens":[{"destino":"Paraty"}]}')
        for conteudo in exemplos:
            with self.subTest(conteudo=str(conteudo)[:80]):
                with self.assertRaises(ValueError):
                    PlanejadorViagens.importar_json(conteudo)

    def test_importacao_na_tela(self):
        tela = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run()
        tela.button(key="importar_json").click().run()
        self.assertTrue(any("Selecione um arquivo" in e.value for e in tela.error))
        tela.button(key="carregar_demo").click().run()
        self.assertFalse(tela.exception)
        self.assertEqual(len(tela.session_state.planejador.viagens), 2)
        tela.selectbox[0].set_value(1).run()
        antes = tela.session_state.planejador.exportar_json()

        # Uma viagem válida seguida de uma inválida não pode causar importação parcial.
        dados = json.loads(antes)
        dados["viagens"][1]["duracao"] = 0
        tela.file_uploader[0].set_value(("invalido.json", json.dumps(dados).encode(), "application/json")).run()
        tela.button(key="importar_json").click().run()
        self.assertFalse(tela.exception)
        self.assertTrue(any("cadastros foram mantidos" in e.value for e in tela.error))
        self.assertEqual(tela.session_state.planejador.exportar_json(), antes)
        self.assertEqual(tela.selectbox[0].value, 1)

        # Substituir duas viagens por uma reajusta a seleção.
        dados = json.loads(antes)
        dados["viagens"] = dados["viagens"][:1]
        tela.file_uploader[0].set_value(("valido.json", json.dumps(dados).encode(), "application/json")).run()
        self.assertEqual(len(tela.session_state.planejador.viagens), 2)  # só escolher não importa
        tela.button(key="importar_json").click().run()
        self.assertFalse(tela.exception)
        self.assertEqual(tela.selectbox[0].value, 0)
        self.assertEqual(len(tela.session_state.planejador.viagens), 1)
        self.assertEqual(tela.metric[0].value, "R$ 1.150,00")
        tela.run()
        self.assertEqual(len(tela.session_state.planejador.viagens), 1)

        tela.file_uploader[0].set_value(("vazio.json", b'{"versao":1,"viagens":[]}', "application/json")).run()
        tela.button(key="importar_json").click().run()
        self.assertFalse(tela.exception)
        self.assertEqual(len(tela.selectbox), 0)
        self.assertEqual(len(tela.get("download_button")), 1)


if __name__ == "__main__":
    unittest.main()

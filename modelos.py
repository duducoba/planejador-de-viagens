"""Classes do planejador de viagens, independentes de qualquer interface."""

from math import isfinite
import json


def validar_texto(texto, nome):
    """Remove espaços das pontas e rejeita textos vazios."""
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(f"{nome} deve ser um texto não vazio.")
    return texto.strip()


def validar_valor(valor, nome):
    """Aceita números finitos e não negativos, expressos em reais."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{nome} deve ser um número.")
    if not isfinite(valor) or valor < 0:
        raise ValueError(f"{nome} deve ser finito e maior ou igual a zero.")
    return float(valor)


class Despesa:
    """Um gasto com descrição, categoria livre e valor total em reais."""

    def __init__(self, descricao, categoria, valor):
        self.descricao = validar_texto(descricao, "Descrição")
        self.categoria = validar_texto(categoria, "Categoria")
        self.valor = validar_valor(valor, "Valor da despesa")


class Viagem:
    """Uma viagem e as despesas usadas para calcular seus custos."""

    def __init__(self, destino, duracao, orcamento):
        self.destino = validar_texto(destino, "Destino")
        if isinstance(duracao, bool) or not isinstance(duracao, int) or duracao <= 0:
            raise ValueError("Duração deve ser um número inteiro de dias maior que zero.")
        self.duracao = duracao
        self.orcamento = validar_valor(orcamento, "Orçamento")
        # Cada viagem começa com sua própria lista de despesas.
        self.despesas = []

    def adicionar_despesa(self, despesa):
        """Inclui um objeto Despesa nesta viagem."""
        if not isinstance(despesa, Despesa):
            raise TypeError("A despesa deve ser um objeto da classe Despesa.")
        self.despesas.append(despesa)

    def custo_total(self):
        """Soma os valores de todas as despesas; sem despesas, retorna zero."""
        return sum(despesa.valor for despesa in self.despesas)

    def saldo(self):
        """Retorna o orçamento restante; negativo significa orçamento excedido."""
        return self.orcamento - self.custo_total()

    def custo_medio_diario(self):
        """Divide o custo total pelo número de dias da viagem."""
        return self.custo_total() / self.duracao

    def gastos_por_categoria(self):
        """Soma despesas de mesma categoria, preservando a grafia cadastrada."""
        totais = {}
        for despesa in self.despesas:
            totais[despesa.categoria] = totais.get(despesa.categoria, 0) + despesa.valor
        return totais


class PlanejadorViagens:
    """Reúne viagens, busca destinos e compara os custos cadastrados."""

    def __init__(self):
        self.viagens = []

    def adicionar_viagem(self, viagem):
        """Inclui um objeto Viagem no planejador."""
        if not isinstance(viagem, Viagem):
            raise TypeError("A viagem deve ser um objeto da classe Viagem.")
        self.viagens.append(viagem)

    def exportar_json(self):
        """Exporta apenas dados de entrada; os resultados serão recalculados."""
        dados = {"versao": 1, "viagens": []}
        for viagem in self.viagens:
            dados["viagens"].append({
                "destino": viagem.destino,
                "duracao": viagem.duracao,
                "orcamento": viagem.orcamento,
                "despesas": [
                    {"descricao": d.descricao, "categoria": d.categoria, "valor": d.valor}
                    for d in viagem.despesas
                ],
            })
        return json.dumps(dados, ensure_ascii=False, indent=2, allow_nan=False)

    @classmethod
    def importar_json(cls, conteudo):
        """Constrói um NOVO planejador. Um erro nunca altera o planejador atual.

        Aceita texto ou bytes UTF-8, até 2 MB, no formato exportado pelo app.
        Os construtores existentes validam os valores de cada objeto.
        """
        try:
            if isinstance(conteudo, bytes):
                if len(conteudo) > 2 * 1024 * 1024:
                    raise ValueError("O arquivo deve ter no máximo 2 MB.")
                conteudo = conteudo.decode("utf-8-sig")
            if not isinstance(conteudo, str):
                raise ValueError("Selecione um arquivo JSON em UTF-8.")
            if len(conteudo.encode("utf-8")) > 2 * 1024 * 1024:
                raise ValueError("O arquivo deve ter no máximo 2 MB.")
            dados = json.loads(conteudo)
            cls._conferir_campos(dados, {"versao", "viagens"}, "Arquivo")
            if type(dados["versao"]) is not int or dados["versao"] != 1:
                raise ValueError("Versão do arquivo não suportada; use a versão 1.")
            if not isinstance(dados["viagens"], list):
                raise ValueError("O campo viagens deve ser uma lista.")
            novo = cls()
            for numero, item in enumerate(dados["viagens"], start=1):
                cls._conferir_campos(item, {"destino", "duracao", "orcamento", "despesas"}, f"Viagem {numero}")
                viagem = Viagem(item["destino"], item["duracao"], item["orcamento"])
                if not isinstance(item["despesas"], list):
                    raise ValueError(f"As despesas da viagem {numero} devem ser uma lista.")
                for gasto in item["despesas"]:
                    cls._conferir_campos(gasto, {"descricao", "categoria", "valor"}, "Despesa")
                    viagem.adicionar_despesa(Despesa(gasto["descricao"], gasto["categoria"], gasto["valor"]))
                # Também rejeita somas que excedam os limites numéricos do Python.
                if not isfinite(viagem.custo_total()):
                    raise ValueError("O custo total da viagem excede o limite numérico.")
                novo.adicionar_viagem(viagem)
            return novo
        except (UnicodeError, json.JSONDecodeError, RecursionError, OverflowError) as erro:
            raise ValueError("Arquivo inválido: use JSON em UTF-8 com valores numéricos válidos.") from erro

    @staticmethod
    def _conferir_campos(item, campos, nome):
        """Rejeita estruturas incompletas ou diferentes do formato esperado."""
        if not isinstance(item, dict) or set(item) != campos:
            raise ValueError(f"{nome}: campos esperados: {', '.join(sorted(campos))}.")

    def encontrar_viagens(self, destino):
        """Busca o destino completo, ignorando maiúsculas e espaços nas pontas.

        Retorna uma lista: pode haver várias viagens para o mesmo destino.
        Se não houver correspondências, retorna uma lista vazia.
        """
        destino = validar_texto(destino, "Destino da busca")
        return [
            viagem for viagem in self.viagens
            if viagem.destino.casefold() == destino.casefold()
        ]

    def comparar_viagens(self):
        """Retorna resumos por custo total crescente, sem alterar o cadastro."""
        resumos = []
        for numero, viagem in enumerate(self.viagens, start=1):
            resumos.append({
                # Número do cadastro: não muda quando os resumos são ordenados.
                "numero": numero,
                "destino": viagem.destino,
                "duracao": viagem.duracao,
                "orcamento": viagem.orcamento,
                "custo_total": viagem.custo_total(),
                "saldo": viagem.saldo(),
                "custo_medio_diario": viagem.custo_medio_diario(),
            })
        return sorted(resumos, key=lambda resumo: resumo["custo_total"])

"""Exemplo executável e verificações simples do núcleo do planejador."""

from math import isclose

from modelos import Despesa, PlanejadorViagens, Viagem


def main():
    planejador = PlanejadorViagens()

    paraty = Viagem("Paraty", 3, 1500)
    paraty.adicionar_despesa(Despesa("Ônibus ida e volta", "Transporte", 300))
    paraty.adicionar_despesa(Despesa("Pousada", "Hospedagem", 600))
    paraty.adicionar_despesa(Despesa("Refeições", "Alimentação", 250))

    petropolis = Viagem("Petrópolis", 2, 800)
    petropolis.adicionar_despesa(Despesa("Ônibus ida e volta", "Transporte", 150))
    petropolis.adicionar_despesa(Despesa("Hotel", "Hospedagem", 500))
    petropolis.adicionar_despesa(Despesa("Refeições", "Alimentação", 200))

    planejador.adicionar_viagem(paraty)
    planejador.adicionar_viagem(petropolis)

    # assert interrompe o exemplo se uma condição não for verdadeira.
    assert isclose(paraty.custo_total(), 1150)
    assert isclose(paraty.saldo(), 350)
    assert isclose(paraty.custo_medio_diario(), 1150 / 3)
    assert isclose(petropolis.custo_total(), 850)
    assert isclose(petropolis.saldo(), -50)
    assert isclose(petropolis.custo_medio_diario(), 425)
    assert planejador.encontrar_viagens(" PARATY ") == [paraty]
    assert planejador.encontrar_viagens("Recife") == []

    comparacao = planejador.comparar_viagens()
    assert [resumo["destino"] for resumo in comparacao] == ["Petrópolis", "Paraty"]

    print("Comparação por custo total (do menor para o maior):")
    for resumo in comparacao:
        print(f"\n{resumo['destino']} — {resumo['duracao']} dias")
        print(f"  Orçamento: R$ {resumo['orcamento']:.2f}")
        print(f"  Custo total: R$ {resumo['custo_total']:.2f}")
        print(f"  Saldo: R$ {resumo['saldo']:.2f}")
        print(f"  Custo médio diário: R$ {resumo['custo_medio_diario']:.2f}")

    # Uma viagem sem despesas tem custo zero e mantém todo o orçamento.
    vazia = Viagem("Recife", 1, 100)
    assert vazia.custo_total() == 0
    assert vazia.saldo() == 100
    assert vazia.custo_medio_diario() == 0

    print("\nVerificação de entradas inválidas:")
    try:
        Viagem("Destino inválido", 0, 100)
    except ValueError as erro:
        print(f"  Duração zero rejeitada: {erro}")
    else:
        raise AssertionError("Duração zero deveria ser rejeitada.")

    try:
        Despesa("Gasto inválido", "Transporte", -10)
    except ValueError as erro:
        print(f"  Despesa negativa rejeitada: {erro}")
    else:
        raise AssertionError("Despesa negativa deveria ser rejeitada.")

    print("\nTodas as verificações passaram.")


if __name__ == "__main__":
    main()

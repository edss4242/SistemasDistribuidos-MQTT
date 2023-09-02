import random

# Definindo constantes e estruturas de dados
NUM_FABRICAS = 2
FABRICA_1_LINHAS = 5
FABRICA_2_LINHAS = 8
NUM_VERSOES = 5
NUM_PARTES = 100

# Definindo estoque mínimo e máximo para produtos acabados
ESTOQUE_VERMELHO_PRODUTOS = 500
ESTOQUE_AMARELO_PRODUTOS = 1000

# Definindo estoque mínimo e máximo para partes
ESTOQUE_VERMELHO_PARTES = 5000
ESTOQUE_AMARELO_PARTES = 8000

# Inicialização do estoque de produtos (iniciando em zero apenas no primeiro dia)
estoque_produtos = {versao: 0 for versao in range(1, NUM_VERSOES + 1)}
estoque_partes = {parte: 10000 for parte in range(1, NUM_PARTES + 1)}

composicao_partes = {}
partes_base = set(random.sample(range(1, NUM_PARTES + 1), 43))  # Partes do kit base
partes_restantes = list(set(range(1, NUM_PARTES + 1)) - partes_base)
for versao in range(1, NUM_VERSOES + 1):
    partes_variacao = set(random.sample(partes_restantes, random.randint(20, 33)))  # Partes do kit de variação
    composicao_partes[versao] = {'base': partes_base, 'variacao': partes_variacao}
    print(composicao_partes[versao])

# Simulação de pedidos diários aleatórios
def gerar_pedidos_diarios():
    pedidos = {versao: random.randint(1, 1000) for versao in range(1, NUM_VERSOES + 1)}
    return pedidos

# Cálculo da produção diária para a Fábrica 1 (Fabricação Empurrada)
def calcular_producao_fabrica1():
    producao_fabrica1 = {versao: FABRICA_1_LINHAS * 48 for versao in range(1, NUM_VERSOES + 1)}
    return producao_fabrica1

# Cálculo da produção diária para a Fábrica 2 (Fabricação Puxada)
def calcular_producao_fabrica2(pedidos):
    producao_fabrica2 = {versao: 0 for versao in range(1, NUM_VERSOES + 1)}

    for versao in range(1, NUM_VERSOES + 1):
        estoque_atual = estoque_produtos[versao]
        pedidos_versao = pedidos.get(versao, 0)  # Verifica se há pedidos para a versão

        # Defina os níveis de estoque amarelo e vermelho para o produto atual
        nivel_amarelo_produtos = ESTOQUE_AMARELO_PRODUTOS
        nivel_vermelho_produtos = ESTOQUE_VERMELHO_PRODUTOS

        # Verifique se o estoque está abaixo do nível vermelho
        if estoque_atual < nivel_vermelho_produtos:
            # Produzir em dobro para atender à demanda
            quantidade_produzir = max(pedidos_versao + nivel_amarelo_produtos - estoque_atual, FABRICA_2_LINHAS) * 2
        elif estoque_atual < nivel_amarelo_produtos:
            # Produzir o suficiente para atender aos pedidos
            quantidade_produzir = max(pedidos_versao + nivel_amarelo_produtos - estoque_atual, FABRICA_2_LINHAS)
        else:
            # Não é necessário produzir
            quantidade_produzir = 0

        producao_fabrica2[versao] = quantidade_produzir

    return producao_fabrica2

# Função para retirar os produtos pedidos do estoque
def retirar_pedidos_do_estoque(pedidos):
    for versao, quantidade_pedida in pedidos.items():
        estoque_atual = estoque_produtos[versao]
        estoque_produtos[versao] = max(estoque_atual - quantidade_pedida, 0)

# Função para verificar e atualizar o estoque de partes com base nos níveis amarelo e vermelho
def verificar_atualizar_estoque_partes():
    for parte, estoque in estoque_partes.items():
        # Defina os níveis de estoque amarelo e vermelho para as partes
        nivel_amarelo_partes = ESTOQUE_AMARELO_PARTES
        nivel_vermelho_partes = ESTOQUE_VERMELHO_PARTES

        # Verifique se o estoque está abaixo do nível vermelho
        if estoque < nivel_vermelho_partes:
            # Adicionar mais 200000 partes
            estoque_partes[parte] += 15000
        elif estoque < nivel_amarelo_partes:
            # Adicionar mais 100000 partes
            estoque_partes[parte] += 7500
        elif estoque<0:
            print("PANE, FALTA DE PECA!!!!!!!!!!!!!!")

# Consumo de partes e kits
def calcular_consumo_partes(pedidos, producao_fabrica2):
    consumo_partes = {parte: 0 for parte in range(1, NUM_PARTES + 1)}

    for versao in range(1, NUM_VERSOES + 1):
        producao_total = 48*NUM_VERSOES + producao_fabrica2.get(versao, 0)
        partes_base = composicao_partes[versao]['base']
        partes_variacao = composicao_partes[versao]['variacao']

        for parte in partes_base:
            consumo_partes[parte] += producao_total
        for parte in partes_variacao:
            consumo_partes[parte] += producao_total

        # Subtrai as peças usadas para produzir os produtos
        for parte_usada in partes_base:
            estoque_partes[parte_usada] -= producao_total

    verificar_atualizar_estoque_partes()
    return consumo_partes

# Monitoramento de estoque de partes
def monitorar_estoque_partes(consumo_partes):
    for parte, consumo in consumo_partes.items():
        estoque_partes[parte] -= consumo

# Função para atualizar o estoque de produtos diariamente
def atualizar_estoque_produtos_diariamente(producao_fabrica1, producao_fabrica2):
    for versao in range(1, NUM_VERSOES + 1):
        estoque_atual = estoque_produtos[versao]
        producao_total = producao_fabrica1.get(versao, 0) + producao_fabrica2.get(versao, 0)
        estoque_produtos[versao] += producao_total
def executar_simulacao_dia():
    print('Estoque de partes antes do consumo:')
    print(estoque_partes)
    print('Estoque no começo do dia:')
    print(estoque_produtos)
    pedidos = gerar_pedidos_diarios()
    print('Pedidos:')
    print(pedidos)
    producao_fabrica1 = calcular_producao_fabrica1()
    print('Produção da Fábrica 1:')
    print(producao_fabrica1)
    producao_fabrica2 = calcular_producao_fabrica2(pedidos)
    producao_fabrica2 = calcular_producao_fabrica2(pedidos)
    print('Produção da Fábrica 2:')
    print(producao_fabrica2)
    atualizar_estoque_produtos_diariamente(producao_fabrica1, producao_fabrica2)
    print('Estoque após producao:')
    print(estoque_produtos)
    retirar_pedidos_do_estoque(pedidos)
    print('Estoque após retirar os pedidos:')
    print(estoque_produtos)
    consumo_partes = calcular_consumo_partes(pedidos, producao_fabrica2)
    monitorar_estoque_partes(consumo_partes)
    print('Estoque de partes após consumo:')
    print(estoque_partes)
# Execução da simulação por vários dias
NUM_DIAS_SIMULACAO = 30

for dia in range(1, NUM_DIAS_SIMULACAO + 1):
    print(f"--------- Dia {dia} -----------------------------------------------------------------")
    executar_simulacao_dia()

print("Simulação concluída.")
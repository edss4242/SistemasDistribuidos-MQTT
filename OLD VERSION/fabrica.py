import paho.mqtt.client as mqtt
import random
import time
import json

# Configurações MQTT
MQTT_BROKER_HOST = "localhost"  # Endereço do HiveMQ (ou IP da máquina que está executando o HiveMQ)
MQTT_BROKER_PORT = 1883
TOPIC_RESPOSTA_REABASTECIMENTO = "resposta/reabastecimento"

# Função para simular a produção
def produzir_produto(client, produto, quantidade):
    print(f"Produzindo {quantidade} unidades do produto {produto}")
    time.sleep(random.randint(5, 10))
    print(f"{quantidade} unidades do produto {produto} produzidas com sucesso!")

# Função para processar as respostas de reabastecimento
def processar_resposta_reabastecimento(client, userdata, message):
    resposta = message.payload.decode("utf-8")
    print(f"Resposta de reabastecimento recebida: {resposta}")
    produto, quantidade = resposta.split(":")[-1].strip().split()
    produzir_produto(client, produto, int(quantidade))

#monta um json com nome = fabrica 1 e todos os produtos (1 a 5) = 48
def geraProducao():
    data_pedido = {
        "nome": "fabrica1"
    }
    for i in range(1, 6):
        nome_produto = f"produto{i}"
        data_pedido[nome_produto] = 48
        print(f'pedido gerado para {nome_produto}, qnt: {data_pedido[nome_produto]}')
    
    json_data = json.dumps(data_pedido, indent=2)
    return json_data

# Configuração do cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

# Inscreve-se no tópico de respostas de reabastecimento
client.subscribe(TOPIC_RESPOSTA_REABASTECIMENTO)
client.message_callback_add(TOPIC_RESPOSTA_REABASTECIMENTO, processar_resposta_reabastecimento)

# Mantém o cliente MQTT em execução
client.loop_forever()
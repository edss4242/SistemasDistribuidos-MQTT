import paho.mqtt.client as mqtt
import random
import time

# Configurações MQTT
MQTT_BROKER_HOST = "localhost"  # Endereço do HiveMQ (ou IP da máquina que está executando o HiveMQ)
MQTT_BROKER_PORT = 1883
TOPIC_PEDIDO_REABASTECIMENTO = "pedido/reabastecimento"

# Função para enviar pedidos de reabastecimento
def enviar_pedido_reabastecimento(produto, quantidade):
    client = mqtt.Client()
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    mensagem = f"{produto} {quantidade}"
    client.publish(TOPIC_PEDIDO_REABASTECIMENTO, mensagem)
    client.disconnect()

# Simulação do fornecedor enviando pedidos de reabastecimento aleatórios
if __name__ == "__main__":
    while True:
        # Simula o fornecedor enviando pedidos de reabastecimento aleatórios
        produto = random.choice(["Pv1", "Pv2", "Pv3", "Pv4", "Pv5"])
        quantidade = random.randint(10, 30)
        enviar_pedido_reabastecimento(produto, quantidade)
        time.sleep(random.randint(5, 10))
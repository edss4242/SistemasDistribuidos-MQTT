import paho.mqtt.client as mqtt
import random
import time
import json

# Configurações MQTT
MQTT_BROKER_HOST = "localhost"  # Endereço do HiveMQ (ou IP da máquina que está executando o HiveMQ)
MQTT_BROKER_PORT = 1883
TOPIC_PEDIDO_REABASTECIMENTO = "pedido/reabastecimento"


#apenas para teste
json_data = '''
{
  "nome": "almoxarifado",
  "produto1": 15,
  "produto2": 7,
  "produto3": 0,
  "produto4": 0,
  "produto5": 2
}
'''

# Função para enviar pedidos de reabastecimento recebe um json com os dados
def enviar_pedido_reabastecimento(json_data):
    #client = mqtt.Client()
    #client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    #mensagem = f"{produto} {quantidade}"
    data = json.loads(json_data)
    nome = data["nome"]
    print(f'pedido recebido de: {nome}')
    data["nome"] = "fornecedor"
    json_str = json.dumps(data, indent=2)
    #criar funçao que envia esse json_str
    return json_str

    #client.publish(TOPIC_PEDIDO_REABASTECIMENTO, mensagem)
    #client.disconnect()


# Simulação do fornecedor enviando pedidos de reabastecimento aleatórios
#if __name__ == "__main__":
    #while True:
        # Simula o fornecedor enviando pedidos de reabastecimento aleatórios
        #produto = random.choice(["Pv1", "Pv2", "Pv3", "Pv4", "Pv5"])
        #quantidade = random.randint(10, 30)
        #enviar_pedido_reabastecimento(produto, quantidade)
        #time.sleep(random.randint(5, 10))
def main():
    
    newjson = json_data
    newjson = enviar_pedido_reabastecimento(newjson) 
    print(newjson)

if __name__ == "__main__":
    main()
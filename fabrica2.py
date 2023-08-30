import paho.mqtt.client as mqtt
import random
import time
import json

#apenas para teste
json_data_deposito = '''
{
  "nome": "deposito",
  "produto1": 15,
  "produto2": 17,
  "produto3": 50,
  "produto4": 1,
  "produto5": 12
}
'''


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

def verifica_estoque():
    data_deposito = json.loads(json_data_deposito)
    nome = data_deposito["nome"]
    print(f'Estoque recebido de: {nome}')
    estoque = [0] * 5 

    #le estoque
    for i in range(1, 6):
        nome_produto = f"produto{i}"
        valor = data_deposito.get(nome_produto, 0)
        estoque[i - 1] = valor

    return estoque

def qnt_producao(estoque,json_data_pedido):
    data_pedido = json.loads(json_data_pedido)
    data_deposito = json.loads(json_data_deposito)
    nome = data_pedido["nome"]
    print(f'{nome} recebido inicio produção')
    
    for i in range(1, 6):
        nome_produto = f"produto{i}"
        valor = data_pedido.get(nome_produto, 0)
        #print(f'{valor}-->{estoque[i-1]}')
        #envia json para estoque
        if(estoque[i-1] > valor):
            nome_produto = f"produto{i}"
            data_pedido[nome_produto] = 0
            data_deposito[nome_produto] = estoque[i-1] - valor


        #envia json para produção
        else:
            nome_produto = f"produto{i}"
            data_deposito[nome_produto] = 0
            data_pedido[nome_produto] = valor - estoque[i-1]
    
    data_deposito["nome"] = "fabrica2"
    json_data_Pmodificado = json.dumps(data_pedido, indent=2)
    json_data_Emodificado = json.dumps(data_deposito, indent=2)
    print(json_data_Pmodificado)
    print(json_data_Emodificado)

def geraPedido():
    data_pedido = {
        "nome": "pedido"
    }
    for i in range(1, 6):
        nome_produto = f"produto{i}"
        data_pedido[nome_produto] = random.randint(1, 100)
        print(f'pedido gerado para {nome_produto}, qnt: {data_pedido[nome_produto]}')
    
    json_data = json.dumps(data_pedido, indent=2)
    return json_data

# Chamar a função para gerar o JSON de pedido
json_pedido = geraPedido()

print(json_pedido)
            

def main():

    json_data_pedido = geraPedido()
    produtos = verifica_estoque()
    qnt_producao(produtos,json_data_pedido)
    

if __name__ == "__main__":
    main()



# Configuração do cliente MQTT
#client = mqtt.Client()
#client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

# Inscreve-se no tópico de respostas de reabastecimento
#client.subscribe(TOPIC_RESPOSTA_REABASTECIMENTO)
#client.message_callback_add(TOPIC_RESPOSTA_REABASTECIMENTO, processar_resposta_reabastecimento)

# Mantém o cliente MQTT em execução
#client.loop_forever()

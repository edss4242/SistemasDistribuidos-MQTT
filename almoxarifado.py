import paho.mqtt.client as mqtt
import json

#constantes
Red_value = 90
Yellow_value = 95

#apenas para teste
json_data = '''
{
  "linha": "nome_da_linha",
  "peça1": 5,
  "peça2": 7,
  "peça3": 0,
  "peça4": 0,
  "peça5": 0
}
'''

# Configurações MQTT
MQTT_BROKER_HOST = "hivemq_broker_container"
MQTT_BROKER_PORT = 1883
TOPIC_CONSUMO_PARTES = "consumo/partes"

def envia_produto1(p,qnt):
    #kit basico
    for i in range(0, 43):
        p[i] -= qnt
        
    #kit variação
    for i in range(43, 63):
        p[i] -= qnt
    #envio das peças
    #envia_peca()

def envia_produto2(p,qnt):
    #kit basico
    for i in range(0, 43):
        p[i] -= qnt
    #kit variação
    for i in range(48, 68):
        p[i] -= qnt
    #envio das peças
    #envia_peca()

def envia_produto3(p,qnt):
    #kit basico
    for i in range(0, 43):
        p[i] -= qnt
    #kit variação
    for i in range(53, 73):
        p[i] -= qnt
    #envio das peças
    #envia_peca()

def envia_produto4(p,qnt):
    #kit basico
    for i in range(0, 43):
        p[i] -= qnt
    #kit variação
    for i in range(58, 68):
        p[i] -= qnt
    #envio das peças 
    #envia_peca()

def envia_produto5(p,qnt):
    #kit basico
    for i in range(0, 43):
        p[i] -= qnt
    #kit variação
    for i in range(67, 100):
        p[i] -= qnt
    #envio das peças
    #envia_peca()

#def envia_peca():
    #mqtt 
    
    
# Função para atualizar o estoque com base nas mensagens MQTT recebidas
#def atualizar_estoque(client, userdata, message, partes):
def atualizar_estoque(partes):    
    #payload = message.payload.decode("utf-8")
    # Analisar o JSON
    data = json.loads(json_data)
    nome_da_linha = data["linha"]
    print(f"requisição da linha: {nome_da_linha}")  
    # Chama as funções atualiza estoque de cada produto
    for i in range(1, 6):
        funcao = eval(f"envia_produto{i}")
        valor = data[f"peça{i}"]
        funcao(partes,valor)

    # Imprime o estoque atual após o consumo
    imprime_estoque(partes)
    # Verifica se o estoque está próximo do nível vermelho e emite ordem de reabastecimento se necessário
    verifica_kanban(partes)
     

# Configuração do cliente MQTT
#client = mqtt.Client()
#client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

# Inscreve-se no tópico para receber as mensagens de consumo de partes
#client.subscribe(TOPIC_CONSUMO_PARTES)
#client.message_callback_add(TOPIC_CONSUMO_PARTES, atualizar_estoque)

# Mantém o cliente MQTT em execução para receber as mensagens
#client.loop_forever()

def imprime_estoque(partes):

    print("Estoque atual:")
    for i, valor in enumerate(partes):
        print(f'parte: {i+1} Qntd: {valor}')

def verifica_kanban(partes):
   
    for i, valor in enumerate(partes):
        if(valor <= Yellow_value and valor > Red_value):
            print(f'peça:{i+1} kanban: yellow')
            # Aqui você pode enviar uma mensagem MQTT para o almoxarifado ou fornecedor para solicitar o reabastecimento
        elif(valor < Red_value):
            print(f'peça:{i+1} kanban: red')
        else:
            print(f'peça:{i+1} kanban: green')

def main():
    partes = [100] * 100   
    atualizar_estoque(partes) 
   

    

if __name__ == "__main__":
    main()


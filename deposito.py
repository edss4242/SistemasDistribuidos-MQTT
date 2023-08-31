import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import font
import json
import time
import threading

mensagem_recebida = False
#json_data_fabrica2 = None

#apenas para teste
json_data = '''
{
  "nome": "deposito",
  "produto1": 100,
  "produto2": 100,
  "produto3": 100,
  "produto4": 100,
  "produto5": 100
}
'''
# Configurações do Broker MQTT
broker_address = "localhost"
broker_port = 1883  # Porta padrão para MQTT

# Callback chamada quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código:", rc)
    client.subscribe("fabrica-deposito")  # inscreve ao tópico desejado

# Callback chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    global mensagem_recebida
    global json_data
    json_data = msg.payload.decode()
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    mensagem_recebida = True

#imprime a qnt de produtos em estoque
def recebe_Estoque(produtos):
    #implementar a leitura do json
    # Analisar o JSON
    global json_data
    data = json.loads(json_data)
    nome = data["nome"]
    print(f'Estoque recebido de: {nome}  valores atualizados:')

    for i in range(1, 6):
        nome_produto = f"produto{i}"
        valor = data.get(nome_produto, 0)
        produtos[i - 1] += valor
        print(f'Quantidade do produto {i} -> {valor}')
        
    return produtos

#monta um json com nome e qnt de cada produto
def envia_Estoque(nome,produto):
    global json_data
    data = json.loads(json_data)
    data["nome"] = nome
    #for i, qtd in enumerate(produto, start=1):
        #nome_produto = f"produto{i}"
        #data[nome_produto] = qtd
    
    json_str = json.dumps(data, indent=2)

    #criar funçao que envia esse json_str
    return json_str

def criar_janela(produto):
    # Criar uma janela
    janela = tk.Tk()
    janela.title("Deposito")

    for i in range(5):
        label = tk.Label(text=f"Produto {i+1}:  [{produto[i]}]",font=font.Font(size=16))
        label.grid(row=(i*2), column=0, sticky="w")

        #quebra de linha
        espaco_vazio = tk.Label(janela, text="", font=font.Font(size=16))
        espaco_vazio.grid(row=i*2+1, column=0, pady=10)
    #Iniciar o loop de eventos
    janela.mainloop() 



def main():
    produto = [100] * 5 
    global mensagem_recebida

    # Cria um cliente MQTT
    client = mqtt.Client()
    client.on_connect = on_connect  
    client.on_message = on_message

    # Criar uma thread para executar a função criar_janela
    thread = threading.Thread(target=criar_janela, args=(produto,))
    thread.start()

    # Conecta ao broker
    client.connect(broker_address, broker_port, 60) 
    # Mantém o cliente MQTT em execução
    client.loop_start()
    
    while True:
        
        global json_data
        #envia estoque
        json_data = envia_Estoque("Deposito",produto)
        client.publish("deposito-fabrica", json_data)  # Publica a mensagem no tópico
        print(f'publish do  json: {json_data} para fabrica2 ')

        # Aguarda até que a mensagem seja recebida
        while not mensagem_recebida:
            print("aguardando")
            time.sleep(5)
            pass
        ######################################

        produto = recebe_Estoque(produto)
        #print(f'{produto}')     

        # Conecta ao broker
        #client.connect(broker_address, broker_port, 60, json_data)

        # Aguarda por 30 segundos antes de executar novamente
        mensagem_recebida = False
        time.sleep(15)

        # Inicia o loop de rede do cliente
        #client.loop_forever()
   
if __name__ == "__main__":
    main()
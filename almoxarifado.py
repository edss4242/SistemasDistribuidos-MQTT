import paho.mqtt.client as mqtt
import random
import time
import json
import threading
import tkinter as tk
from tkinter import font

ESTOQUE_MAXIMO_PECAS = 100000000

DIAS_DA_SEMANA = {1: "Segunda-Feira", 2: "Terça-Feira", 3: "Quarta-Feira",
                  4: "Quinta-Feira", 5: "Sexta-Feira", 6: "Sabado",
                  7: "Domingo"}

QTD_TIPO_PECAS = 1
NIVEIS_OPERACAO = {"VERMELHO": ESTOQUE_MAXIMO_PECAS*0.2, "AMARELO": ESTOQUE_MAXIMO_PECAS*0.5} 
QTD_PRODUTOS = 5

entrega_recebida = {}
pedido_recebido = {}
source = 0


whoami = "Almoxarifado novo"
    
#topicos de comunicação
    
topico_identificacao = "Matriz - Almoxarifado"
topico_alocacao = "Almoxarifado - Matriz"
topico_receber_pedido = "Fabrica - Almoxarifado"
topico_enviar = "Almoxarifado - Fabrica"
topico_pedir = "Fornecedor - Almoxarifado"
topico_receber = "Almoxarifado - Fornecedor"
topics = [topico_identificacao, topico_receber,
              topico_receber_pedido]

def client_almoxarifado():

    #Setup inicial
    
    today = 1
    id_request = 0 
    estoque_pecas = []
    consumo = []
    consumo_dia = []
    pedido = {}
    fazer_pedido = False
    global entrega_recebida
    global pedido_recebido
    global whoami

    for i in range(QTD_TIPO_PECAS):
        estoque_pecas.append(ESTOQUE_MAXIMO_PECAS)
        consumo.append(0)
        consumo_dia.append(0)

    #Start Client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    conexao_padrao(client)
    client.loop_start()
    
    # Criar uma thread para executar o sub
    sub_thread_forncedor = threading.Thread(target=sub, args=(client, topico_receber,))
    sub_thread_fab = threading.Thread(target=sub, args=(client, topico_receber_pedido,))
    
    # Criar uma thread para executar a função criar_janela
    #thread_window = threading.Thread(target=criar_janela, args=(estoque_produtos,))
    
    #thread_window.start()
    sub_thread_fab.start()
    sub_thread_forncedor.start()
    
    #identificacao da fabrica
    indentificacao(client, topico_alocacao)
    while whoami == "Almoxarifado novo":
        time.sleep(1)
        indentificacao(client, topico_alocacao, "again")


    while True:
        #inicio do dia
        try:
            if entrega_recebida["nome"] == whoami:
                estoque_pecas = abastecimento(estoque_pecas)
                print("abastecido. Estoque atual:", estoque_pecas)
                time.sleep(2)
        except:
            pass

        try:
            if len(pedido_recebido["nome"]) > 0:
                
                consumo_dia = consome_pedido(consumo, pedido_recebido)
                client.publish(topico_enviar, str(pedido_recebido).encode(), qos = 1)
                print("pedido", str(pedido_recebido), "enviado para a fabrica")
                pedido_recebido = {}
            
        except:
            pass
        estoque_pecas = consumir(estoque_pecas, consumo_dia)
        consumo_dia = consumo_reset()

        pedido["nome"] = whoami
        soma = 0
        for i in range(QTD_TIPO_PECAS):
            peca = "peca"+str(i+1)
            if estoque_pecas[i] < NIVEIS_OPERACAO["AMARELO"]*0.5:
                pedido[peca] = (ESTOQUE_MAXIMO_PECAS - estoque_pecas[i])
                soma += pedido[peca]
            else:
                pedido[peca] = 0 

        if soma != 0 and fazer_pedido:    
            message = whoami + "- #"+str(id_request)+" - "+ str(pedido)
            id_request += 1
            client.publish(topico_pedir, message.encode(), qos = 1)
            print("pedido", message, "feito!")
            pedido = {}
            fazer_pedido = False
            time.sleep(1)

        # fim do dia
        
        print("DIA", today, ":", estoque_pecas)
        if today%2 == 0:
            fazer_pedido = True
        today += 1
        time.sleep(1)

#reseta os pedidos para próxima semana
def consumo_reset():
    reset = []
    for i in range(QTD_TIPO_PECAS):
        reset.append(0)

    return reset

#consumo do dia
def consome_pedido(consumo, pedido):
    consumo_dia = 0
    for i in range(QTD_TIPO_PECAS):
        peca = "peca"+str(i+1)
        consumo_dia += pedido[peca]

    return [consumo_dia]

#efetivamente reduzir o estoque
def consumir(estoque, consumo_dia):
    for i in range(QTD_TIPO_PECAS):
        estoque[i] -= consumo_dia[i]

    return estoque

def indentificacao(client, topico, message = "Novo almoxarifado"):
    client.publish(topico, message.encode(), qos = 1)

def abastecimento(estoque):
    global entrega_recebida

    for i in range(QTD_TIPO_PECAS):
        estoque[i] += entrega_recebida["pecas"]

    entrega_recebida = {}
    return estoque

def conexao_padrao(client):
    client.connect("broker.hivemq.com", 1883, keepalive=30)

def on_disconnect(client, userdata, rc):
    print("voce caiu! Tente reconexão!")
    
    while True:
        try:     
            conexao_padrao(client)
            #print("Conectado ao broker com código:", rc)
            break
        except:
            pass 

def sub(client, topico):
    try:
        client.subscribe (topico, qos=1)
        client.loop_start()
    except:
        pass

def criar_janela(produto):
    # Criar uma janela
    janela = tk.Tk()
    janela.title("Almoxarifado")

    for i in range(QTD_TIPO_PECAS):
        label = tk.Label(text=f"Quantidade Peças {i+1}:  [{produto[i]}]",font=font.Font(size=16))
        label.grid(row=(i*2), column=0, sticky="w")

        #quebra de linha
        espaco_vazio = tk.Label(janela, text="", font=font.Font(size=16))
        espaco_vazio.grid(row=i*2+1, column=0, pady=10)
    #Iniciar o loop de eventos
    janela.mainloop()

# Callback chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    global entrega_recebida
    global pedido_recebido
    global source
    global whoami
    #print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    
    if msg.topic == "Matriz - Almoxarifado":
        whoami = "Almoxarifado "+msg.payload.decode()
        print("indentificacao feita:", whoami)
    
    if msg.topic == "Fabrica - Almoxarifado":
        source = (msg.payload.decode().split("-")[0])
        pedido_recebido = json.loads(msg.payload.decode().split("-")[2].replace("\'", "\""))

    if msg.topic == "Fornecedor - Almoxarifado":
            entrega_recebida = msg.payload.decode()
    

    

# Callback chamada quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    global topics
    
    for i in topics:
        client.subscribe (i, qos=1)
 
if __name__ == "__main__":
    client_almoxarifado()


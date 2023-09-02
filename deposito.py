import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import font
import json
import time
import threading
import random

ESTOQUE_MAXIMO = 100
QTD_PRODUTOS = 5
DIAS_DA_SEMANA = {1: "Segunda-Feira", 2: "Terça-Feira", 3: "Quarta-Feira",
                  4: "Quinta-Feira", 5: "Sexta-Feira", 6: "Sabado",
                  7: "Domingo"}

entrega_recebida = {}
ARQUIVO_ESTOQUE = "estoque.txt"

whoami = "Deposito novo"


#topicos de comunicação
topico_identificacao = "Matriz - Deposito"
topico_alocacao = "Deposito - Matriz"
topico_pedir = "Deposito - Fabrica"
topico_receber = "Fabrica - Deposito"
topics = [topico_identificacao, topico_receber]

#Principal fluxo para um deposito
def client_deposito():

    #Setup inicial
    
    today = 1
    id_request = 0
    fazer_pedido = False 
    
    estoque_produtos = []
    consumo = []
    consumo_dia = []
    global entrega_recebida
    global whoami

    for i in range(QTD_PRODUTOS):
        estoque_produtos.append(ESTOQUE_MAXIMO)
        consumo.append(0)
        consumo_dia.append(0)
        while True:
            try:
                with open(ARQUIVO_ESTOQUE, "w") as file:
                    file.write(str(estoque_produtos))
                break
            except:
                time.sleep(0.5)

    #Start Client
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect("broker.hivemq.com", 1883)
    client.loop_start()
    
    # Criar threads para executar os subs
    sub_thread_fab = threading.Thread(target=sub, args=(client, topico_receber,))
    sub_thread_matriz = threading.Thread(target=sub, args=(client, topico_identificacao,))
    

    # Criar uma thread para executar a função criar_janela
    thread_window = threading.Thread(target=criar_janela, args=())
    
    #start threads sub
    #thread_window.start()
    sub_thread_fab.start()
    sub_thread_matriz.start()

    #identificação
    indentificacao(client, topico_alocacao)
    while whoami == "Deposito novo":
        time.sleep(1)
        indentificacao(client, topico_alocacao, "again")

    #inicio do dia


    while True:
        try:
            if entrega_recebida["nome"] == whoami:
                estoque_produtos = abastecimento(estoque_produtos)
                print("abastecido. Estoque atual:", estoque_produtos)
                time.sleep(2)
        except:
            pass
        
        #print("Hoje é", DIAS_DA_SEMANA[today])
        consumo, consumo_dia = consome_random(consumo)
        estoque_produtos = consumir(estoque_produtos, consumo_dia)
        if fazer_pedido:
            pedido = {
            "nome": whoami,
            "produto1": consumo[0],
            "produto2": consumo[1],
            "produto3": consumo[2],
            "produto4": consumo[3],
            "produto5": consumo[4]
            }
            message = whoami + "- #"+str(id_request)+" - "+ str(pedido)
            id_request += 1
            client.publish(topico_pedir, message.encode(), qos = 1)
            print("pedido", message, "feito!")
            consumo = consumo_reset()
            fazer_pedido = False
    
        #fim do dia
        gravar_estoque(estoque_produtos)
        

        if today%7 == 0:
            fazer_pedido = True
        today += 1
        time.sleep(1)


def indentificacao(client, topico, message = "Novo deposito"):
    client.publish(topico, message.encode(), qos = 1)



#gravar dado em arquivo apoio para comunicação com interface grafica
def gravar_estoque(estoque_produtos):
    while True:
            try:
                with open(ARQUIVO_ESTOQUE, "w") as file:
                    file.write(str(estoque_produtos))
                break
            except:
                time.sleep(0.5)

#reseta os pedidos para próxima semana
def consumo_reset():
    reset = []
    for i in range(QTD_PRODUTOS):
        reset.append(0)

    return reset

#consumo do dia
def consome_random(consumo):
    consumo_dia = []
    for i in range(QTD_PRODUTOS):
        consumo_dia.append(random.randrange(0,10))
        consumo[i] += consumo_dia[i]

    return consumo, consumo_dia

#efetivamente reduzir o estoque
def consumir(estoque_produtos, consumo_dia):
    for i in range(QTD_PRODUTOS):
        estoque_produtos[i] -= consumo_dia[i]

    return estoque_produtos

#armazenagem do recebimento
def abastecimento(estoque):
    global entrega_recebida

    for i in range(QTD_PRODUTOS):
        produto = "produto"+str(i+1)
        estoque[i] += entrega_recebida[produto]

    entrega_recebida = {}
    return estoque


# Callback chamada quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    global topics
    
    for i in topics:
        client.subscribe (i, qos=1)

#Thread de subscriber    
def sub(client, topico):
    client.subscribe (topico, qos=1)
    client.loop_start()


# Callback chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    global entrega_recebida
    global whoami

    if msg.topic == "Matriz - Deposito":
        whoami = "Deposito "+msg.payload.decode()
        print("indentificacao feita:", whoami)

    else:    
        try:
            message = msg.payload.decode().replace("\'", "\"")
            entrega_recebida = json.loads(message)
        except:
            pass
#leitura de estoque para interface grafica
def update_produtos(produto):
    while True:
            try:
                with open(ARQUIVO_ESTOQUE, "r") as file:
                    output = file.read()
                    output = output[1:-1].replace(" ", "").split(",")
                    for i in range(QTD_PRODUTOS):
                        produto[i].set(int(output[i]))
                break
            except:
                time.sleep(0.5)
    
    return produto

#interface grafica
def criar_janela():
    # Criar uma janela
    janela = tk.Tk()
    janela.title("Deposito")
    produto = []
    for i in range(QTD_PRODUTOS):
        produto.append(0)
        produto[i] = tk.IntVar()
    produto = update_produtos(produto)
 
    while True:
        for i in range(QTD_PRODUTOS):
            text = "Produto "+str(i+1)+": " + str(produto[i].get())
            try:
                label = tk.Label(janela, text=text, font=font.Font(size=16))
                label.grid(row=(i*2), column=5, sticky="w")


                #quebra de linha
                espaco_vazio = tk.Label(janela, text="", font=font.Font(size=16))
                espaco_vazio.grid(row=i*2+1, column=5, pady=10)
            except:
                pass

        #Iniciar o loop de eventos
         
        try:
            janela.update()
            time.sleep(3)
            janela.after(5000, update_produtos(produto))
            for widget in janela.winfo_children():
                widget.destroy()
                time.sleep(0.2)
        except:
            time.sleep(0.5)

   
if __name__ == "__main__":
    client_deposito()
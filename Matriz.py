import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import font
import json
import time
import threading
import random



depositos = 0
fabricas = 0
almoxarifados = 0


#topicos
topico_alocacao_deposito = "Deposito - Matriz"
topico_alocacao_fabrica = "Fabrica - Matriz"
topico_alocacao_almoxarifado = "Almoxarifado - Matriz"
topics = [topico_alocacao_deposito, topico_alocacao_almoxarifado, topico_alocacao_fabrica]    

#Principal fluxo para um deposito
def client_matriz():

    
    #Start Client
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect("broker.hivemq.com", 1883)
    client.loop_start()
    
    # Criar threads para executar os subs
    sub_thread_dep = threading.Thread(target=sub, args=(client, topico_alocacao_deposito,))
    sub_thread_fab = threading.Thread(target=sub, args=(client, topico_alocacao_fabrica,))
    sub_thread_almox = threading.Thread(target=sub, args=(client, topico_alocacao_almoxarifado,))
    
    #start threads sub
    sub_thread_dep.start()
    sub_thread_fab.start()
    sub_thread_almox.start()


    #inicio do dia
    while True:
        #client.loop_forever()
        pass
    



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
    global depositos
    global fabricas
    global almoxarifados

    if msg.topic == "Deposito - Matriz":
        if msg.payload.decode() == "Novo deposito":
            depositos += 1
        message = str(depositos)
        client.publish("Matriz - Deposito", message.encode(), qos = 1)
    else:
        if msg.topic == "Fabrica - Matriz":
            if msg.payload.decode() == "Nova fabrica":
                fabricas += 1
            message = str(fabricas)
            client.publish("Matriz - Fabrica", message.encode(), qos = 1)
        else:
            if msg.payload.decode() == "Novo almoxarifado":
                almoxarifados += 1
            message = str(almoxarifados)
            client.publish("Matriz - Almoxarifado", message.encode(), qos = 1)


#interface grafica
   
if __name__ == "__main__":
    client_matriz()
import paho.mqtt.client as mqtt
import tkinter as tk
import json

#constantes
Red_value = 80
Yellow_value = 95

#apenas para teste
json_data = '''
{
  "linha": "linha1",
  "produto1": 15,
  "produto2": 1,
  "produto3": 0,
  "produto4": 0,
  "produto5": 20
}
'''

# Configurações MQTT
MQTT_BROKER_HOST = "hivemq_broker_container"
MQTT_BROKER_PORT = 1883
TOPIC_CONSUMO_PARTES = "consumo/partes"

def envia_produto1(p,qnt,nome):
    #kit basico
    for i in range(0, 43):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #kit variação
    for i in range(43, 63):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #envio das peças
    #envia_peca()

def envia_produto2(p,qnt,nome):
    #kit basico
    for i in range(0, 43):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #kit variação
    for i in range(48, 68):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #envio das peças
    #envia_peca()

def envia_produto3(p,qnt,nome):
    #kit basico
    for i in range(0, 43):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #kit variação
    for i in range(53, 73):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #envio das peças
    #envia_peca()

def envia_produto4(p,qnt,nome):
    #kit basico
    for i in range(0, 43):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #kit variação
    for i in range(58, 78):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #envio das peças 
    #envia_peca()

def envia_produto5(p,qnt,nome):
    #kit basico
    for i in range(0, 43):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
    #kit variação
    for i in range(67, 100):
        if(nome != "fornecedor"):
            p[i-1] -= qnt
        else:
            p[i-1] += qnt
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
        valor = data[f"produto{i}"]
        funcao(partes,valor,nome_da_linha)

    # Imprime o estoque atual após o consumo
    imprime_estoque(partes)
    
     

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
        # Verifica se o estoque está próximo do nível vermelho e emite ordem de reabastecimento se necessário
        verifica_kanban(valor,i)

def verifica_kanban(valor,i):

        if(valor <= Yellow_value and valor > Red_value):
            print(f'peça:{i+1} kanban: yellow')
            # Aqui você pode enviar uma mensagem MQTT para o almoxarifado ou fornecedor para solicitar o reabastecimento
        elif(valor < Red_value):
            print(f'kanban: red')
        else:
            print(f'kanban: green')

def criar_quadrado_vermelho(master):
    quadrado = tk.Canvas(master, width=10, height=10, bg="red")
    quadrado.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="e")
    return quadrado

def criar_quadrado_amarelo(master):
    quadrado = tk.Canvas(master, width=10, height=10, bg="yellow")
    quadrado.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="e")
    return quadrado

def criar_quadrado_verde(master):
    quadrado = tk.Canvas(master, width=10, height=10, bg="green")
    quadrado.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="e")
    return quadrado


def main():
    partes = [100] * 100  
    atualizar_estoque(partes)

    # Criar uma janela
    janela = tk.Tk()
    janela.title("Almoxarifado")

    for i in range(100):
        row = i % 25  # Linha atual (0 a 24), repetindo a cada 25 labels
        column = i // 25  # Coluna atual (0 a 3)
        
        frame = tk.Frame(janela)
        frame.grid(row=row, column=column, padx=150, pady=5, sticky="w")
        
        label = tk.Label(frame, text=f"Partes {i+1}:  [{partes[i-1]}]")
        label.grid(row=0, column=0, sticky="w")
        
        if(partes[i-1] < Yellow_value and partes[i-1 ] > Red_value):
            quadrado = criar_quadrado_amarelo(frame)
        elif(partes[i-1]<Red_value):
            quadrado = criar_quadrado_vermelho(frame)
        else:
            quadrado = criar_quadrado_verde(frame)



    #Iniciar o loop de eventos
    janela.mainloop()   

if __name__ == "__main__":
    main()


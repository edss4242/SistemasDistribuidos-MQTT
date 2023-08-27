import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import font
import json


#apenas para teste
json_data = '''
{
  "nome": "deposito",
  "produto1": 15,
  "produto2": 7,
  "produto3": 0,
  "produto4": 0,
  "produto5": 2
}
'''

#imprime a qnt de produtos em estoque
def recebe_Estoque(produtos):
    #implementar a leitura do json
    # Analisar o JSON
    data = json.loads(json_data)
    nome = data["nome"]
    print(f'Estoque recebido de: {nome} \n valores atualizados:')

    for i in range(1, 6):
        nome_produto = f"produto{i}"
        valor = data.get(nome_produto, 0)
        produtos[i - 1] += valor
        print(f'Quantidade do produto {i} -> {valor}')
        
    return produtos

#monta um json com nome e qnt de cada produto
def envia_Estoque(nome,produto):
    json_data = {
        "linha": nome
    }
    for i, qtd in enumerate(produto, start=1):
        nome_produto = f"produto{i}"
        json_data[nome_produto] = qtd
    
    json_str = json.dumps(json_data, indent=2)

    #criar funçao que envia esse json_str
    return json_str


def main():
    produto = [0] * 5   

    # Criar uma janela
    janela = tk.Tk()
    janela.title("Deposito")

  
    produto = recebe_Estoque(produto)
    for i in range(5):
        label = tk.Label(text=f"Produto {i+1}:  [{produto[i]}]",font=font.Font(size=16))
        label.grid(row=(i*2), column=0, sticky="w")

        #quebra de linha
        espaco_vazio = tk.Label(janela, text="", font=font.Font(size=16))
        espaco_vazio.grid(row=i*2+1, column=0, pady=10)

    
    json_data = envia_Estoque("Deposito",produto)
    print(json_data)

    #Iniciar o loop de eventos
    janela.mainloop() 
   
if __name__ == "__main__":
    main()
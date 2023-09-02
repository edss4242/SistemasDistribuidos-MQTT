import paho.mqtt.client as mqtt

# Configurações do broker
broker_address = "localhost"  # Endereço do broker 
port = 1883                   # Porta padrão para MQTT

# Callback chamada quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código:", rc)

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Conecta ao broker
client.connect(broker_address, port, 60)

# Loop para manter a conexão
client.loop_start()

while True:
    mensagem = input("Digite a mensagem a ser enviada: ")
    client.publish("meu/topico", mensagem)  # Publica a mensagem no tópico

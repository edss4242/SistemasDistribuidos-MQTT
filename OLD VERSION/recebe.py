import paho.mqtt.client as mqtt

# Configurações do broker
broker_address = "localhost"  # Endereço do broker (no caso do mesmo PC, use "localhost")
port = 1883                   # Porta padrão para MQTT

# Callback chamada quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código:", rc)
    client.subscribe("meu/topico")  # Subscreve ao tópico desejado

# Callback chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conecta ao broker
client.connect(broker_address, port, 60)

# Loop para manter a conexão
client.loop_forever()

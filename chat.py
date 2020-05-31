import requests
import time
from signalrcore.hub_connection_builder import HubConnectionBuilder

negotiate_url='https://chat-py.azurewebsites.net/api/negotiate'
messages_url='https://chat-py.azurewebsites.net/api/messages'
response=requests.post(negotiate_url)
result=response.json()
server_url=result['url']
connection_open=False
offset=40


# {"url":"https://da-rpi-signalr.service.signalr.net/client/?hub=chat","accessToken":"<token>"}
def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value

username = input_with_default('Enter your username (default: {0}): ', "User-1")

def on_open():
    """hub connection on open handler"""
    print("connection opened and handshake received ready to send messages\n")
    global connection_open
    connection_open=True

def on_close():
    """hub connection on close handler"""
    global connection_open
    connection_open=False
    print("\rconnection closed")

def print_message(msg):
    sender=msg[0]['sender']
    text=msg[0]['text']
    if sender != username:
        print(f"\r{sender}: {text}" + (" " * offset) + "\n" + (" " * offset) + f"{username}:", end="")



hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={
        "access_token_factory": lambda: result['accessToken']
    }).with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()

hub_connection.on_open(on_open)
hub_connection.on_close(on_close)
hub_connection.on("newMessage", print_message)
hub_connection.start()

message = None

while message != "exit()":
    if connection_open:
        print(" " * offset + f"{username}:", end="")
        message = input()
        if message != None and message != "" and message != "exit()":
            # hub_connection.send("SendMessage", [username, message])
            resp=requests.post(messages_url, json={"sender": username, "text": message})
    else:
        print ("Loading...", end="\r")
        time.sleep(1)

hub_connection.stop()

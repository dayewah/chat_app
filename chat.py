import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder

negotiate_url='https://chat-func-py.azurewebsites.net/api/negotiate'
messages_url='https://chat-func-py.azurewebsites.net/api/messages'
response=requests.post(negotiate_url)
result=response.json()
server_url=result['url']

# {"url":"https://da-rpi-signalr.service.signalr.net/client/?hub=chat","accessToken":"<token>"}
def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value

username = input_with_default('Enter your username (default: {0}): ', "User-1")

hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={
        "access_token_factory": lambda: result['accessToken']
    }).with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()

hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages\n"))
hub_connection.on_close(lambda: print("connection closed"))
hub_connection.on("newMessage", lambda msg:print(f"{msg[0]['sender']}: {msg[0]['text']}"))
hub_connection.start()

message = None

while message != "exit()":
    message = input()
    if message is not None and message is not "" and message is not "exit()":
        # hub_connection.send("SendMessage", [username, message])
        resp=requests.post(messages_url, json={"sender": username, "text": message})

hub_connection.stop()

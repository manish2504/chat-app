'Chat Room Connection - Client-To-Client'
import threading
import socket


host = '127.0.0.1'  # local host
port = 59000

# server object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server to host and port
server.bind((host, port))
server.listen()
clients = []
aliases = []


# message from server to all clients
def broadcast(message):
    for client in clients:
        client.send(message)



# Function to handle clients'connections
def handle_client(client):
    while True:
        try:
            # Maximum amount of bytes server can receive from client
            message = client.recv(1024)
            broadcast(message)
        except:
            # Identify client clien index from clients that is causing error
            index = clients.index(client)
            clients.remove(client)  
            client.close()
            alias = aliases[index]
            # Send message in form of bytes
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break


# Main function to receive the clients connection
def receive():
    while True:
        print('Server is running and listening ...')
        # accept method is actively running and accepting new connection ; returns a new socket representing a connection and an address
        client, address = server.accept()


        # convet int address to string
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))

        # envoke and start the thread
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()

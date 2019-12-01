import socket

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 22  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect(("192.168.1.40", port))  # connect to the server

    message = raw_input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = raw_input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()

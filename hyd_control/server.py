import socket
import threading

HEADER = 64
PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
connected = False
print(SERVER)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        id_length = conn.recv(HEADER).decode(FORMAT)
        if id_length:
            id_length = int(id_length)
            _id = conn.recv(id_length).decode(FORMAT)
            if _id == DISCONNECT_MESSAGE:
                connected = False
            print(_id)
        script_length = conn.recv(HEADER).decode(FORMAT)
        if script_length:
            script_length = int(script_length)
            script = conn.recv(script_length).decode(FORMAT)
            if script == DISCONNECT_MESSAGE:
                connected = False
            print(script)

    conn.close()


def __check_connection__(conn):
    try:
        send_length = str(len("[CONNECTION_CHECK]")).encode('utf-8')
        send_length += b' ' * (64 - len(send_length))
        conn.send(send_length)
        conn.send(bytes("[CONNECTION_CHECK]", "UTF-8"))
        return True
    except socket.error as err:
        print("bag pula")
        return False


def send_commands(conn, addr):
    while True:
        if not __check_connection__(conn):
            break
        command = input()
        command = command.encode('utf-8')
        msg_length = len(command)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (64 - len(send_length))

        conn.send(send_length)
        conn.send(command)

    print("disconnected")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        connected = True
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        thread2 = threading.Thread(target=send_commands, args=(conn, addr))
        thread2.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        conn2, addr2 = server.accept()
        conn.close()
        thread.join()
        thread2 = threading.Thread(target=handle_client, args=(conn2, addr2))
        thread2.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()

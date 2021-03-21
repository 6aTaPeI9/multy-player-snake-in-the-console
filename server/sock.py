import socket
from select import select

SERVER_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKETS = [SERVER_SOCK]

def accept(sock):
    cl_sock, _ = sock.accept()
    SOCKETS.append(cl_sock)

    return


def recv(sock):
    req = sock.recv(1024)

    if not req:
        SOCKETS.remove(sock)


def loop():
    while True:
        ready_sock, _, _ = select(SOCKETS, [], [])

        for sock in ready_sock:
            if sock is SERVER_SOCK:
                accept(sock)
            else:
                recv(sock)

if __name__ == '__main__':
    SERVER_SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER_SOCK.bind(('localhost', 5000))
    SERVER_SOCK.listen(5)
    print('Запущено')
    loop()
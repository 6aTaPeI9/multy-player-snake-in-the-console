import threading
from websocket import wsocket

from select import select
from room import Room

# Длительность опроса сокетов на входящий и исходящие данные.
SELECT_TIMEOUT = 1

def accept(sock: wsocket.WSocket, room: Room):
    """
        Прием подключения нового игрока.
    """
    player_sock, _ = sock.accept()

    if player_sock.status == 1:
        player_sock.handshake()
    else:
        pass
    return

# def recv(sock):
#     req = sock.recv(1024)

#     if not req:
#         SOCKETS.remove(sock)

def receive_data(serv_sock: wsocket.WSocket, room: Room):
    """
        Метод слушает новые подключения игроков и получает данные
        от уже подключенных.
    """
    while True:
        receive_sock, send_sock, _ = select(room.players, [], [], SELECT_TIMEOUT)

        for player in receive_sock:
            if player is serv_sock:
                player.check_steps()
            else:
                

        for player in send_sock:


if __name__ == '__main__':
    SERVER_SOCK = wsocket.WSocket(wsocket.socket.AF_INET, wsocket.socket.SOCK_STREAM)
    SERVER_SOCK.setsockopt(wsocket.socket.SOL_SOCKET, wsocket.socket.SO_REUSEADDR, 1)
    SERVER_SOCK.bind(('localhost', 5000))
    SERVER_SOCK.listen(5)

    SOCKETS = [SERVER_SOCK]
    threading.Thread(target=receive_data, args=(SERVER_SOCK, SOCKETS)).start()

from wsocket import WSocket
from socket import AF_INET, SOCK_STREAM
from email.parser import BytesParser

web_sock_guid = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

sock = WSocket(AF_INET, SOCK_STREAM)
sock.bind(('localhost', 5555))
sock.listen(5)

while True:
    print('Слушаем...')
    conn = sock.accept()[0]
    print('Новое подключие')
    while True:
        print('Ждем...: ')
        dt = conn.recv(1024)

        for row in dt.decode().split('\r\n'):
            print(row)

        print('Получено: ' + str(dt))

        dt = conn.send("""HTTP/1.1 101 Web Socket Protocol Handshake\r\nServer: my_server\r\nUpgrade: websocket\r\n\n""".encode())




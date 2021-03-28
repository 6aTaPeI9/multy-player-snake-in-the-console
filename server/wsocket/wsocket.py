# -*- coding: utf-8 -*-
"""
    Модуль содержит обертку над стандартным сокетом с
    частичной реализацией протокола websocket 13 версии.
"""

import socket
import time

from .headers import HttpRequest
from . import handshake, framing

class ConnStatus:
    """
        Статусы соединения
    """
    # Статус ожидания рукопожатия
    CONNECTING = 0

    # активное соединение
    CONNECTED = 1

    # Ожидание чистого отключения
    CLOSING = 2

    # сокет отключен
    CLOSED = 3


class PingStatus:
    """
        Статусы пинга
    """
    # Пинг отрпавлен
    SENDED = 0

    # Понг получен
    RECIEVED = 1

class WSocket(socket.socket):
    def __init__(self, *args, **kwargs):
        """
            Инциализация сокета с частичной поддержкой
            протокола WebSocket v13
        """
        super().__init__(*args, **kwargs)

        # Устанавливаем соединение в статус установки соединения.
        self.status = ConnStatus.CONNECTING

        # момент следующего пинга
        self.next_ping = None

        # Статус пинга
        self.ping_status = PingStatus.RECIEVED

        return


    def recv(self, *args, **kwargs):
        """
            Обертка над методом ожидания новых данных
        """
        recv_data = super().recv(*args, **kwargs)

        # Если установлен статус подключения
        # выполняем рукопожатие

        if self.status == ConnStatus.CONNECTING:
            self.handshake(recv_data)
            return None
        else:
            recv_data = framing.read_frame(recv_data)

        return recv_data


    def accept(self, *args, **kwargs):
        """
            Обертка над методом ожидания новых подключений
        """
        fd, addr = self._accept()
        sock = WSocket(self.family, self.type, self.proto, fileno=fd)

        if socket.getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)

        return sock, addr


    def handshake(self, req_data: bytes):
        """
            Выплнение рукопожатия
        """
        # Запрос
        req = HttpRequest()

        # Парсим http заголовки
        req.read_request(req_data)

        for k, v in req.headers.items():
            print(k, ': ', v)

        # Ответ
        answer = HttpRequest()
        try:
            # Валидируем входящий запрос для выполнения рукопожатия
            s_w_key = handshake.validate_request(req)
        except Exception as ex:
            s_w_key = None
            answer.write_exc(ex)

        handshake.build_response(answer, s_w_key)

        self.send(answer.to_request().encode())

        if answer.exception is None:
            print('Успешно')
            self.status = ConnStatus.CONNECTED

        return True


    def fileno(self):
        """
            Обработчик получения файлового дескриптора сокета.
        """
        # TODO делаем пинг если пришло время
        return super().fileno()


    def _ping(self):
        """
            Выполняем ping клиента
        """
        pass

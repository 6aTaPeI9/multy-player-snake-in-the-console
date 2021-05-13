# -*- coding: utf-8 -*-
"""
    Модуль содержит обертку над стандартным сокетом с
    частичной реализацией протокола websocket 13 версии.
"""

import json
import socket
import time

from . import handshake
from .framing import Frame, OpCodes
from .headers import HttpRequest
from .const import ConnStatus, PingStatus, SockEvents

# Частота пинга(в секундах)
PING_FREQ = 5


class WSocket(socket.socket):
    def __init__(self, *args, ping: bool = True, **kwargs):
        """
            Инциализация сокета с частичной поддержкой
            протокола WebSocket v13
        """
        super().__init__(*args, **kwargs)

        # Устанавливаем соединение в статус установки соединения.
        self.status = ConnStatus.CONNECTING

        # Время отправки последнего пинга
        self.ping_time = time.time()

        # Тело пинга.
        # При каждой вызове генериурется случайное тело.
        self.ping_body = None

        # Статус пинга
        self.ping_status = PingStatus.RECIEVED
        self.do_ping = ping

        # Обработчики для событий
        self._handlers = {}


    def recv(self, *args, **kwargs):
        """
            Обертка над методом ожидания новых данных
        """
        recv_data = super().recv(*args, **kwargs)

        # Если установлен статус подключения
        # выполняем рукопожатие
        if self.status == ConnStatus.CONNECTING:
            self.handshake(recv_data)
        elif self.status == ConnStatus.CONNECTED:
            row_data = Frame(frame=recv_data)

            if not row_data.data():
                return

            parsed_data = row_data.data()
            op_code = int(parsed_data.get('OpCode'), 16)

            if op_code in (OpCodes.OP_PING, OpCodes.OP_PONG):
                print('PONG')
                self.ping_status = PingStatus.RECIEVED
                return

            if op_code == OpCodes.OP_CLOSE:
                self._close(from_client=True)
                return
            print('Пришли данные', row_data.data())
            try:
                data = json.loads(row_data.data().get('Data'))
                self._execute_handler(data[0], data=data[1])
            except Exception as ex:
                print(ex)


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

        super().send(answer.to_request().encode())

        if answer.exception is None:
            self.status = ConnStatus.CONNECTED
            # Выполняем обработчик нового подключения
            self._execute_handler(SockEvents.CONNECTED)

        return True


    def fileno(self):
        """
            Обработчик получения файлового дескриптора сокета.
        """
        if self.do_ping:
            self.ping()

        return super().fileno()


    def ping(self):
        """
            Проверка статуса клиента.
            Метод по необходимости отправляет пинг
        """
        # Проверяем актуальность последнего пинга
        if (time.time() - self.ping_time) > PING_FREQ:
            if self.ping_status == PingStatus.SENDED:
                self._close()
            else:
                self.send('ping', OpCodes.OP_PING)
                self.ping_status = PingStatus.SENDED
                self.ping_time = time.time()
                print('PING')


    def send(self, data, op_code: OpCodes.OP_TEXT):
        """
            Отправка данных
        """
        frame = Frame(data=data)
        frame.set_op_code(op_code)
        super().send(frame.frame())


    def _close(self, from_client: bool = False):
        """
            Закрытие соединения
        """
        if not from_client:
            self.send('close', OpCodes.OP_CLOSE)

        self.status = ConnStatus.CLOSED
        self._execute_handler(SockEvents.CONN_CLOSE)
        self.close()


    def on(self, event: str, handler):
        """
            Добавление обработчиков входящих данных
        """
        if self._handlers.get(event) is not None:
            raise ValueError(f'Обработчик с именем {event} уже добавлен.')

        self._handlers[event] = handler


    def on_close(self, handler):
        """
            Оброботчик закрытия соединения
        """
        self.on(SockEvents.CONN_CLOSE, handler)


    def on_connect(self, handler):
        """
            Оброботчик нового подключения.
            Вызывает после выполнения рукопожатия.
        """
        self.on(SockEvents.CONNECTED, handler)


    def _execute_handler(self, event: str, **kwargs):
        """
            Выполнение обработчика, если он есть.
        """

        handl = self._handlers.get(event)

        if not handl:
            print(f'Не найден обработчик для события {event}')
            return

        handl.call({'socket': self, **kwargs})
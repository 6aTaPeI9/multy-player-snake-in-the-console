from wsocket import WSocket
from socket import AF_INET, SOCK_STREAM
from email.parser import BytesParser

# Максимальное кол-во заголовков
MAX_HEADERS = 256

# Максимальная длина контента одного заголовка
MAX_LINE = 4096

USER_AGENT = f"Python/{sys.version[:3]} snakegame/1"


def read_request(stream):
    """

    """

    request_line = read_line(stream)

    try:
        method, raw_path, version = request_line.split(b" ", 2)
    except ValueError:
        raise ValueError(f"invalid HTTP request line: {d(request_line)}")

    if method != b"GET":
        raise ValueError(f"unsupported HTTP method: {d(method)}")
    if version != b"HTTP/1.1":
        raise ValueError(f": {d(version)}")
    path = raw_path.decode("ascii", "surrogateescape")

    headers = read_headers(stream)

    return path, headers


def read_response(stream):
    """

    """
    status_line = read_line(stream)

    try:
        version, raw_status_code, raw_reason = status_line.split(b" ", 2)
    except ValueError:
        raise ValueError(f"invalid HTTP status line: {d(status_line)}") from None

    if version != b"HTTP/1.1":
        raise ValueError(f"unsupported HTTP version: {d(version)}")
    try:
        status_code = int(raw_status_code)
    except ValueError:
        raise ValueError(f"invalid HTTP status code: {d(raw_status_code)}") from None
    if not 100 <= status_code < 1000:
        raise ValueError(f"unsupported HTTP status code: {d(raw_status_code)}")
    if not _value_re.fullmatch(raw_reason):
        raise ValueError(f"invalid HTTP reason phrase: {d(raw_reason)}")

    reason = raw_reason.decode()

    headers = read_headers(stream)

    return status_code, reason, headers


def read_headers(stream):
    """
    """
    headers = {}

    for _ in range(MAX_HEADERS + 1):

        line = read_line(stream)

        if line == b"":
            break

        try:
            raw_name, raw_value = line.split(b":", 1)
        except ValueError:
            raise ValueError(f"invalid HTTP header line: {d(line)}") from None

        if not _token_re.fullmatch(raw_name):
            raise ValueError(f"invalid HTTP header name: {d(raw_name)}")

        raw_value = raw_value.strip(b" \t")

        if not _value_re.fullmatch(raw_value):
            raise ValueError(f"invalid HTTP header value: {d(raw_value)}")

        name = raw_name.decode("ascii")  # guaranteed to be ASCII at this point
        value = raw_value.decode("ascii", "surrogateescape")
        headers[name] = value

    else:
        raise websockets.exceptions.SecurityError("too many HTTP headers")

    return headers


def read_line(stream: asyncio.StreamReader) -> bytes:
    """
    Read a single line from ``stream``.

    CRLF is stripped from the return value.

    """
    # Security: this is bounded by the StreamReader's limit (default = 32 KiB).
    line = await stream.readline()
    # Security: this guarantees header values are small (hard-coded = 4 KiB)
    if len(line) > MAX_LINE:
        raise websockets.exceptions.SecurityError("line too long")
    # Not mandatory but safe - https://tools.ietf.org/html/rfc7230#section-3.5
    if not line.endswith(b"\r\n"):
        raise EOFError("line without CRLF")
    return line[:-2]

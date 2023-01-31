# -*- coding: utf-8 -*-


class ClientException(Exception):
    """Base client exception."""


class ClientConnectionTimeout(ClientException):
    """Client connection timeout exception."""


class ClientConnectionError(ClientException):
    """Client connection error exception."""


class ClientHTTPError(ClientException):
    """Client HTTP error exception."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)


class ModuleException(Exception):
    """Base module exception."""


class FileIOError(ModuleException):
    """File IO exception."""


class UnsupportedContentType(ModuleException):
    """Unsupported response content exception."""


class UnsupportedExtension(ModuleException):
    """Unsupported pandas extension exception."""


class JSONDecodeError(ModuleException):
    """JSON decoding exception."""

    def __init__(self, orig: Exception, message: str):
        self.orig = orig
        self.message = message
        super().__init__(self.message)


class BytesDecodeError(ModuleException):
    """Bytes decoding exception."""

    def __init__(self, orig: Exception, message: str):
        self.orig = orig
        self.message = message
        super().__init__(self.message)


class PandasRuntimeError(ModuleException):
    """Pandas runtime exception."""

    def __init__(self, orig: Exception, message: str):
        self.orig = orig
        self.message = message
        super().__init__(self.message)


class UnknownClient(ModuleException):
    """Unknown client exception."""


class ImproperClient(ModuleException):
    """Improper client exception."""


class WebsocketException(Exception):
    """Base websocket exception."""


class WebsocketUnknownEndpoint(WebsocketException):
    """Websocket unknown endpoint exception."""


class WebsocketAuthError(WebsocketException):
    """Websocket authentication exception."""


class WebsocketResponseError(WebsocketException):
    """Websocket response error exception."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

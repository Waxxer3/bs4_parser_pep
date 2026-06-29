class ParserException(Exception):
    """Базовое исключение парсера."""


class ParserFindTagException(ParserException):
    """Не найден тег."""

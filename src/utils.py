from bs4 import BeautifulSoup
from requests import RequestException

from .constants import DEFAULT_ENCODING
from .exceptions import ParserException, ParserFindTagException


def get_response(session, url, encoding=DEFAULT_ENCODING):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ParserException(
            f'Возникла ошибка при загрузке страницы {url}'
        ) from error


def get_soup(session, url, encoding=DEFAULT_ENCODING):
    response = get_response(session, url, encoding)
    return BeautifulSoup(response.text, 'lxml')


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=attrs or {})
    if searched_tag is None:
        raise ParserFindTagException(
            f'Не найден тег {tag} {attrs}'
        )
    return searched_tag

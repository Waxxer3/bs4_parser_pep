import logging
import re
from collections import Counter
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from .configs import configure_argument_parser, configure_logging
from .constants import MAIN_DOC_URL, PEP_URL, EXPECTED_STATUS, BASE_DIR
from .outputs import control_output
from .utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)

        response = get_response(session, version_link)
        if response is None:
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return None

    soup = BeautifulSoup(response.text, 'lxml')

    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(parents=True, exist_ok=True)

    table_tag = soup.find('table')

    if table_tag is None:
        return None

    pdf_a4_tag = table_tag.find(
        'a',
        href=re.compile(r'\.zip$')
    )

    if not pdf_a4_tag:
        return None

    archive_url = urljoin(downloads_url, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    archive_path = downloads_dir / filename

    file_response = get_response(session, archive_url)
    if file_response is None:
        return None

    archive_path.write_bytes(file_response.content)

    return None


def pep(session):
    response = get_response(session, PEP_URL)
    if response is None:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    table_tag = soup.find(
        'table',
        attrs={'class': 'pep-table'}) or soup.find('table')
    tbody_tag = table_tag.find('tbody')
    tr_tags = tbody_tag.find_all('tr')

    status_counter = Counter()
    total = 0

    for tr_tag in tqdm(tr_tags):
        cols = tr_tag.find_all('td')
        if not cols:
            continue

        preview_status = cols[0].text[1:]
        pep_link_tag = cols[1].find('a')
        href = pep_link_tag['href']

        pep_link = urljoin(PEP_URL, href)
        pep_response = get_response(session, pep_link)
        if pep_response is None:
            continue

        pep_soup = BeautifulSoup(pep_response.text, 'lxml')

        dl_tag = pep_soup.find(
            'dl',
            {'class': 'rfc2822 field-list simple'}
        ) or pep_soup.find('dl')

        status = None
        for dt in dl_tag.find_all('dt'):
            if 'Status' in dt.text:
                status_tag = dt.find_next_sibling('dd')
                if status_tag:
                    status = status_tag.get_text(strip=True)
                break

        if not status:
            logging.warning(f'Не удалось определить статус для {pep_link}')
            continue

        expected_statuses = EXPECTED_STATUS.get(preview_status, ())
        if status not in expected_statuses:
            logging.info(
                f'Несовпадающие статусы:\n'
                f'{pep_link}\n'
                f'Статус в карточке: {status}\n'
                f'Ожидаемые статусы: {list(expected_statuses)}'
            )

        status_counter[status] += 1
        total += 1

    results = [('Статус', 'Количество')]
    results.extend(status_counter.items())
    results.append(('Total', total))

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()

    session = requests_cache.CachedSession()

    if args.clear_cache:
        session.cache.clear()

    results = MODE_TO_FUNCTION[args.mode](session)

    if results is not None:
        control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()

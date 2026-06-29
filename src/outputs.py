# outputs.py
import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
    BASE_DIR,
    DATETIME_FORMAT,
    DEFAULT_ENCODING,
    RESULTS_DIR,
    OUTPUT_PRETTY,
    OUTPUT_FILE,
)


def control_output(results, cli_args):
    output = cli_args.output
    if output == OUTPUT_PRETTY:
        pretty_output(results)
    elif output == OUTPUT_FILE:
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(parents=True, exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name

    with open(file_path, 'w', encoding=DEFAULT_ENCODING, newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)

    logging.info('Файл с результатами был сохранён: %s', file_path)

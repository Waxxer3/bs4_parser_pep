# Проект парсинга pep

Парсер документации Python на базе BeautifulSoup.

## Возможности

Проект поддерживает несколько режимов работы:

- `whats-new` — собирает список статей «What's New in Python».
- `latest-versions` — выводит список доступных версий документации Python.
- `download` — скачивает архив документации Python в формате ZIP.
- `pep` — собирает статистику по статусам PEP и проверяет соответствие статусов.

## Используемые технологии

- Python 3.9+
- BeautifulSoup4
- requests-cache
- tqdm
- prettytable

## Установка

Клонируйте репозиторий:

```bash
git clone <ссылка_на_репозиторий>
```

Перейдите в каталог проекта:

```bash
cd bs4_parser_pep
```

Создайте и активируйте виртуальное окружение:

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

### Получить список новых версий Python

```bash
python -m src.main whats-new
```

### Получить список всех версий документации

```bash
python -m src.main latest-versions
```

### Скачать архив документации

```bash
python -m src.main download
```

### Получить статистику по PEP

```bash
python -m src.main pep
```

## Дополнительные параметры

Очистить кэш:

```bash
python -m src.main pep -c
```

Вывести результат в красивой таблице:

```bash
python -m src.main pep -o pretty
```

Сохранить результат в CSV:

```bash
python -m src.main pep -o file
```

## Автор
Waxxer3

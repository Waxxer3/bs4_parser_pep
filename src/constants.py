from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent.parent

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DEFAULT_ENCODING = 'utf-8'

LOG_DIR = 'logs'
RESULTS_DIR = 'results'
DOWNLOADS_DIR = 'downloads'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

LOG_FILE = 'parser.log'

OUTPUT_PRETTY = 'pretty'
OUTPUT_FILE = 'file'

MAX_LOG_SIZE = 1024 * 1024
BACKUP_COUNT = 5

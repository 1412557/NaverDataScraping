import logging
from datetime import datetime

DATE_FORMAT = ["%Y/%m/%d",  "%Y/%m", "%Y-%m-%d", "%Y-%m"]
logger = logging.getLogger(__name__)


def try_parsing_date(text):
    for fmt in DATE_FORMAT:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def clean_up_repo(path):
    import os, shutil
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error('Failed to delete %s. Reason: %s' % (file_path, e))
import os
from datetime import datetime


def zulu_time_now_str():
    return datetime.utcnow().isoformat()[:-3] + "Z"


def create_needed_folders():
    os.makedirs("./.cnl/", exist_ok=True)

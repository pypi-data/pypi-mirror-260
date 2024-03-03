# create tables
# start api
# start periodic

import multiprocessing
from time import sleep

from cnl_engine.cnl_engine_api_app_runner import main as fast_api_app_runner_main
from cnl_engine.db.db_management.create_tables import create_tables
from cnl_engine.periodic_engine_manager import main as periodic_engine_manager_main
from cnl_engine.utils.create_needed_folders import create_needed_folders


def main(path_to_module: str):
    create_needed_folders()
    create_tables()

    # start api
    process = multiprocessing.Process(target=fast_api_app_runner_main)
    process.start()

    # start periodic
    process = multiprocessing.Process(
        target=periodic_engine_manager_main, kwargs={"path_to_module": path_to_module}
    )
    process.start()

    while True:
        sleep(1)

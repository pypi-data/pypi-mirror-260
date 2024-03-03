from cnl_engine.services.engine_related.engine_related import EnginesManager


def main(path_to_module: str):
    EnginesManager(path_to_user_function=path_to_module).run_periodic_task()

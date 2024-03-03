import importlib.util
import multiprocessing
import os

from cnl.config_processing import should_run_telegram
from cnl.types.Config import Config
from cnl_deployment_targets.telegram.main import main as cnl_telegram_main
from cnl_engine.main import main as cnl_engine_main
from cnl_front.main import main as cnl_front_main
from cnl_local.main import main as cnl_local_main
from typing_extensions import Optional


def load_config(config_path: Optional[str]) -> Config:
    if not config_path:
        return "default config"  # type: ignore

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"No such file: '{config_path}'")

    # Load module
    spec = importlib.util.spec_from_file_location("cnl_dynamic.config", config_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module)  # type: ignore

    # Access the variable from the module
    config = getattr(module, "config", None)

    if config is None:
        raise AttributeError(
            f"The module '{config_path}' does not have a 'config' variable."
        )

    return config


def cnl_run(module_path: str, config_path: Optional[str]):
    # load config
    # ask if I should run module + run module
    config = load_config(config_path)
    # run targets
    if should_run_telegram(config):
        process = multiprocessing.Process(
            target=cnl_telegram_main,
            kwargs={"tg_api_key": config["telegram"]["api_key"]},
        )
        process.start()
    # run main of engine
    process = multiprocessing.Process(
        target=cnl_engine_main, kwargs={"path_to_module": module_path}
    )
    process.start()
    # run main of cnl local
    process = multiprocessing.Process(target=cnl_local_main)
    process.start()
    # run main of front
    process = multiprocessing.Process(target=cnl_front_main)
    process.start()

    print("🇨 🇳 🇱  is running..")
    print(f"Chat UI: http://localhost:5007/chat-ui")
    print(f"CNL Local: http://localhost:5007/")

    process.join()

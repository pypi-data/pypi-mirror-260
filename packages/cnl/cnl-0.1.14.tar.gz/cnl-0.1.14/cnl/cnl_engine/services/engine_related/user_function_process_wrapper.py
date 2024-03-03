from cnl_engine.db.repositories.cnl_store import get_store, update_store
from cnl_engine.db.repositories.conversation_history import get_history
from cnl_engine.db.repositories.conversation_meta import get_meta
from cnl_engine.types.common_types import ChatMessage
from typing_extensions import List


def user_function_process_wrapper(
    path_to_user_function_file: str,
    conversation_id: str,
    store_id: str,
) -> ChatMessage:
    history: List[ChatMessage] = get_history(conversation_id)
    # cnl_store = {}
    cnl_store = get_store(store_id)
    # meta = {}
    meta = get_meta(conversation_id)

    import importlib.util

    # Load module
    spec = importlib.util.spec_from_file_location(
        "cnl_dynamic.user_module", path_to_user_function_file
    )
    foo = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(foo)  # type: ignore

    # Access the variable from the module
    reply = foo.main(history, meta, cnl_store)

    # update cnl_store
    update_store(store_id, cnl_store)

    return reply

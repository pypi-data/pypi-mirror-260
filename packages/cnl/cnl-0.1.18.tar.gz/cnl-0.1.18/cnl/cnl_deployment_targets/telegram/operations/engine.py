import httpx
from cnl_deployment_targets.telegram.operations.engine_types import Event
from typing_extensions import List

ENGINE_BASE_URL = "http://localhost:5008"


def add_event(event: Event):
    httpx.post(f"{ENGINE_BASE_URL}/add_event", json=event)


def get_unread_events(conversation_id: str) -> List[Event]:
    return httpx.get(
        f"{ENGINE_BASE_URL}/get_unread_for_front",
        params={"conversation_id": conversation_id},
    ).json()

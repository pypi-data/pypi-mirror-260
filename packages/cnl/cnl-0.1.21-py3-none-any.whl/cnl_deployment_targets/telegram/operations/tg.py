import httpx
from cnl_deployment_targets.telegram.operations.tg_schemas import Update
from typing_extensions import List, Optional

TOKEN = "6595909512:AAGvjv3m_g9sB3oZovrkVhq4bTOvV_wQSZA"
BASE_API_URL = f"https://api.telegram.org/bot{TOKEN}"


def get_updates(offset: Optional[int] = None) -> List[Update]:
    """Fetch new events from tg"""
    params = {"timeout": 100}
    if offset:
        params["offset"] = offset
    response = httpx.get(f"{BASE_API_URL}/getUpdates", params=params, timeout=120.0)
    result = response.json()
    return result["result"]


def send_message(chat_id: int, content: str):
    """Send a message to a chat."""
    data = {"chat_id": chat_id, "text": content}
    response = httpx.post(f"{BASE_API_URL}/sendMessage", data=data)
    return response.json()

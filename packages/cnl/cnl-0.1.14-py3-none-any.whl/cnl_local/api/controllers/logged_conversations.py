from pprint import pprint

from cnl_local.db.repositories.datasets_samples import get_dataset as get_dataset_
from cnl_local.db.repositories.datasets_samples import get_datasets as get_datasets_
from cnl_local.db.repositories.datasets_samples import (
    update_or_create_dataset as update_or_create_dataset_,
)
from cnl_local.db.repositories.logged_conversations import (
    get_logged_conversation as get_logged_conversation_,
)
from cnl_local.db.repositories.logged_conversations import (
    get_logged_conversations as get_logged_conversations_,
)
from cnl_local.db.repositories.logged_conversations import (
    update_or_create_logged_conversation,
)
from cnl_local.types.datasets_samples.Dataset import Dataset
from cnl_local.types.logged_conversations import LoggedConversation
from fastapi import APIRouter, HTTPException
from typing_extensions import List, Optional

router = APIRouter()


@router.post("/log_conversation", tags=["logged_conversations"])
def log_conversation(conversation: LoggedConversation):
    # print(f"Going to write to db:")
    # pprint(conversation)
    update_or_create_logged_conversation(conversation)


@router.get("/logged_conversation", tags=["logged_conversations"])
def get_logged_conversation(conversation_id: str) -> Optional[LoggedConversation]:
    logged_conversation = get_logged_conversation_(conversation_id)
    if not logged_conversation:
        raise HTTPException(status_code=404)
    # print(f"Returning logged conversation:")
    # pprint(logged_conversation)
    return logged_conversation


@router.get("/logged_conversations", tags=["logged_conversations"])
def get_logged_conversations() -> List[LoggedConversation]:
    logged_conversations = get_logged_conversations_()
    return logged_conversations

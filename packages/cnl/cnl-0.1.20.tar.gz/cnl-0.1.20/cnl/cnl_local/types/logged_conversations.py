from typing_extensions import List, Literal, TypedDict

from cnl_local.types.datasets_samples.DatasetSample import DatasetSample


class LoggedConversation(TypedDict):
    conversation_id: str
    last_activity: str
    conversation_history: "ConversationHistory"


ConversationHistory = List["ConversationHistoryMessage"]


class ConversationHistoryMessage(TypedDict):
    message_id: str
    from_: Literal["bot", "user"]
    content: str
    dataset_samples: List[DatasetSample]
    feedback: str
    timestamp: str

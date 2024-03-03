from typing_extensions import List, Literal, TypedDict, Union


class ConversationToRun(TypedDict):
    conversation_id: str
    engine_id: str


class EnginesManagerEngineMeta(TypedDict):
    engine_id: str
    conversation_id: str


##
# Conversation history
##
class LoggedConversation(TypedDict):
    conversation_id: str
    last_activity: str
    conversation_history: "ConversationHistory"


ConversationHistory = List["ConversationHistoryMessage"]


class ConversationHistoryMessage(TypedDict):
    message_id: str
    from_: Literal["bot", "user"]
    content: str
    dataset_samples: List["DataSample"]
    feedback: str
    timestamp: str


##
# Events
##


class UserMessageEvent(TypedDict):
    type: Literal["user-message"]
    conversation_id: str
    message_id: str
    content: str


class BotMessageEvent(TypedDict):
    type: Literal["bot-message"]
    conversation_id: str
    message_id: str
    content: str


class TypingAnimationEvent(TypedDict):
    type: Literal["start-typing-animation"]
    conversation_id: str


# class QuickReplyEvent(TypedDict):
#     type: Literal["quick-reply"]
#     payload: None


Event = UserMessageEvent  # Union[NewMessageEvent]


##
# Datasets
##
class DataSample(TypedDict):
    pass


##
# Cnl
##
# class ChatMessage(TypedDict):
#     type: Literal["text"]
#     content: str
#     data_samples: List[DataSample]
class ChatMessage(TypedDict):
    message_id: str
    from_: Literal["bot", "user"]
    content: str
    dataset_samples: List[DataSample]
    feedback: str
    timestamp: str

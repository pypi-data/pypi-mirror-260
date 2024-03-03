from cnl_engine.types.common_types import (
    ConversationHistory,
    ConversationHistoryMessage,
    DataSample,
)


def update_conversation_history_with_new_message(
    conversation_history: ConversationHistory, message: ConversationHistoryMessage
) -> ConversationHistory:
    conversation_history = conversation_history + [message]
    return conversation_history


def update_conversation_history_with_data_sample(
    conversation_history: ConversationHistory, message_id: str, data_sample: DataSample
):
    for message in conversation_history:
        if message["message_id"] == message_id:
            message["dataset_samples"] = message["dataset_samples"] + [data_sample]
            break
    return conversation_history

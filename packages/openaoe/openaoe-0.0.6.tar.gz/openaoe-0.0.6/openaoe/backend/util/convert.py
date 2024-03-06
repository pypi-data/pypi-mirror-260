from openaoe.backend.model.google import GemmaChatBody
from openaoe.backend.model.openaoe import AoeChatBody, OllamaMessage, OllamaChatBody


def body_convert(body: AoeChatBody):
    target_body = None
    msgs = []
    if "gemma" in body.model:
        for msg in body.messages:
            m = OllamaMessage(role=msg.sender_type if msg.sender_type != 'bot' else "assistant", content=msg.text)
            msgs.append(m)
        last_m = OllamaMessage(role='user', content=body.prompt)
        msgs.append(last_m)
        target_body = GemmaChatBody(
            model="gemma:7b",
            messages=msgs
        )
    elif "mistral" in body.model:
        for msg in body.messages:
            m = OllamaMessage(role=msg.sender_type if msg.sender_type != 'bot' else "assistant", content=msg.text)
            msgs.append(m)
        last_m = OllamaMessage(role='user', content=body.prompt)
        msgs.append(last_m)
        target_body = OllamaChatBody(
            model="mistral",
            messages=msgs
        )
    return target_body

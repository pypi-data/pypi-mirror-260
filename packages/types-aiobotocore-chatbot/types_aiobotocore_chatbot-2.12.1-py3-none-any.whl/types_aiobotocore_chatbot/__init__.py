"""
Main interface for chatbot service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chatbot import (
        Client,
        chatbotClient,
    )

    session = get_session()
    async with session.create_client("chatbot") as client:
        client: chatbotClient
        ...

    ```
"""

from .client import chatbotClient

Client = chatbotClient

__all__ = ("Client", "chatbotClient")

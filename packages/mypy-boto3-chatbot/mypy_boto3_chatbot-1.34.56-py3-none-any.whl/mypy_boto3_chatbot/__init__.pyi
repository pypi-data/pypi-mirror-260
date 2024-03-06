"""
Main interface for chatbot service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chatbot import (
        ChatbotClient,
        Client,
    )

    session = Session()
    client: ChatbotClient = session.client("chatbot")
    ```
"""

from .client import ChatbotClient

Client = ChatbotClient

__all__ = ("ChatbotClient", "Client")

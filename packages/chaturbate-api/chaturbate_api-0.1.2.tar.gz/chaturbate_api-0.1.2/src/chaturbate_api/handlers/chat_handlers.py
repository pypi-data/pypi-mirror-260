"""Handler for chat message event."""

import logging


class ChatMessageEventHandler:
    """Handle chat message event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle chat message event."""
        username = message["object"]["user"]["username"]
        chat_message = message["object"]["message"]["message"]
        logging.info("Chat message from %s: %s", username, chat_message)
        return {
            "event": "chatMessage",
            "username": username,
            "chat_message": chat_message,
        }

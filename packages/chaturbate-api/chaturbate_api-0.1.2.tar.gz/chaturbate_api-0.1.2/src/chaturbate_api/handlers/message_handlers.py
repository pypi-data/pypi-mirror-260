"""Handler for private message event."""

import logging


class PrivateMessageEventHandler:
    """Handle private message event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle private message event."""
        from_user = message["object"]["message"]["fromUser"]
        to_user = message["object"]["message"]["toUser"]
        private_message = message["object"]["message"]["message"]
        logging.info(
            "Private message from %s to %s: %s",
            from_user,
            to_user,
            private_message,
        )
        return {
            "event": "privateMessage",
            "from_user": from_user,
            "to_user": to_user,
            "private_message": private_message,
        }

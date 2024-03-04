"""Media purchase event handler."""

import logging


class MediaPurchaseEventHandler:
    """Handle media purchase event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle media purchase event."""
        username = message["object"]["user"]["username"]
        media_type = message["object"]["media"]["type"]
        media_name = message["object"]["media"]["name"]
        logging.info("%s purchased %s %s", username, media_type, media_name)
        return {
            "event": "mediaPurchase",
            "username": username,
            "media_type": media_type,
            "media_name": media_name,
        }

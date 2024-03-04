"""User event handlers."""

import logging


class UserEnterEventHandler:
    """Handle user enter event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle user enter event."""
        username = message["object"]["user"]["username"]
        logging.info("%s entered the room", username)
        return {
            "event": "userEnter",
            "username": username,
            "message": f"{username} entered the room",
        }


class UserLeaveEventHandler:
    """Handle user leave event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle user leave event."""
        username = message["object"]["user"]["username"]
        logging.info("%s left the room", username)

        return {
            "event": "userLeave",
            "username": username,
            "message": f"{username} left the room",
        }


class FanclubJoinEventHandler:
    """Handle fanclub join event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle fanclub join event."""
        username = message["object"]["user"]["username"]
        logging.info("%s joined the fanclub", username)
        return {
            "event": "fanclubJoin",
            "username": username,
            "message": f"{username} joined the fanclub",
        }

"""Follow event handlers."""

import logging


class FollowEventHandler:
    """Handle follow event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle follow event."""
        username = message["object"]["user"]["username"]
        logging.info("%s has followed", username)
        return {
            "event": "follow",
            "username": username,
            "message": f"{username} has followed",
        }


class UnfollowEventHandler:
    """Handle unfollow event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle unfollow event."""
        username = message["object"]["user"]["username"]
        logging.info("%s has unfollowed", username)
        return {
            "event": "unfollow",
            "username": username,
            "message": f"{username} has unfollowed",
        }

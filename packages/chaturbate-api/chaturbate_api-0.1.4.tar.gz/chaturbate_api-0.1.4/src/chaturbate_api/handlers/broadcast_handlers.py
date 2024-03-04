"""Handlers for broadcast events."""

import logging


class BroadcastStartEventHandler:
    """Handle broadcast start event."""

    @staticmethod
    async def handle() -> dict:
        """Handle broadcast start event."""
        logging.info("Broadcast started")
        return {"event": "broadcastStart", "message": "Broadcast started"}


class BroadcastStopEventHandler:
    """Handle broadcast stop event."""

    @staticmethod
    async def handle() -> dict:
        """Handle broadcast stop event."""
        logging.info("Broadcast stopped")
        return {"event": "broadcastStop", "message": "Broadcast stopped"}

"""Handler for room subject change event."""

import logging


class RoomSubjectChangeEventHandler:
    """Handle room subject change event."""

    @staticmethod
    async def handle(message: dict) -> dict:
        """Handle room subject change event."""
        subject = message["object"]["subject"]
        logging.info("Room subject changed to: %s", subject)
        return {"event": "roomSubjectChange", "subject": subject}

"""Entry point for the Chaturbate API client."""

import asyncio
import logging
import sys

import aiohttp

from chaturbate_api.client import ChaturbateAPIClient
from chaturbate_api.config import Config
from chaturbate_api.event_handlers import event_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

# Get the base URL of the events API
EVENTS_API_URL = Config.get_url()


async def main() -> None:
    """Run the main coroutine for the Chaturbate API client.

    Returns
    -------
        None

    """
    # Initialize aiohttp session
    async with aiohttp.ClientSession() as session:
        # Initialize the Chaturbate API client with the base URL,
        # session, and event handlers
        client = ChaturbateAPIClient(
            base_url=EVENTS_API_URL,
            session=session,
            event_handlers=event_handlers,
        )

        try:
            # Start the client to continuously retrieve and process events
            await client.run()
        except Exception:
            logging.exception("An error occurred")
            sys.exit(1)


if __name__ == "__main__":
    # Run the main coroutine
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

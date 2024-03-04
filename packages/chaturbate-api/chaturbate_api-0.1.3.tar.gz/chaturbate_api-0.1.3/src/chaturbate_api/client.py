"""Module for the Chaturbate API client."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from aiolimiter import AsyncLimiter

from chaturbate_api.exceptions import ChaturbateServerError

from .constants import (
    API_REQUEST_LIMIT,
    API_REQUEST_PERIOD,
    HTTP_CLIENT_ERROR,
    HTTP_SERVER_ERROR,
    HTTP_SUCCESS,
)

if TYPE_CHECKING:
    import aiohttp

logger = logging.getLogger(__name__)


class ChaturbateAPIClient:
    """Chaturbate API Client.

    This class represents a client for retrieving events from the Chaturbate API.
    It provides methods to initialize the client, start the client, and handle events.

    Attributes
    ----------
        base_url (str): The base URL for the API.
        session (aiohttp.ClientSession): The aiohttp client session.
        event_handlers (Dict[str, Any]): A dictionary of event handlers.

    """

    def __init__(
        self: ChaturbateAPIClient,
        base_url: str,
        session: aiohttp.ClientSession,
        event_handlers: dict[str, Any],
    ) -> None:
        """Initialize the Chaturbate API client.

        Args:
        ----
            base_url (str): The base URL for the API.
            session (aiohttp.ClientSession): The aiohttp client session.
            event_handlers (Dict[str, Any]): A dictionary of event handlers.

        """
        self.base_url = base_url
        self.session = session
        self.event_handlers = event_handlers
        self.limiter = AsyncLimiter(API_REQUEST_LIMIT, API_REQUEST_PERIOD)

    async def run(self: ChaturbateAPIClient) -> None:
        """Start the client and continuously retrieve events from the API."""
        logger.debug("Base URL: %s", self.base_url)

        url = self.base_url

        while url:
            events, next_url = await self.get_events(
                url,
            )  # Adjust get_events to return next_url
            await self.process_events(events)
            url = next_url  # Update the URL for the next iteration

    async def get_events(
        self: ChaturbateAPIClient,
        url: str,
    ) -> tuple[list[dict[str, Any]], str | None]:
        """Get events from the Chaturbate API.

        Args:
        ----
            url (str): The URL to get events from.

        Returns:
        -------
            List[Dict[str, Any]]: List of events.
            str: The next URL to get events from.

        Raises:
        ------
            ValueError: If the URL format is invalid.
            ChaturbateServerError: If the server returns an error.
            ValueError: If the server returns an unknown error.

        """
        if not url.startswith("https://events.testbed.cb.dev") and not url.startswith(
            "https://eventsapi.chaturbate.com",
        ):
            msg = "Invalid URL format"
            raise ValueError(msg)
        async with self.limiter:
            async with self.session.get(url) as response:
                if response.status == HTTP_SUCCESS:
                    json_response = await response.json()
                    events = json_response.get("events", [])
                    next_url = json_response.get("nextUrl")
                    return events, next_url
                if response.status >= HTTP_SERVER_ERROR:
                    msg = f"Server error: {response.status}"
                    raise ChaturbateServerError(msg)
                if response.status == HTTP_CLIENT_ERROR:
                    return []
                msg = f"Error: {response.status}"
                raise ValueError(msg)
            return (
                [],
                self.base_url,
            )

    async def process_events(
        self: ChaturbateAPIClient,
        events: list[dict[str, Any]],
    ) -> None:
        """Process events from the Chaturbate API.

        Args:
        ----
            events (List[Dict[str, Any]]): List of events to process.

        Returns:
        -------
            None

        """
        for event in events:
            await self.process_event(event)

    async def process_event(self: ChaturbateAPIClient, event: dict[str, Any]) -> None:
        """Process a single event.

        Args:
        ----
            event (Dict[str, Any]): The event to process.

        Returns:
        -------
            None

        """
        method = event.get("method")
        obj = event.get("object")
        handler_class = self.event_handlers.get(method)
        formatted_obj = json.dumps(obj, indent=4)

        logger.debug("Method: %s\nObject: %s", method, formatted_obj)
        if handler_class:
            handler = handler_class()
            await handler.handle(event)
        else:
            logger.warning("Unknown method: %s", method)

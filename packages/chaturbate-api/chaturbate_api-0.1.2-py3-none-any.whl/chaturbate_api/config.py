"""Configuration for the chaturbate_api package."""

import os

from dotenv import load_dotenv

from chaturbate_api.exceptions import BaseURLNotFoundError

load_dotenv()


class Config:
    """Configuration for the Chaturbate API client."""

    def get_url() -> str:
        """Get the base URL of the events API.

        Returns
        -------
            str: The base URL of the events API.

        Raises
        ------
            BaseURLNotFoundError: If the base URL is not found.

        """
        events_api_url = os.getenv("EVENTS_API_URL")
        if events_api_url is None:
            raise BaseURLNotFoundError
        return events_api_url

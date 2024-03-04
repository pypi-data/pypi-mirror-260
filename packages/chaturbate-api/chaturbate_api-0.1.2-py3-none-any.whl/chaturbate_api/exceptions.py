"""Module with custom exceptions for the Chaturbate API."""


class BaseURLNotFoundError(Exception):
    """Raised when the base URL of the events API is not found."""

    def __init__(self: "BaseURLNotFoundError") -> None:
        """Initialize the exception."""
        msg_error = "Base URL not found."
        msg_solution = "Set the EVENTS_API_URL environment variable and try again."
        formatted_msg = f"{msg_error}\n{msg_solution}"
        super().__init__(formatted_msg)


class ChaturbateServerError(Exception):
    """Raised when the Chaturbate API returns a server error."""

    def __init__(self: "ChaturbateServerError", status_code: int) -> None:
        """Initialize the exception.

        Parameters
        ----------
        status_code : int
            The status code of the server response.

        """
        super().__init__(f"Chaturbate API server error: {status_code}")

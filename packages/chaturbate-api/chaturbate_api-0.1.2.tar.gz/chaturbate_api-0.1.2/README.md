# Chaturbate API Integration

This project provides an integration with the Chaturbate API, allowing for the polling of various events such as broadcast starts, user entries, and more. It uses async for event handling.

## Features

- Polling Chaturbate API for real-time events
- Handling of various event types, including broadcast starts/stops, user entries/exits, follows/unfollows, chat messages, and tips
- Extensible event handling system

### Installation

Ensure you have Python 3.8+ installed on your machine. Then, you can install the package and its dependencies using the following command:

```
pip install chaturbate_api
```

### Set Up

To use this integration, you'll need to set up your environment with the necessary API URL. Create a `.env` file in the root directory with the following content:

```
EVENTS_API_URL=https://eventsapi.chaturbate.com/events/user_name/api_key
```

> [!NOTE]
> Replace `https://eventsapi.chaturbate.com/events/user_name/api_key` with the actual API URL provided by Chaturbate.

### Usage

To start the application, run:

```
python -m chaturbate_api
```

This will initiate the polling process, and you'll begin receiving events based on the configured handlers.

### Development

To contribute to this project or modify it for your needs, clone the repository and run tests to ensure your modifications don't break existing functionality:


```
git clone -r https://github.com/MountainGod2/chaturbate_api.git
```

```
pip install pytest
cd chaturbate_api/
pytest .
```

### License

This project is licensed under the MIT License - see the LICENSE file for details.


import logging
import tempfile

import requests

from . import utils


class TelegramHandler(logging.Handler):
    """
    A custom logging handler that uses the Telegram Bot API to send logs to a chat.

    :param token: The Telegram Bot API token.
    :param chat: The chat ID to send the logs to.
    :param message: The optional message to send along with the logs.
    :param file_name: The name of the file to send.
                      If not provided, defaults to "traceback.html".
    """

    def __init__(self, token, chat, **kwargs):
        super().__init__()
        self.token = token
        self.chat = chat
        self.message = kwargs.get("message", "")

        # Set file name
        file_name = kwargs.get("file_name", "traceback.html")
        if not file_name.endswith(".html"):
            file_name += ".html"

        self.file_name = file_name

    def emit(self, record):
        html = utils.retrieve_traceback_html(record)

        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(html.encode())
            temp_file.seek(0)

            # Send message
            requests.post(
                url=f"https://api.telegram.org/bot{self.token}/sendDocument",
                data={"chat_id": self.chat, "caption": self.message},
                files={"document": (self.file_name, temp_file, "text/html")},
                timeout=10,
            )

from pathlib import Path

from mmpy_bot_mk2.bot import Bot
from mmpy_bot_mk2.function import (
    MessageFunction,
    WebHookFunction,
    listen_to,
    listen_webhook,
)
from mmpy_bot_mk2.plugins import ExamplePlugin, Plugin, WebHookExample
from mmpy_bot_mk2.scheduler import schedule
from mmpy_bot_mk2.settings import Settings
from mmpy_bot_mk2.wrappers import ActionEvent, Message, WebHookEvent

__version__ = Path(__file__).parent.joinpath("version.txt").read_text().rstrip()

__all__ = [
    "__version__",
    "Bot",
    "MessageFunction",
    "WebHookFunction",
    "listen_to",
    "listen_webhook",
    "ExamplePlugin",
    "Plugin",
    "WebHookExample",
    "schedule",
    "Settings",
    "ActionEvent",
    "Message",
    "WebHookEvent",
]

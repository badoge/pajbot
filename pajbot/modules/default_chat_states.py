from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import logging

from pajbot.managers.handler import HandlerManager
from pajbot.modules import BaseModule, ModuleSetting

if TYPE_CHECKING:
    from pajbot.bot import Bot

log = logging.getLogger(__name__)


class DefaultChatStatesModule(BaseModule):
    ID = __name__.rsplit(".", maxsplit=1)[-1]
    NAME = "Default Chat States"
    DESCRIPTION = "Enforces certain chat states when the streamer goes online/offline"
    CATEGORY = "Moderation"
    ENABLED_DEFAULT = False
    ONLINE_PHRASE = "Goes Online"
    OFFLINE_PHRASE = "Goes Offline"
    NEVER_PHRASE = "Never"
    PHRASE_OPTIONS = [ONLINE_PHRASE, OFFLINE_PHRASE, NEVER_PHRASE]
    SETTINGS = [
        ModuleSetting(
            key="emoteonly",
            label="Enable emote only mode when the stream...",
            type="options",
            required=True,
            default=NEVER_PHRASE,
            options=PHRASE_OPTIONS,
        ),
        ModuleSetting(
            key="subonly",
            label="Enable subscriber only mode when the stream...",
            type="options",
            required=True,
            default=NEVER_PHRASE,
            options=PHRASE_OPTIONS,
        ),
        ModuleSetting(
            key="r9k",
            label="Enable R9K mode when the stream...",
            type="options",
            required=True,
            default=NEVER_PHRASE,
            options=PHRASE_OPTIONS,
        ),
        ModuleSetting(
            key="slow_option",
            label="Enable slow mode when the stream...",
            type="options",
            required=True,
            default=NEVER_PHRASE,
            options=PHRASE_OPTIONS,
        ),
        ModuleSetting(
            key="slow_time",
            label="Amount of seconds to use when setting slow mode",
            type="number",
            required=True,
            placeholder="30",
            default=30,
            constraints={"min_value": 1, "max_value": 1800},
        ),
        ModuleSetting(
            key="followersonly_option",
            label="Enable followers only mode when the stream...",
            type="options",
            required=True,
            default=NEVER_PHRASE,
            options=PHRASE_OPTIONS,
        ),
        ModuleSetting(
            key="followersonly_time",
            label="Amount of time to use when setting followers only mode | Format is number followed by time format. E.g. 30m, 1 week, 5 days 12 hours",
            type="text",
            required=False,
            placeholder="",
            default="",
            constraints={},
        ),
    ]

    def __init__(self, bot: Optional[Bot]) -> None:
        super().__init__(bot)

    def on_stream_start(self, **rest) -> bool:
        if self.bot is None:
            log.warning("on_stream_start failed in DefaultChatStatesModule because bot is None")
            return True

        if self.settings["emoteonly"] == self.ONLINE_PHRASE:
            self.bot.privmsg(".emoteonly")

        if self.settings["subonly"] == self.ONLINE_PHRASE:
            self.bot.privmsg(".subonly")

        if self.settings["r9k"] == self.ONLINE_PHRASE:
            self.bot.privmsg(".uniquechat")

        if self.settings["slow_option"] == self.ONLINE_PHRASE:
            self.bot.privmsg(f".slow {self.settings['slow_time']}")

        if self.settings["followersonly_option"] == self.ONLINE_PHRASE:
            if self.settings["followersonly_time"] == "":
                self.bot.privmsg(".followers")
            else:
                self.bot.privmsg(f".followers {self.settings['followersonly_time']}")

        return True

    def on_stream_stop(self, **rest) -> bool:
        if self.bot is None:
            log.warning("on_stream_stop failed in DefaultChatStatesModule because bot is None")
            return True

        if self.settings["emoteonly"] == self.OFFLINE_PHRASE:
            self.bot.privmsg(".emoteonly")

        if self.settings["subonly"] == self.OFFLINE_PHRASE:
            self.bot.privmsg(".subonly")

        if self.settings["r9k"] == self.OFFLINE_PHRASE:
            self.bot.privmsg(".uniquechat")

        if self.settings["slow_option"] == self.OFFLINE_PHRASE:
            self.bot.privmsg(f".slow {self.settings['slow_time']}")

        if self.settings["followersonly_option"] == self.OFFLINE_PHRASE:
            if self.settings["followersonly_time"] == "":
                self.bot.privmsg(".followers")
            else:
                self.bot.privmsg(f".followers {self.settings['followersonly_time']}")

        return True

    def enable(self, bot: Optional[Bot]) -> None:
        HandlerManager.add_handler("on_stream_start", self.on_stream_start)
        HandlerManager.add_handler("on_stream_stop", self.on_stream_stop)

    def disable(self, bot: Optional[Bot]) -> None:
        HandlerManager.remove_handler("on_stream_start", self.on_stream_start)
        HandlerManager.remove_handler("on_stream_stop", self.on_stream_stop)

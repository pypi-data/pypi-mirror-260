"""
Module for handling GitHub check_run webhook events.
https://docs.github.com/en/webhooks/webhook-events-and-payloads#check_run
"""

from github.CheckRun import CheckRun

from githubapp.events.event import Event


class CheckRunEvent(Event):
    """This class represents an check run event."""

    event_identifier = {"event": "check_run"}

    def __init__(
        self,
        check_run,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.check_run = self._parse_object(CheckRun, check_run)


class CheckRunCompletedEvent(CheckRunEvent):
    """This class represents an check run completed event."""

    event_identifier = {"action": "completed"}

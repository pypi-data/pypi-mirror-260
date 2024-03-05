from __future__ import annotations


class WorkstreamError(Exception):
    def __init__(
        self, *args: object, title: str | None = None, help_text: str | None = None
    ) -> None:
        self.title = title
        self.help_text = help_text
        super().__init__(*args)


class dbtFailure(Exception):
    pass

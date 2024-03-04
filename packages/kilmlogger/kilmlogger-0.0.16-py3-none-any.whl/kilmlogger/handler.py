import sys

from logging import Handler, LogRecord

from kilmlogger.services.scribe.client import ScribeBaseClient, DefaultScribeClient
from kilmlogger.constants import ACCEPTED_LEVELS


class GRPCEventStreamingHandler(Handler):
    def __init__(self, client: ScribeBaseClient = DefaultScribeClient()):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        Handler.__init__(self)
        self._client = client

    def emit(self, record: LogRecord) -> None:
        # NOTE: Only sent log to scribe and DP if the log level is in ACCEPTED_LEVELS
        if record.levelname not in ACCEPTED_LEVELS:
            return

        self.acquire()
        try:
            self._client.log(
                msg=record.msg,
            )
        except Exception:
            sys.stdout.write("--- Logging error ---\n")
        finally:
            self.release()

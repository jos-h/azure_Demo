import datetime
import logging
import os
import traceback

import pytz
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient


class AzureLogAnalyticsHandler(logging.Handler):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.dcr_endpoint = os.getenv("LOGS_INGESTION_ENDPOINT")
        self.dcr_immutableid = os.getenv("DCR_IMMUTABLEID")
        self.stream_name = os.getenv("STREAM_NAME")
        self.credential = DefaultAzureCredential()
        self.client = LogsIngestionClient(
            endpoint=self.dcr_endpoint, credential=self.credential, logging_enable=True
        )

    def formatException(self, exec_info) -> DefaultAzureCredential:
        return traceback.format_exception(exec_info)

    def emit(self, record):
        """
        Sends the log record to the Azure Log Analytics workspace.

        Args:
            record (logging.LogRecord): The log record to be sent.
        """
        # Create the log message dictionary
        log_message = {
            "TimeGenerated": datetime.datetime.now(tz=pytz.UTC).isoformat(),
            "Level": record.levelname,
            "Logger": record.name,
            "Msg": record.getMessage(),
            "message": record.getMessage(),
        }

        if record.exc_info is not None:
            if isinstance(record.exc_info[1], Exception):
                log_message["message"] = self.formatException(record.exc_info[1])

        try:
            self.client.upload(
                rule_id=self.dcr_immutableid,
                stream_name=self.stream_name,
                logs=[log_message],
            )
        except HttpResponseError as e:
            print(f"Error sending log to Azure Log Analytics: {e}")

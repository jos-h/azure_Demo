import datetime
import logging
import os
import traceback

import pytz
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

def get_client_credential():
    if os.getenv("LOGS_INGESTION_ENDPOINT") and os.getenv("USE_AZURE_LOG"):
        credential = DefaultAzureCredential()
        client = LogsIngestionClient(
            endpoint=os.getenv("LOGS_INGESTION_ENDPOINT"),
            credential=credential,
            logging_enable=True,
        )
        return client, credential
    return None, None


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
        self.client, self.credential = get_client_credential()

        self._console_handler = logging.StreamHandler()
        self._console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s"
            )
        )

    def formatException(self, exec_info) -> DefaultAzureCredential:
        return traceback.format_exception(exec_info)

    def emit(self, record):
        """
        Sends the log record to the Azure Log Analytics workspace if enabled else
        log the record onto console
        Args:
            record (logging.LogRecord): The log record to be sent.
        """
        try:
            if self.client and self.credential:
                # Create the log message dictionary
                log_message = {
                    "TimeGenerated": datetime.datetime.now(tz=pytz.UTC).isoformat(),
                    "Level": record.levelname,
                    "Logger": record.name,
                    "Msg": record.getMessage(),
                    "message": record.getMessage(),
                }
                self.client.upload(
                    rule_id=os.getenv("DCR_IMMUTABLEID"),
                    stream_name=os.getenv("STREAM_NAME"),
                    logs=[log_message],
                )
            else:
                self._console_handler.emit(record)
        except HttpResponseError as e:
            print(f"Error sending log to Azure Log Analytics: {e}")

from adapters.input.local_storage_adapter import LocalReaderAdapter
from adapters.input.s3_storage_adapter import S3ReaderAdapter
from config.settings import Settings
from config.logging import logging


class InputAdapterFactory:
    @staticmethod
    def create_input_adapter():
        if Settings.STORAGE_TYPE == "S3":
            return S3ReaderAdapter(
                Settings.AWS_ACCESS_KEY_ID,
                Settings.AWS_SECRET_ACCESS_KEY,
                Settings.AWS_REGION,
                Settings.AWS_SESSION_TOKEN,
            )
        elif Settings.STORAGE_TYPE == "LOCAL":
            return LocalReaderAdapter()
        else:
            error = f"Unsupported STORAGE_TYPE: {Settings.STORAGE_TYPE}"
            logging.error(error)
            raise ValueError(error)

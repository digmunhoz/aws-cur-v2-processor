from adapters.output.elasticsearch_adapter import ElasticsearchWriterAdapter
from adapters.output.opensearch_adapter import OpensearchWriterAdapter
from config.settings import Settings
from config.logging import logging


class OutputAdapterFactory:
    @staticmethod
    def create_output_adapter():
        if Settings.OUTPUT_ADAPTER == "elasticsearch":
            return ElasticsearchWriterAdapter(
                host=Settings.OUTPUT_ADAPTER_HOST, port=Settings.OUTPUT_ADAPTER_PORT
            )
        elif Settings.OUTPUT_ADAPTER == "opensearch":
            return OpensearchWriterAdapter(
                host=Settings.OUTPUT_ADAPTER_HOST, port=Settings.OUTPUT_ADAPTER_PORT
            )
        else:
            error = f"Unsupported OUTPUT_ADAPTER: {Settings.OUTPUT_ADAPTER}"
            logging.error(error)
            raise ValueError(error)

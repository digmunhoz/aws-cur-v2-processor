import hashlib
from datetime import datetime

from config.settings import Settings

class DataValidator:
    def validate(self, data):
        return True


class DataTransformer:
    def clean_item(self, item):
        # Replaces NaN to 0
        return {
            k: (0 if (isinstance(v, float) and v != v) else v)
            for k, v in item.items()
        }

    def transform(self, data):

        bulk_data = []
        index_suffix = self.gen_index_suffix(data[0])
        index_name = f"{Settings.INDEX_NAME}{index_suffix}"
        for document in data:
            cleaned_document = self.clean_item(document)
            doc_hash_id = self.gen_hash(cleaned_document)
            action = {
                "_op_type": "index",
                "_index": index_name,
                "_id": doc_hash_id,
                "_source": cleaned_document,
            }
            bulk_data.append(action)
        return bulk_data

    def gen_hash(self, document):
        hash_string = str(document["line_item_usage_start_date"])
        fields = [
            "bill_payer_account_id",
            "identity_line_item_id",
            "line_item_usage_account_id",
        ]

        for field in fields:
            value = document.get(field)
            if value:
                hash_string += value

        generated_id = hashlib.sha256(hash_string.encode("utf-8")).hexdigest()

        return generated_id

    def gen_index_suffix(self, document):
        date_field = document["line_item_usage_start_date"]
        timestamp = date_field.timestamp()
        date_obj = datetime.fromtimestamp(timestamp)
        index_suffix = date_obj.strftime("%Y-%m")
        return str(index_suffix)

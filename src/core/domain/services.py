import hashlib
from datetime import datetime

class DataValidator:
    def validate(self, data):
        return True

class DataTransformer:
    def clean_item(self, item):
        # Replaces NaN to None
        return {k: (None if (isinstance(v, float) and v != v) else v) for k, v in item.items()}

    def transform(self, data):

        bulk_data = []
        index_suffix = self.gen_index_suffix(data[0])
        index_name = f"aws-cur-v2_{index_suffix}"
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
        dt_field = document["line_item_usage_start_date"]
        timestamp = dt_field.timestamp()
        hash_string = str(timestamp)
        fields = ["bill_payer_account_id", "identity_line_item_id", "line_item_usage_account_id", "product_sku"]

        for field in fields:
            value = document.get(field)
            if value:
                hash_string += value
        return hashlib.sha256(hash_string.encode("utf-8")).hexdigest()

    def gen_index_suffix(self, document):
        date_field = document["line_item_usage_start_date"]
        timestamp = date_field.timestamp()
        date_obj = datetime.fromtimestamp(timestamp)
        index_suffix = date_obj.strftime('%Y-%m')
        return str(index_suffix)
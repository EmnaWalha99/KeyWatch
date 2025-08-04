from config.db import get_transactions_collection
from dataAccess.counting_transactions import get_distinct_counts, get_velocity_counts

from extractors.extract_sender_info import extract_sender_info
from extractors.extract_location_info import (
    extract_ip_info,
    extract_country_mismatch,
    extract_impossible_travel,
    extract_frequent_timezone_switch,
)
from extractors.extract_time_info import extract_day, extract_late_hour
from extractors.extract_card_and_payment_info import (
    extract_pan_info,
    extract_amount,
    extract_fee_rate,
    extract_avg_amount_last_7d
)
from extractors.extract_status import extract_status, extract_many_failed_attempts
from extractors.extract_merchant_domain import extract_merchant_domain


class FeatureExtractor:
    def __init__(self, collection=None):
        self.collection = collection or get_transactions_collection()

        # extracteurs synchrones
        self.sync_extractors = [
            extract_sender_info,
            extract_ip_info,
            extract_amount,
            extract_merchant_domain,
            extract_late_hour,
            extract_day,
            extract_status,
            extract_country_mismatch,
            extract_fee_rate,
            extract_pan_info,
        ]

        #extracteurs asynchrones
        self.async_extractors = [
            extract_many_failed_attempts,
        ]

    async def extract_features(self, trnx_data: dict) -> dict:
        features = {}

        # Appeler extracteurs synchrones
        for extractor in self.sync_extractors:
            try:
                result = extractor(trnx_data)
                features.update(result)
            except Exception as e:
                print(f"[ERROR] {extractor.__name__} failed: {e}")

        for extractor in self.async_extractors:
            try:
                result = await extractor(trnx_data)
                features.update(result)
            except Exception as e:
                print(f"[ERROR] {extractor.__name__} failed: {e}")

        try:
            features.update(await extract_impossible_travel(trnx_data, collection=self.collection))
            features.update(await extract_avg_amount_last_7d(trnx_data, collection=self.collection))
            features.update(await extract_frequent_timezone_switch(trnx_data, collection=self.collection, n=3, threshold=2))
            features.update(await get_velocity_counts(trnx_data, collection=self.collection))
            features.update(await get_distinct_counts(trnx_data, collection=self.collection))
        except Exception as e:
            print(f"[ERROR] Special extractor failed: {e}")

        return features

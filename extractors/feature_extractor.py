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
from extractors.extract_status import extract_status
from extractors.extract_merchant_domain import extract_merchant_domain


class FeatureExtractor:
    def __init__(self, collection=None):
        self.collection = collection if collection is not None else get_transactions_collection()

        self.extractors = [
            extract_sender_info,
            extract_ip_info,
            extract_amount,
            extract_merchant_domain,
            extract_late_hour,
            extract_day,
            extract_status,
            extract_country_mismatch,
            #extract_impossible_travel,
            extract_fee_rate,
            extract_pan_info,
        ]

    def extract_features(self, trnx_data: dict) -> dict:
        features = {}

        # simple extractors
        for extractor in self.extractors:
            try:
                features.update(extractor(trnx_data))
            except Exception as e:
                print(f"[ERROR] {extractor.__name__} failed: {e}")

        # extractors that need collection or special args
        try:
            features.update(extract_impossible_travel(trnx_data , collection = self.collection))
            features.update(extract_avg_amount_last_7d(trnx_data,collection = self.collection))
            features.update(
                extract_frequent_timezone_switch(
                    trnx_data, collection=self.collection, n=3, threshold=2
                )
            )
            features.update(get_velocity_counts(trnx_data, collection=self.collection))
            features.update(get_distinct_counts(trnx_data))
        except Exception as e:
            print(f"[ERROR] Special extractor failed: {e}")

        return features

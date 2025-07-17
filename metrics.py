from prometheus_client import Counter, Histogram, Summary

#system metrics
REQUEST_COUNT = Counter("request_count", "Total number of HTTP requests")
EXCEPTION_COUNT= Counter("exception_count" , "Total number of unhandled exceptions")
REQUEST_DURATION= Histogram("request_duration_seconds","Histogram of request duration")

# fraud detection metrics
TRANSACTION_COUNT = Counter("transaction_total","Total number of transactions processed")
FEATURE_EXTRACTION_TIME=Summary("feature_extraction_duration_seconds","Time taken to extract features")


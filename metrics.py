from prometheus_client import Counter, Histogram, Summary , Gauge
import psutil
import time 
from threading import Thread
import threading

#cpu and memory usage 
CPU_USAGE= Gauge("system_cpu_usage_percent","CPU usage percentage")
MEMORY_USAGE= Gauge("system_memory_usage_percent","Memory usage percentage")
UPTIME = Gauge("uptime_seconds", "Uptime of the service in seconds")
THREAD_COUNT = Gauge("system_thread_count", "Number of active threads")
DISK_USAGE = Gauge("system_disk_usage_percent", "Disk usage percentage")
PROCESS_RSS_MB = Gauge("system_process_rss_mb", "Memory usage (RSS) of this process in MB")


#system metrics
REQUEST_COUNT = Counter("request_count", "Total number of HTTP requests")
EXCEPTION_COUNT= Counter("exception_count" , "Total number of unhandled exceptions")
REQUEST_DURATION= Histogram("request_duration_seconds","Histogram of request duration")

# fraud detection metrics
TRANSACTION_COUNT = Counter("transaction_total","Total number of transactions processed")
FEATURE_EXTRACTION_TIME=Summary("feature_extraction_duration_seconds","Time taken to extract features")


#internal timer
START_TIME=time.time()

def monitor_system_metrics():
    while True:
        try:
            CPU_USAGE.set(psutil.cpu_percent(interval=1))
            MEMORY_USAGE.set(psutil.virtual_memory().percent)
            UPTIME.set(time.time()- START_TIME)
            THREAD_COUNT.set(threading.active_count())
            DISK_USAGE.set(psutil.disk_usage('/').percent)
            PROCESS_RSS_MB.set(psutil.Process().memory_info().rss / 1024 / 1024)
        except Exception as e : 
            print(f"[Monitoring Error] {e}")
        time.sleep(5)
        
# start background monitoring
Thread(target=monitor_system_metrics , daemon=True).start()
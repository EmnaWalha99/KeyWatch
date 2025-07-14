from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from dateutil.parser import isoparse

def extract_late_hour(data):
        try:
            utc_paid_at = data.get("paidAt", {}).get("$date", None)
            tz = data.get("senderIpInformation", {}).get("timezone", "UTC")

            print(f"[DEBUG] Raw paidAt: {utc_paid_at}")
            print(f"[DEBUG] Timezone: {tz}")

            if not utc_paid_at:
                raise ValueError("paidAt['$date'] is missing")

            dt_utc = isoparse(utc_paid_at).replace(tzinfo=timezone.utc)
            print(f"[DEBUG] UTC datetime: {dt_utc}")

            # Fallback to UTC if timezone is invalid
            try:
                dt_local = dt_utc.astimezone(ZoneInfo(tz))
            except Exception as tz_err:
                print(f"[WARN] Invalid timezone '{tz}', using UTC. Error: {tz_err}")
                dt_local = dt_utc

            print(f"[DEBUG] Local datetime: {dt_local}")

            hour = dt_local.hour
            return {
                "local_hour": hour,
                "is_late_night": 1 if 1 <= hour <= 5 else 0
            }

        except Exception as e:
            print("[ERROR] Late hour extraction failed:", e)
            return {
                "local_hour": None,
                "is_late_night": 0
            }
            
def extract_day(data):
        try:
            utc_paid_at = data.get("paidAt", {}).get("$date", None)
            if not utc_paid_at:
                raise ValueError("paidAt['$date'] is missing")
            dt_utc = isoparse(utc_paid_at).replace(tzinfo=timezone.utc)
            day_of_week = dt_utc.weekday()  # 0=lundi, 6=dimanche
            is_weekend = 1 if day_of_week >= 5 else 0  # 5=samedi, 6=dimanche
            return {
                "day_of_week": day_of_week,
                "is_weekend": is_weekend
            }
        except Exception as e:
            print("[ERROR] Day extraction failed:", e)
            return {
                "day_of_week": None,
                "is_weekend": 0
            }
            
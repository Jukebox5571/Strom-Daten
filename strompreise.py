import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# API-URL
url = "https://api.awattar.de/v1/marketdata"

# Zeitraum: heutiger Tag (00:00 bis 23:00)
now = datetime.now()
start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
end_time = start_time + timedelta(days=1)

params = {
    "start": int(start_time.timestamp() * 1000),
    "end": int(end_time.timestamp() * 1000)
}

response = requests.get(url, params=params)
data = response.json().get("data", [])

records = []
for item in data:
    start = datetime.fromtimestamp(item["start_timestamp"] / 1000)
    preis_ct_kwh = round(item["marketprice"] / 10, 2)

    records.append({
        "timestamp": start.strftime("%Y-%m-%d %H:%M:%S"),
        "preis_ct_kwh": preis_ct_kwh
    })

# Datei anhängen oder neu erstellen
filename = "strompreise_awattar.csv"
df_new = pd.DataFrame(records)

if os.path.exists(filename):
    df_existing = pd.read_csv(filename)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset="timestamp")
else:
    df_combined = df_new

df_combined.to_csv(filename, index=False)

# Parses all .fit dive log files exported from Suunto Ocean diving computer into a single CSV file (data/dives_parsed.csv) for further analysis.

import fitparse
import pandas as pd
import os

def parse_dive(filepath):
    fitfile = fitparse.FitFile(filepath)
    
    summary = {
        "file": os.path.basename(filepath),
        "date": None,
        "max_depth": None,
        "duration": None,
        "avg_temperature": None,
        "min_temperature": None,
    }
    
    for record in fitfile.get_messages("session"):
        for field in record:
            name = field.name
            value = field.value
            if name == "start_time": summary["date"] = value
            elif name == "max_depth": summary["max_depth"] = value
            elif name == "total_elapsed_time": summary["duration"] = value
            elif name == "avg_temperature": summary["avg_temperature"] = value
            elif name == "min_temperature": summary["min_temperature"] = value

    return summary

# --- Run ---
data_folder = "data/"
records = []

for fname in sorted(os.listdir(data_folder)):
    if fname.endswith(".fit"):
        try:
            records.append(parse_dive(os.path.join(data_folder, fname)))
        except Exception as e:
            print(f"Failed to parse {fname}: {e}")

df = pd.DataFrame(records)
df.to_csv("data/dives_parsed.csv", index=False)
print(f"Parsed {len(df)} dives successfully.")
print(df[["file", "date", "max_depth", "duration"]].head())
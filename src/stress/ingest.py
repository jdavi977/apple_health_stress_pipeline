# HeartRateVariabilitySDNN, RestingHeartRate, HeartRate for MVP

# HKQuantityTypeIdentifierHeartRateVariabilitySDNN
# HKQuantityTypeIdentifierRestingHeartRate
# HKQuantityTypeIdentifierHeartRate

import os
import xml.etree.ElementTree as ET

import pandas as pd

FEATURES = [
    "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
    "HKQuantityTypeIdentifierRestingHeartRate",
    "HKQuantityTypeIdentifierHeartRate",
]

RECORD_ATTRS = [
    "type",
    "sourceName",
    "sourceVersion",
    "device",
    "unit",
    "creationDate",
    "startDate",
    "endDate",
    "value",
]

DATE_COLS = ["creationDate", "startDate", "endDate"]


def extract_stress_features(dataset, output_dir="data/interim"):

    os.makedirs(output_dir, exist_ok=True)

    rows = {feature: [] for feature in FEATURES}

    # Stream the export instead of loading the whole tree into memory
    for _, elem in ET.iterparse(dataset, events=("end",)):
        if elem.tag == "Record":
            feature = elem.get("type")
            if feature in rows:
                rows[feature].append({attr: elem.get(attr) for attr in RECORD_ATTRS})
            elem.clear()

    for feature, records in rows.items():
        df = pd.DataFrame(records, columns=RECORD_ATTRS)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        for col in DATE_COLS:
            # Offsets shift with DST, so normalize everything to UTC
            df[col] = pd.to_datetime(df[col], format="%Y-%m-%d %H:%M:%S %z", utc=True)

        output_path = os.path.join(output_dir, f"{feature}.parquet")
        df.to_parquet(output_path, index=False)

def main():
    extract_stress_features("data/raw/export.xml")

if __name__ == "__main__":
    main()

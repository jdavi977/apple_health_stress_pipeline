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

# Only heart rate records carry this: 0 = not set, 1 = sedentary, 2 = active
MOTION_CONTEXT_KEY = "HKMetadataKeyHeartRateMotionContext"


def extract_stress_features(dataset, output_dir="data/interim"):

    os.makedirs(output_dir, exist_ok=True)

    rows = {feature: [] for feature in FEATURES}

    # Stream the export instead of loading the whole tree into memory
    for _, elem in ET.iterparse(dataset, events=("end",)):
        if elem.tag == "Record":
            feature = elem.get("type")
            if feature in rows:
                row = {attr: elem.get(attr) for attr in RECORD_ATTRS}
                entry = elem.find(f"MetadataEntry[@key='{MOTION_CONTEXT_KEY}']")
                row["motionContext"] = entry.get("value") if entry is not None else None
                rows[feature].append(row)
            elem.clear()

    for feature, records in rows.items():
        df = pd.DataFrame(records, columns=RECORD_ATTRS + ["motionContext"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["motionContext"] = pd.to_numeric(df["motionContext"], errors="coerce").astype("Int64")
        for col in DATE_COLS:
            # Offsets shift with DST, so normalize everything to UTC
            df[col] = pd.to_datetime(df[col], format="%Y-%m-%d %H:%M:%S %z", utc=True)

        output_path = os.path.join(output_dir, f"{feature}.parquet")
        df.to_parquet(output_path, index=False)

def main():
    extract_stress_features("data/raw/export.xml")

if __name__ == "__main__":
    main()

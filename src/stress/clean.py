import pandas as pd
import os
import duckdb
from tzlocal import get_localzone_name

os.makedirs("data/processed", exist_ok=True)
con = duckdb.connect("data/processed/stress.duckdb")

FILES = [
        "data/interim/HKQuantityTypeIdentifierHeartRateVariabilitySDNN.parquet",
        "data/interim/HKQuantityTypeIdentifierRestingHeartRate.parquet",
        "data/interim/HKQuantityTypeIdentifierHeartRate.parquet"
    ]

GENERAL_COLUMNS = ["sourceVersion","startDate", "endDate", "value"]

LOCAL_TZ = get_localzone_name()

def clean_data(df):
    table_name = df["type"].loc[0]

    # Adds the general columnns to a cleaned dataframe
    clean = df[GENERAL_COLUMNS].copy()
    # Local date each record starts on (DuckDB stores timestamps as UTC, so
    # converted timestamp columns would be identical to the originals)
    clean["local_date"] = clean["startDate"].dt.tz_convert(LOCAL_TZ).dt.date

    if (table_name == "HKQuantityTypeIdentifierRestingHeartRate"):
        # A day can have more than one record, keep the latest-created one
        clean["creationDate"] = df["creationDate"]
        clean = clean.sort_values(["creationDate", "endDate"])
        clean = clean.drop_duplicates(subset="local_date", keep="last")
        clean = clean.sort_values("startDate")

    elif (table_name == "HKQuantityTypeIdentifierHeartRate"):
        # 0 = not set, 1 = sedentary, 2 = active
        clean["motionContext"] = df["motionContext"]
    
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM clean")


def load_parquet(file_path):
    df = pd.read_parquet(file_path)
    return df

def main():
    for file in FILES:
        df = load_parquet(file)
        clean_data(df)
    con.close()

if __name__ == "__main__":
    main()
# HeartRateVariabilitySDNN, RestingHeartRate, HeartRate for MVP

# HKQuantityTypeIdentifierHeartRateVariabilitySDNN
# HKQuantityTypeIdentifierRestingHeartRate
# HKQuantityTypeIdentifierHeartRate

import os
import xml.etree.ElementTree as ET

def extract_stress_features(dataset, output_dir="data/interim"):

    tree = ET.parse(dataset)

    features = [
        "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
        "HKQuantityTypeIdentifierRestingHeartRate",
        "HKQuantityTypeIdentifierHeartRate"
    ]

    os.makedirs(output_dir, exist_ok=True)

    root = tree.getroot()
    for feature in features:
        feature_root = ET.Element("HealthData")
        for item in root.findall(f".//Record[@type='{feature}']"):
            feature_root.append(item)

        output_path = os.path.join(output_dir, f"{feature}.xml")
        ET.ElementTree(feature_root).write(output_path, encoding="utf-8", xml_declaration=True)

def main():
    extract_stress_features("data/raw/export.xml")

if __name__ == "__main__":
    main()
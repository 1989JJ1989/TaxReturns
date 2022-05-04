import csv
import os
from datetime import datetime

# Opening the raw data provided by Coinbase.com
with open("fills.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Parsing fiscal years and traded currencies and changing date string to datetime object
    fiscal_years = []
    currencies = {}
    for row in csv_reader:
        row["created at"] = datetime.strptime(
            row["created at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if row["created at"].year not in fiscal_years:
            fiscal_years.append(row["created at"].year)
        if row["size unit"] not in currencies:
            currencies[row["size unit"]] = os.path.join(os.getcwd(), row["size unit"])

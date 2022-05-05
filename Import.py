import csv
import os
from datetime import datetime

# Opening the raw data provided by Coinbase.com
with open("fills_cpro.csv", "r+") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    fieldnames = csv_reader.fieldnames

    # Parsing fiscal years and traded currencies and changing date string to datetime object
    fieldnames = csv_reader.fieldnames
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

# Setting up an appropriate data structure
# Setting up a tree structure for each currency, year and side
for currency in currencies:
    for year in fiscal_years:
        for side in ["BUY", "SELL"]:
            try:
                os.makedirs(os.path.join(currencies[currency], str(year), side))
            except:
                FileExistsError

            # Setting up a respective csv file to take in the values
            with open(
                os.path.join(
                    currencies[currency],
                    str(year),
                    side,
                    "{}_{}_fills.csv".format(currency, str(year)),
                ),
                "w",
            ) as new_file:
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
                csv_writer.writeheader()

                with open("fills_cpro.csv", "r+") as csv_file:
                    csv_reader = csv.DictReader(csv_file)

                    # Writing the appropriate values to the respective appropriate csv files
                    for row in csv_reader:
                        row["created at"] = datetime.strptime(
                            row["created at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        )
                        if (
                            row["size unit"] == currency
                            and row["created at"].year == year
                            and row["side"] == side
                        ):
                            csv_writer.writerow(row)

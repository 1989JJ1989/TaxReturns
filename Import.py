import csv
import os
import Consolidate as cs
from datetime import datetime

# Creating a merged fills file out of the separate Coinbase Basic and Pro fills files
cs.convert_coinbase_basic("fills_c.csv", "fills_cpro.csv")

# Opening the merged fills file
with open("merged_fills.csv", "r+") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    fieldnames = csv_reader.fieldnames

    # Parsing fiscal years and traded currencies and changing date string to datetime object
    fiscal_years = []
    currencies = {}
    for row in csv_reader:
        try:
            row["created at"] = datetime.strptime(
                row["created at"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            row["created at"] = datetime.strptime(
                row["created at"], "%Y-%m-%dT%H:%M:%SZ"
            )
        if row["created at"].year not in fiscal_years:
            fiscal_years.append(row["created at"].year)
        if row["size unit"] not in currencies:
            currencies[row["size unit"]] = os.path.join(os.getcwd(), row["size unit"])

# Setting up an appropriate data structure
# Setting up a tree structure for each currency, year and side
for currency in currencies.keys():
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

                with open("merged_fills.csv", "r+") as csv_file:
                    csv_reader = csv.DictReader(csv_file)

                    # Writing the appropriate values to the respective appropriate csv files
                    for row in csv_reader:
                        # try:
                        #     row["created at"] = datetime.strptime(
                        #         row["created at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        #     )
                        # except ValueError:
                        #     row["created at"] = datetime.strptime(
                        #         row["created at"], "%Y-%m-%dT%H:%M:%SZ"
                        #     )

                        if row["size unit"] == currency and row["side"] == side:
                            csv_writer.writerow(row)

                        # # print(row["created at"])
                        # print(row["size unit"])
                        # print(row["side"])

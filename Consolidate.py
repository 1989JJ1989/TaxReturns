import csv
import os
from datetime import datetime

# Defining the function to merge two csv files from Coinbase Basic and Coinbase Pro
def convert_coinbase_basic(tobeconverted1, tobeconverted2):

    # Setting the different paths to the files and to the merged file
    path_tobeconverted1 = os.path.join(os.getcwd(), "fills_raw", tobeconverted1)
    path_tobeconverted2 = os.path.join(os.getcwd(), "fills_raw", tobeconverted2)
    path_merged = os.path.join(os.getcwd(), "merged_fills.csv")

    # Mapping the different keys in the files to be merged to align the data
    key_mapping = {
        "portfolio": "NOT PROVIDED",
        "trade id": "NOT PROVIDED",
        "product": "NOT PROVIDED",
        "side": "Transaction Type",
        "created at": "Timestamp",
        "size": "Quantity Transacted",
        "size unit": "Asset",
        "price": "Spot Price at Transaction",
        "fee": "Fees",
        "total": "Total (inclusive of fees)",
        "price/fee/total unit": "Spot Price Currency",
    }

    # Opening the files to be merged
    with open(path_tobeconverted1, "r") as csv_tbc1:
        csv_reader1 = csv.DictReader(csv_tbc1)

        with open(path_tobeconverted2, "r") as csv_tbc2:
            csv_reader2 = csv.DictReader(csv_tbc2)

            # Writing to the new file showing the merged data
            with open(path_merged, "w") as csv_merged:
                csv_writer = csv.DictWriter(csv_merged, fieldnames=key_mapping.keys())

                csv_writer.writeheader()

                for row in csv_reader1:
                    trade = {}
                    for key, item in key_mapping.items():
                        trade[key] = row.get(item, "NOT PROVIDED")
                        if key == "side":
                            trade[key] = row.get(item, "NOT PROVIDED").upper()
                    csv_writer.writerow(trade)

                for row in csv_reader2:
                    trade = {}
                    for key, item in key_mapping.items():
                        trade[key] = row[key]
                    csv_writer.writerow(trade)

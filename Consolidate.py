import csv
import os


def convert_coinbase_basic(tobeconverted, master):
    path_tobeconverted = os.path.join(os.getcwd(), "fills_raw", tobeconverted)
    path_master = os.path.join(os.getcwd(), "fills_raw", master)

    key_mapping = {
        "portfolio": "NEW",
        "trade_id": "NEW",
        "product": "NEW",
        "side": "Type",
        "created at": "Timestamp",
        "size": "Quantity Transacted",
        "size unit": "Asset",
        "price": "Spot Price at Transaction",
        "fee": "NEW",
        "total": "Total",
        "price/fee/total unit": "Spot Price Currency",
    }

    with open(path_tobeconverted, "r") as csv_tobeconverted:
        csv_reader = csv.DictReader(csv_tobeconverted)
        print(csv_tobeconverted.closed)

        # First off, apending to the end of the file
        with open(path_master, "a") as csv_master:
            csv_writer = csv.DictWriter(csv_master, fieldnames=key_mapping.keys())
            print(csv_master.closed)

            for row in csv_reader:
                trade = {}
                for key, item in key_mapping.items():
                    trade[key] = item
                csv_writer.writerow(trade)


convert_coinbase_basic("fills_c.csv", "fills_cpro.csv")

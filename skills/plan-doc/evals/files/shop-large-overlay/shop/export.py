import csv


def write_orders_csv(rows, path):
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)

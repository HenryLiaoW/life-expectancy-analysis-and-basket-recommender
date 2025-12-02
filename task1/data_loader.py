import csv

# def load_csv(path):
#     return []


def load_csv(path):
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

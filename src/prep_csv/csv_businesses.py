import json
import csv
import config
from tqdm import tqdm

CSV_BUS = "./out/business_{}.csv".format(config.SUBSET_SETTINGS['PERC'])
CSV_CAT = "./out/categories_{}.csv".format(config.SUBSET_SETTINGS['PERC'])

BUS_HEADERS = ["business_id", "name", "address", "city", "state", "postal_code", "latitude", "longitude", "stars",
               "is_open"]
CAT_HEADERS = ["business_id", "category"]


def write_csv(f):
    f_bus = open(CSV_BUS, 'w')
    f_cat = open(CSV_CAT, 'w')
    fw_bus = csv.DictWriter(f_bus, fieldnames=BUS_HEADERS)
    fw_cat = csv.DictWriter(f_cat, fieldnames=CAT_HEADERS)

    fw_bus.writeheader()
    fw_cat.writeheader()

    num_lines = sum(1 for _ in open(f, 'r'))
    with tqdm(total=num_lines) as pbar:
        with open(f, 'r') as sub_f:
            for l in sub_f:
                process_line(fw_bus, fw_cat, l)
                pbar.update(1)

    f_bus.close()
    f_cat.close()


def process_line(fw_bus, fw_cat, line):
    bus_line = dict()

    data = json.loads(line)
    for h in BUS_HEADERS:
        if type(data[h]) is str:
            bus_line[h] = data[h].replace(",", "")
        else:
            bus_line[h] = data[h]
    fw_bus.writerow(bus_line)

    for cat in data["categories"]:
        cat_line = dict()
        cat_line["business_id"] = data["business_id"]
        cat_line["category"] = cat
        fw_cat.writerow(cat_line)

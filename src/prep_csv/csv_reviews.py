import json
import csv
import config
from tqdm import tqdm

CSV_REV = "./out/reviews_{}.csv".format(config.SUBSET_SETTINGS['PERC'])

REV_HEADERS = ["review_id", "user_id", "business_id", "stars", "useful", "funny", "cool", "text", "date"]


def write_csv(f):
    f_rev = open(CSV_REV, 'w')
    fw_rev = csv.DictWriter(f_rev, fieldnames=REV_HEADERS)

    fw_rev.writeheader()

    num_lines = sum(1 for _ in open(f, 'r'))
    with tqdm(total=num_lines) as pbar:
        with open(f, 'r') as sub_f:
            for l in sub_f:
                process_line(fw_rev, l)
                pbar.update(1)

    f_rev.close()


def process_line(fw_rev, line):
    rev_line = dict()

    data = json.loads(line)
    for h in REV_HEADERS:
        if type(data[h]) is str:
            rev_line[h] = data[h].replace(",", "")
        else:
            rev_line[h] = data[h]
    fw_rev.writerow(rev_line)

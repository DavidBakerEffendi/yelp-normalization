import json
import csv
import config
from tqdm import tqdm

CSV_USE = "./out/users_{}.csv".format(config.SUBSET_SETTINGS['PERC'])
CSV_FND = "./out/friendships_{}.csv".format(config.SUBSET_SETTINGS['PERC'])

USE_HEADERS = ["user_id", "name", "yelping_since", "useful", "funny", "cool", "fans"]
FND_HEADERS = ["user_id", "friend_id"]


def write_csv(f):
    f_use = open(CSV_USE, 'w')
    f_fnd = open(CSV_FND, 'w')
    fw_use = csv.DictWriter(f_use, fieldnames=USE_HEADERS)
    fw_fnd = csv.DictWriter(f_fnd, fieldnames=FND_HEADERS)

    fw_use.writeheader()
    fw_fnd.writeheader()

    num_lines = sum(1 for _ in open(f, 'r'))
    with tqdm(total=num_lines) as pbar:
        with open(f, 'r') as sub_f:
            for l in sub_f:
                process_line(fw_use, fw_fnd, l)
                pbar.update(1)

    f_use.close()
    f_fnd.close()


def process_line(fw_use, fw_fnd, line):
    use_line = dict()

    data = json.loads(line)
    for h in USE_HEADERS:
        if type(data[h]) is str:
            use_line[h] = data[h].replace(",", "")
        else:
            use_line[h] = data[h]
    fw_use.writerow(use_line)

    for friend in data["friends"]:
        friend_line = dict()
        friend_line["user_id"] = data["user_id"]
        friend_line["friend_id"] = friend
        fw_fnd.writerow(friend_line)

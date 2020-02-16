import json
from tqdm import tqdm
import config

SUB_FILE = "./out/users_subset_{}.json".format(config.SUBSET_SETTINGS['PERC'])


def get_user_ids(fr, sub_num):
    user_ids = set()
    i = 0
    for line in fr:
        user_ids.add(json.loads(line)["user_id"])
        i += 1
        if i == sub_num - 1:
            return user_ids


def strip_friends(line, user_ids):
    user_line = dict()

    data = json.loads(line)
    friends_list = data['friends']
    stripped_list = list(user_ids & set(friends_list))

    user_line['user_id'] = data['user_id']
    user_line['name'] = data['name']
    user_line['yelping_since'] = data['yelping_since']
    user_line['useful'] = data['useful']
    user_line['funny'] = data['funny']
    user_line['cool'] = data['cool']
    user_line['friends'] = stripped_list
    user_line['fans'] = data['fans']

    return json.dumps(user_line)


def generate_subset(f_dir, perc):
    fr = open(f_dir, 'r')
    fw = open(SUB_FILE, 'w')
    num_lines = sum(1 for _ in fr)
    sub_num = int(perc * num_lines)

    fr.seek(0)
    user_ids = get_user_ids(fr, sub_num)

    fr.seek(0)
    with tqdm(total=sub_num) as pbar:
        for line in fr:
            new_line = strip_friends(line, user_ids)
            fw.write(new_line + '\n')
            pbar.update(1)
            if pbar.n == sub_num - 1:
                break
    fr.close()
    fw.close()

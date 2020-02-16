import json

from tqdm import tqdm

import config
from src.subset import sub_users, sub_businesses

SUB_FILE = "./out/reviews_subset_{}.json".format(config.SUBSET_SETTINGS['PERC'])


def generate_subset(f_dir, perc):
    fr = open(f_dir, 'r')
    fw = open(SUB_FILE, 'w')
    num_lines = sum(1 for _ in fr)

    # Load all user and business IDs
    print('[INFO] Loading all user and business IDs to validate reviews')
    n_user_f = open(sub_users.SUB_FILE, 'r')
    n_business_f = open(sub_businesses.SUB_FILE, 'r')
    users = set([json.loads(d)['user_id'] for d in n_user_f])
    businesses = set([json.loads(d)['business_id'] for d in n_business_f])
    n_user_f.close()
    n_business_f.close()

    print('[INFO] Continuing with review subset...')
    fr.seek(0)
    count = 0
    with tqdm(total=num_lines) as pbar:
        for line in fr:
            data = json.loads(line)
            if data['user_id'] in users and data['business_id'] in businesses:
                fw.write(line)
                count += 1
            pbar.update(1)
    print('[INFO] Total reviews {}. Because of the subsets of users and businesses, {} reviews written.'
          .format(num_lines, count))
    fr.close()
    fw.close()

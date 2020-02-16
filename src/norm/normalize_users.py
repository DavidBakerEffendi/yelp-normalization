import json

NORM_FILE = './out/user_norm.json'


def process_line(fw, line):
    user_line = dict()

    data = json.loads(line)
    user_line['user_id'] = data['user_id']
    user_line['name'] = data['name']
    user_line['yelping_since'] = data['yelping_since']
    user_line['useful'] = data['useful']
    user_line['funny'] = data['funny']
    user_line['cool'] = data['cool']
    user_line['friends'] = str(data['friends']).split(', ')
    user_line['fans'] = data['fans']

    fw.write(json.dumps(user_line) + '\n')

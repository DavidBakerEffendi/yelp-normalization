import json

NORM_FILE = './out/review_norm.json'


def process_line(fw, line):
    review_line = dict()

    data = json.loads(line)

    review_line['review_id'] = data['review_id']
    review_line['user_id'] = data['user_id']
    review_line['business_id'] = data['business_id']
    review_line['stars'] = data['stars']
    review_line['useful'] = data['useful']
    review_line['funny'] = data['funny']
    review_line['cool'] = data['cool']
    review_line['text'] = data['text']
    review_line['date'] = data['date']

    fw.write(json.dumps(review_line) + '\n')

import json

NORM_FILE = './out/business_norm.json'


def process_line(fw, line):
    business_line = dict()

    data = json.loads(line)
    business_line['business_id'] = data['business_id']
    business_line['name'] = data['name']
    business_line['address'] = data['address']
    business_line['city'] = data['city'].title()  # Some city names are all caps etc. fix this by calling title()
    business_line['state'] = str(data['state']).upper()
    business_line['postal_code'] = data['postal_code']
    business_line['latitude'] = data['latitude']
    business_line['longitude'] = data['longitude']
    business_line['stars'] = data['stars']
    business_line['categories'] = str(data['categories']).split(', ')
    if data['is_open'] == 0:
        business_line['is_open'] = False
    else:
        business_line['is_open'] = True

    fw.write(json.dumps(business_line) + '\n')

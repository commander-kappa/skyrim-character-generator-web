import regex as re
REGEX = re.compile('^class\\s(.+)\\(.+')


with open('./model.py', 'r') as file:
    for line in file.readlines():
        if line.startswith('class '):
            out = REGEX.sub('tables[\"\\1\"] = model.\\1.query.all()', line)
            print(out[:-1])
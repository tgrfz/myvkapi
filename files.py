import json

def id_list_from_file(file):
    with open(file, 'r', encoding='utf-8') as fin:
        ids = [int(line) for line in fin]
    return ids

def id_list_in_file(file, ids):
    with open(file, 'w', encoding='utf-8') as fout:
        for id in ids:
            fout.write("{}\n".format(id))

def statuses_from_file(file):
    memory = {}
    id_ = -1
    with open(file, 'r', encoding='utf-8') as fin:
        for line in fin:
            if id_ == -1:
                id_ = int(line[:-1])
            else:
                memory[id_] = line[:-1]
                id_ = -1
    return memory

def statuses_in_file(file, statuses):
    with open(file, 'w', encoding = 'utf-8') as fout:
        for id_ in statuses:
            fout.write('{}\n{}\n'.format(id_, statuses[id_]))

def dump_in_json_file(file, data):
    with open(file, 'w', encoding = 'utf-8') as fout:
        json.dump(data, fout)

def load_from_json_file(file):
    with open(file, 'r', encoding='utf-8') as fin:
        data = json.load(fin)
    return data
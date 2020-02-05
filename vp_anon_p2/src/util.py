import csv
import random as rd


class fdict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


fset = frozenset


def get_data(path):
    f = open(path, "r")
    reader = csv.DictReader(f)

    data = [line for line in csv.DictReader(f)]

    f.close()

    return data


def write_data(path, l_df):
    f = open(path, "w")
    writer = csv.DictWriter(f, list(l_df[0][0].keys()))

    writer.writeheader()
    for df in l_df:
        for line in df:
            writer.writerow(line)

    f.close()


gt = get_data("data/ground_truth.csv")


def month_split(df=gt, nb_month_to_split=13):
    if nb_month_to_split == 0: nb_month_to_split = 13
    month_start, pos = 0, 0
    l_df = []

    for i in range(nb_month_to_split):
        splitted_date = df[month_start]['date'].split('/')
        year, month = splitted_date[0], splitted_date[1]

        while (year == splitted_date[0] and month == splitted_date[1] and pos
               <= len(df)):
            if pos < len(df):
                splitted_date = df[pos]['date'].split('/')
            pos += 1

        month_length = pos - month_start - 1
        if month_start + month_length > len(df):
            month_length = len(df) - month_start
        l_df.append(df[month_start:month_start + month_length])

        month_start = pos - 1

    return l_df


def row2str(row):
    return (f"{row['id_user']}{row['date']}{row['hours']}{row['id_item']}"
            f"{row['price']}{row['qty']}")


def get_item(field, df=gt):
    return {row[field] for row in df}


def get_item_bought_per_uid(uid, df=gt):
    return {row['id_item'] for row in df if row['id_user'] == uid}


def get_item_bought_per_uids(uids, df=gt):
    return {uid: get_item_bought_per_uid(uid) for uid in uids}


def get_row_by_field(field, value, df=gt):
    return {value: {row for row in df if row[field] == value}}


def get_row_per_uid(uid, df=gt):
    return {fdict(row) for row in df if row['id_user'] == uid}


def flatten_set(s):
    return {e for elt in s for e in elt}


def inter_len(s1, s2):
    return len(s1.intersection(s2))


def dict2list(d):
    return list(d.items())


def count_dels(df=gt):
    return len([row['id_user'] for row in df if row['id_user'] == "DEL"])


def gen_pos_uid(df=gt):
    return {row['id_user']: {i for i, a_row in enumerate(df) if
            a_row['id_user'] == row['id_user']}
            for row in df}

import random
import time
from os.path import isfile
import csv
import gauss


def stats(rows):
    res = dict([('id_user', dict()), ('date', dict()), ('hours', dict()),
                ('id_item', dict()), ('price', dict()), ('qty', dict())])
    for r in rows:
        iu = r['id_user']
        d = r['date']
        h = r['hours']
        it = r['id_item']
        p = r['price']
        q = r['qty']
        if iu in res['id_user'].keys():
            res['id_user'][iu] += 1
        else:
            res['id_user'][iu] = 1
        if d in res['date'].keys():
            res['date'][d] += 1
        else:
            res['date'][d] = 1
        if h in res['hours'].keys():
            res['hours'][h] += 1
        else:
            res['hours'][h] = 1
        if it in res['id_item'].keys():
            res['id_item'][it] += 1
        else:
            res['id_item'][it] = 1
        if p in res['price'].keys():
            res['price'][p] += 1
        else:
            res['price'][p] = 1
        if q in res['qty'].keys():
            res['qty'][q] += 1
        else:
            res['qty'][q] = 1
    return res


def stats_targets(rows, list_fields):
    """
    DMA
    date format change in AAAA/MM
    :param rows: (dict) rows of csv file
    :param list_fields: (list str) exact names of fields to compare
    :return: (dict) keys : values of fields sep ' ' ; values : times keys war encountred
    """
    res = dict()
    for r in rows:
        temp = ""
        for f in list_fields:
            if f == 'date':
                temp += r[f][:-3]
            else:
                temp += str(r[f])
            temp += ' '
        if temp in res.keys():
            res[temp] += 1
        else:
            res[temp] = 1
    return res


def select_uniq_iditems_iduser(statistics):
    """
    DMA
    date format here : AAAA/MM
    :param statistics: (dict) keys : values of fields in this order "id_user, id_item, date", values (int) not used
    :return: (list dict) keys : "id_user, id_item, date", values: corresponding values
    """
    dico = dict()
    for s in statistics.keys():
        tmp = s.split(' ')
        [id_, temp, date] = tmp[0], tmp[1], tmp[2]
        if temp in dico.keys():
            if id_ not in dico[temp]:
                dico[temp].append((id_, date))
        else:
            dico[temp] = [(id_, date)]
    dico_uniq = []
    for el in dico.items():
        if len(el[1]) <= 5:
            for i in range(0, len(el[1])):
                dico_uniq.append(dict([('id_item', el[0]), ('id_user', el[1][i][0]), ('date', el[1][i][1])]))
    return dico_uniq


def check_prices_items(rows):
    """
    DMA
    :param rows: (dict) rows of csv file
    :return: (dict) keys : id_item, values : (list) prices for this item
    """
    dico = dict()
    for r in rows:
        if r['id_item'] in dico.keys():
            if not r['price'] in dico[r['id_item']].keys():
                dico[r['id_item']][r['price']] = 1
            else:
                dico[r['id_item']][r['price']] += 1
        else:
            dico[r['id_item']] = {r['price']: 1}
    return dico


def avg_prices_items(rows):
    """
    |!| modify rows
    :param rows:
    :return:
    """
    temp = dict()
    mrows = check_prices_items(rows)
    for u in mrows.items():
        id_item = u[0]
        prices = u[1]
        tmp = 0
        nb = 0
        for v in prices.items():
            tmp += float(v[0]) * v[1]
            nb += v[1]
        temp[id_item] = round(tmp / nb, 2)
    for r in rows:
        if r['id_item'] in temp.keys():
            r['price'] = temp[r['id_item']]
    return rows


def supp_uniq_usr_item(rows):
    """
    DMA
    DEL when this user is the only one to use the item of this line
    :param rows: (dict) rows of csv file
    :return: (dict) the same dict with id_user value changed to DEL
    """
    statistics = stats_targets(rows, ['id_user', 'id_item', 'date'])
    uniq_item_user = select_uniq_iditems_iduser(statistics)
    res = []
    for r in rows:
        for u in uniq_item_user:
            if r['id_user'] == u['id_user'] and r['id_item'] == u['id_item'] and r['date'][:-3] == u['date']:
                r['id_user'] = 'DEL'
        res.append(r)
    return res


def change_row(rows, i, j, field_):
    temp = rows[i][field_]
    rows[i][field_] = rows[j][field_]
    rows[j][field_] = temp
    return rows


def read_csv_file(path):
    with open(path) as truth:
        reader = csv.DictReader(truth)
        row1 = reader.__next__()
        res = [row1]
        for row in reader:
            res.append(row)
    return res


def month_extremities(f):
    file = f[:-4] + "_month_extremities" + ".csv"
    if not isfile(file):
        rows = read_csv_file(f)
        dic_lines_a_month = dict()
        for i in range(len(rows)):
            if rows[i]['date'][0:7] in dic_lines_a_month.keys():
                dic_lines_a_month[rows[i]['date'][0:7]] += 1
            else:
                dic_lines_a_month[rows[i]['date'][0:7]] = 1
        month_ends = dict()
        prev_month = 0
        for el in dic_lines_a_month.items():
            month_ends[el[0]] = (prev_month, prev_month + el[1])
            prev_month += el[1]
        res = []
        for e in month_ends.items():
            res.append({'month': e[0], 'begin': e[1][0], 'end': e[1][1]})
        gauss.write_file(file[:-4], res, ['month', 'begin', 'end'])
    return read_csv_file(file)


def shuffle_uniq_usr_item(rows, file):
    """
    #TODO
    :param file:
    :param rows:
    :return:
    """
    statistics = stats_targets(rows, ['id_user', 'id_item', 'date'])
    uniq_item_user = select_uniq_iditems_iduser(statistics)
    uniq_lines = []
    for i in range(len(rows)):
        for u in uniq_item_user:
            if rows[i]['id_user'] == u['id_user'] and rows[i]['id_item'] == u['id_item']\
                    and rows[i]['date'][:-3] == u['date']:
                uniq_lines.append(i)
    random.seed(int(time.time()))
    month_ends = month_extremities(file)
    deb_m, end_m = int(), int()  # just declaration
    for i in uniq_lines:
        month = ""
        for m in month_ends:
            if m['month'] == rows[i]['date'][0:7]:
                deb_m, end_m = int(m['begin']), int(m['end'])
                month = m['month']
        j = random.randint(deb_m, end_m)
        imonth = gauss.csv_getter("ground_truth_month_" + str(month_translator(month)) + "_item_usrs.csv")
        item_users = []  # just declaration
        for item in imonth:
            if item['id_item'] == rows[i]['id_item']:
                item_users = item['users']
        while rows[j]['id_user'] in item_users:
            j = random.randint(deb_m, end_m)
        rows = change_row(rows, i, j, 'price')
        rows = change_row(rows, i, j, 'id_item')
        rows = change_row(rows, i, j, 'qty')
    return rows


def month_translator(m):
    if type(m) is int:
        return "2010/12" if m == 0 else "2011/" + gauss.str_back((m-1))
    else:  #m is str
        return 1 if m == "2010/12" else int(m[-2:]) + 1

def write_item_users(file):
    for i in range(1, 14):
        f = file[:-4] + "_month_" + str(i) + ".csv"
        rows = gauss.csv_getter(f)
        refer_item_usrs(rows, f)
    return


def refer_item_usrs(rows, file):
    """
    DMA
    :param rows: the rows of file
    :param file: path of csv file (with the extention ".csv")
    :return:
    """
    res = dict()
    for r in rows:
        if r['id_item'] in res.keys():
            if r['id_user'] not in res[r['id_item']]:
                res[r['id_item']].append(r['id_user'])
        else:
            res[r['id_item']] = [r['id_user']]
    temp = []
    for e in res.items():
        temp.append({'id_item': e[0], 'users': e[1]})
    gauss.write_file(file[:-4] + "_item_usrs", temp, ['id_item', 'users'])


def shuffle_half_hour(rows):
    t = rows[0]['hours']
    i = 1
    temp = [rows[0]]
    #TODO
    #while

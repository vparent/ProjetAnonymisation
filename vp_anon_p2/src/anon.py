import sys
import hashlib
import random as rd
import numpy as np
sys.path.append('./src/')
import util as u


def gen_corresp_pseudonym_hash(gt):
    new_uids = set()
    corresp = {}

    uids = {row['id_user'] for row in gt}

    for uid in uids:
        transacs = set()
        if uid == "DEL":
            corresp[uid] = "DEL"
        else:
            transacs = {u.fdict(row) for row in gt
                        if row['id_user'] == uid}
            transac = rd.choice(list(transacs))
            str_transac = str(rd.randint(0, 256)) + u.row2str(transac)
            htransac = hashlib.sha512(str_transac.encode()).hexdigest()
            borne = rd.randint(0, 123)
            while htransac[borne:borne+5] in new_uids:
                borne = rd.randint(0, 122)
            new_uids.add(htransac[borne:borne+5])
            corresp[uid] = htransac[borne:borne+5]

    return corresp


def apply_pseudom(gt, corresp):
    for i in range(len(gt)):
        new_uid = corresp[gt[i]['id_user']]
        gt[i]['id_user'] = new_uid

    return gt


def pseudonym_hash_per_month(ngt):
    for i in range(len(ngt)):
        corresp = gen_corresp_pseudonym_hash(ngt[i])
        apply_pseudom(ngt[i], corresp)

    return ngt


def get_item_set_classes(gt):
    uids = u.get_item('id_user', gt)

    i_bought = u.get_item_bought_per_uids(uids, gt)
    d_inter_u_len = {uid_1: {u.inter_len(i_bought[uid_1], i_bought[uid_2]):
                     uid_2 for uid_2 in uids - {uid_1}}
                     for uid_1 in uids}

    # Ensemble d'utilisateur qui ont acheté les mêmes items
    # dans le moiscommun.
    u_classes = set()
    # for i in range(2):
    for uid_1 in d_inter_u_len.keys():
        # On récupère les classes ou uid_1 apparaît
        classes = {u_class for u_class in u_classes if uid_1 in u_class}
        u_class = {elt for a_class in classes for elt in set(a_class)}
        # Si uid_1 apparaît déja dans une classe d'id_user
        if not classes:
            # On les supprimes de l'ensemble des classes
            # d'id_user pour mise-à-jour
            u_classes -= classes
            if len(d_inter_u_len[uid_1].values()) > 0:
                u_classes.add(u.fset({uid_1, max(d_inter_u_len[uid_1].items())[1]}
                              | {elt for a_class in classes for elt in set(a_class)
                              }))
        # Sinon on ajoute une classe
        else:
            if len(d_inter_u_len[uid_1].values()) > 0:
                u_classes.add(u.fset({uid_1, max(d_inter_u_len[uid_1].items())[1]})
                              )

    uid_classes = set()
    for uid in d_inter_u_len.keys():
        classes = {u_class for u_class in u_classes if uid in u_class}
        a_u_class = {elt for a_class in classes for elt in set(a_class)}
        uid_classes.add(u.fset(a_u_class))

    return uid_classes


def merge_item_set_classes(gt, lim=10):
    iset_classes = get_item_set_classes(gt)
    print("got classes")

    class_pairs = set()
    for class1 in iset_classes:
        go_next = False
        for pair in class_pairs:
            if class1 in pair:
                go_next = True
        if go_next:
            continue
        uid0 = list(class1)[0]
        i_bought_0 = u.get_item_bought_per_uid(uid0)
        c_class2 = [a_class for a_class in iset_classes if
                    u.inter_len(u.get_item_bought_per_uid(list(a_class)[0]),
                                i_bought_0) > lim]

        if len(c_class2) > 0:
            if c_class2[0] == class1 and len(c_class2) > 1:
                class2 = c_class2[1]
            class_pairs.add((class1, class2))
        print(class_pairs)

    iids = u.get_item('id_user', gt)
    for pair in class_pairs:
        i_bought_1 = u.get_item_bought_per_uid(list(pair[0])[0])
        i_bought_2 = u.get_item_bought_per_uid(list(pair[0])[0])
        inter = i_bought_1.intersection(i_bought_2)
        for i in range(len(gt)):
            if gt[i]['id_user'] in pair[0]:
                if gt[i]['id_item'] not in inter:
                    gt[i]['id_item'] = "DEL"
            if gt[i]['id_user'] in pair[1]:
                if gt[i]['id_item'] not in inter:
                    gt[i]['id_item'] = "DEL"

    return gt


def uniform_date(df, tresh=0.50):
    l_dates = [row['date'] for row in df]
    s_dates = set(l_dates)
    l_tuple_freq_date = []

    for date in s_dates:
        l_tuple_freq_date.append((l_dates.count(date) / len(l_dates), date))
    l_tuple_freq_date.sort(reverse=True)

    i, f_sum = 0, 0
    while f_sum < tresh:
        f_sum += l_tuple_freq_date[i][0]
        i += 1
    n_dates = [tpl[1] for tpl in l_tuple_freq_date[0:i]]
    n_dates.sort()
    i = 0
    while i < len(df):
        day = df[i]['date'].split('/')[2]
        j = 0
        while j < len(n_dates) and n_dates[j].split('/')[2] < day:
            j += 1
        if (j < len(n_dates)):
            df[i]['date'] = n_dates[j]
        else:
            df[i]['date'] = n_dates[len(n_dates)-1]
        i += 1

    return df


def uniform_hours(df, tresh=0.50):
    l_hours = [row['hours'] for row in df]
    s_hours = set(l_hours)
    l_tuple_freq_hour = []

    for hour in s_hours:
        l_tuple_freq_hour.append((l_hours.count(hour) / len(l_hours), hour))
    l_tuple_freq_hour.sort(reverse=True)

    i, f_sum = 0, 0
    while f_sum < tresh:
        f_sum += l_tuple_freq_hour[i][0]
        i += 1
    n_hours = [tpl[1] for tpl in l_tuple_freq_hour[0:i]]
    n_hours.sort()
    i = 0
    while i < len(df):
        hour, minute = cur_hour, cur_min = tuple(df[i]['hours'].split(':'))
        j = 0
        while j < len(n_hours) and cur_hour < hour and cur_min < minute:
            cur_hour, cur_min = tuple(df[i]['hours'].split(':'))
            j += 1
        if (j < len(n_hours)):
            df[i]['hours'] = n_hours[j]
        else:
            df[i]['hours'] = n_hours[len(n_hours)-1]
        i += 1

    return df

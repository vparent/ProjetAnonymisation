import src.util as util
import random as rd


def del_half_random_all_gt(gt):
    idx_to_del = []

    while len(idx_to_del) < len(gt) // 2:
        idx_choice = rd.choice(range(len(gt)))
        if idx_choice not in idx_to_del:
            idx_to_del.append(idx_choice)

    return idx_to_del


def del_half_per_month(ngt):
    idx_to_del = []

    for gt in ngt:
        idx_to_del.append(del_half_random_all_gt(gt))

    return idx_to_del


def del_lines_per_idx(gt, idx_to_del):
    for idx in idx_to_del:
        gt[idx]['id_user'] = "DEL"
    return gt


def del_lines_per_idx_per_month(ngt, idxs_to_del):
    for i, idx_list in enumerate(idxs_to_del):
        for idx in idx_list:
            ngt[i][idx]['id_user'] = "DEL"
    return ngt

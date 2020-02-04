from tt_test import month_translator

def count_id(rows):
    res = dict()
    for r in rows:
        _id = r["id_user"]
        if _id in res.keys():
            date = r["date"][:-3]
            if date in res[_id].keys():
                if r["id_item"] in res[_id][date]:
                    res[_id][date][r["id_item"]] += r["qty"]
                else:
                    res[_id][date][r["id_item"]] = r["qty"]
            else:
                res[_id][date] = dict()
                res[_id][date][r["id_item"]] = r["qty"]
        else:
            res[_id] = dict()
            res[_id][r["date"][:-3]] = dict()
            res[_id][r["date"][:-3]][r["id_item"]] = r["qty"]
    return res


def convert_dic(dico):
    res = []
    for _id in dico.items():
        for date in _id[1].items():
            for item in date[1].items():
                res.append(dict())
                res[-1]["id_user"] = _id[0]
                res[-1]["date"] = date[0]
                res[-1]["id_item"] = item[0]
                res[-1]["qty"] = item[1]
    return res


def qty(gt, s):
    dicoT = count_id(gt)
    dicoA = count_id(s)
    tT = convert_dic(dicoT)
    tA = convert_dic(dicoA)
    ids = {e[0] for e in dicoT.items()}
    idsA = {e[0] for e in dicoA.items()}
    ids = list(ids)
    result1 = [ids] + [[dict() for k in range(len(ids))] for l in range(13)]
    for ttA in tA:
        for ttT in tT:
            if ttA["date"] == ttT["date"] and ttA["id_item"] == ttT["id_item"]:
                idx = result1[0].index(ttT["id_user"])
                y = month_translator(ttT["date"])
                nbA = int(ttA["qty"])
                nbT = int(ttT["qty"])
                if y > 14:
                    print(ttT["date"])
                if ttA["id_user"] in result1[y][idx].keys():
                    result1[y][idx][ttA["id_user"]].append(abs(nbA-nbT)/max(nbA, nbT))
                else:
                    result1[y][idx][ttA["id_user"]] = [abs(nbA-nbT)/max(nbA, nbT)]
    print("phase 2")
    for i in range(1, len(result1)):
        for j in range(len(result1[0])):
            for id_ in idsA:
                if id_ in result1[i][j] :
                    temp = result1[i][j][id_]
                    result1[i][j][id_] = 0
                    nb = 0
                    for k in temp:
                        if k != 0:
                            result1[i][j][id_] += k
                            nb += 1
                    result1[i][j][id_] = result1[i][j][id_] / nb
    return result1

"""
temp = result1[i][j]
                result1[i][j] = 0
                nb = 0
                for e in temp.keys():
                    if e == id_:

                        if e in result1[i][j].keys():
                            result1[i][j][e] += temp[e]
                for k in temp:

                result1[i][j] = result1[i][j] / taille
"""


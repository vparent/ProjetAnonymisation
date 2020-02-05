from gauss import *

f = "S_TMTM_submission_1-date_sorted_month_"
ft = "ground_truth_month_"

result1 = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
result2 = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
result3 = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
for i in range(1, 14):
    fil = f + str(i) + "_countids" + ".csv"
    filt = ft + str(i) + "_countids" + ".csv"
    rows = csv_getter(fil)
    rowst = csv_getter(filt)
    dicoA = dict()
    dicoT = dict()
    for r in rows:
        if r['nb'] in dicoA.keys():
            dicoA[r['nb']].append(r['id_user'])
        else:
            dicoA[r['nb']] = [r['id_user']]
    for r in rowst:
        if r['nb'] in dicoT.keys():
            dicoT[r['nb']].append(r['id_user'])
        else:
            dicoT[r['nb']] = [r['id_user']]
    for el in dicoA.items():
        tai = len(el[1])
        if tai <= 3 and el[0] in dicoT.keys():
            sources = dicoT[el[0]]
            for e in sources:
                if e in result1[0]:
                    j = result1[0].index(e)
                else:
                    j = len(result1[0])
                    for k in range(14):
                        result1[k].append('')
                        result2[k].append('')
                        result3[k].append('')
                result1[0][j] = e
                result2[0][j] = e
                result3[0][j] = e
                result1[i][j] = el[1][0]
                if tai >= 2:
                    result2[i][j] = el[1][1]
                    if tai == 3:
                        result3[i][j] = el[1][2]
result1 = transpo_mat(result1)
result2 = transpo_mat(result2)
result3 = transpo_mat(result3)
print(result1)
print("----------------")
print(result2)
print("---------------")
print(result3)
with open("res1_TMTM" + ".csv", 'w', newline='') as writer:
    wr = csv.writer(writer, quoting=csv.QUOTE_ALL)
    for r in result1:
        wr.writerow(r)
with open("res2_TMTM" + ".csv", 'w', newline='') as writer:
    wr = csv.writer(writer, quoting=csv.QUOTE_ALL)
    for r in result2:
        wr.writerow(r)
with open("res3_TMTM" + ".csv", 'w', newline='') as writer:
    wr = csv.writer(writer, quoting=csv.QUOTE_ALL)
    for r in result2:
        wr.writerow(r)
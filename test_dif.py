import csv

def csv_getter(f):
    with open(f, 'r') as truth:
        reader = csv.DictReader(truth)
        rows = []
        for r in reader:
            rows.append(r)
    return rows

def str_comp():
    A= csv_getter("funs_attack/resultat/F_on_sait_pas_1-LCOINSTI.csv")
    B= csv_getter("funs_attack/resultat/F_ONSP1-LCOINSTI.csv")
    print("B=",B[3]["1"])
    #list_n=[k for k in A[:]["id_user"]]
    dif=0
    tot=0
    l_t = [k for k in B[0].keys()]
    for l in range(len(B)):
        for k in l_t:
            tot+=1
            if A[l][k]!=B[l][k]:
                dif +=1
                #print("ligne =", l,"colonne",k," A = ",A[l][k]," B = ",B[l][k]," nA = ",A[l]["id_user"]," nB = ",B[l]["id_user"])
    print("dif = ",dif," tot = ",tot)

str_comp()
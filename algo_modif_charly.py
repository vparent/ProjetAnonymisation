import pandas
import hashlib
import random

gt = pandas.read_csv("ground_truth.csv")
gt1= pandas.read_csv("ground_truth_month_1.csv")
gt2= pandas.read_csv("ground_truth_month_2.csv")
gt3= pandas.read_csv("ground_truth_month_3.csv")
gt4= pandas.read_csv("ground_truth_month_4.csv")
gt5= pandas.read_csv("ground_truth_month_5.csv")
gt6= pandas.read_csv("ground_truth_month_6.csv")
gt7= pandas.read_csv("ground_truth_month_7.csv")
gt8= pandas.read_csv("ground_truth_month_8.csv")
gt9= pandas.read_csv("ground_truth_month_9.csv")
gt10= pandas.read_csv("ground_truth_month_10.csv")
gt11= pandas.read_csv("ground_truth_month_11.csv")
gt12= pandas.read_csv("ground_truth_month_12.csv")
gt13= pandas.read_csv("ground_truth_month_13.csv")

ngt=[gt1,gt2,gt3,gt4,gt5,gt6,gt7,gt8,gt9,gt10,gt11,gt12,gt13]
nngt=[gt1,gt2,gt3,gt4,gt5]
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L"]
date = ["JA","FE","MA","AP","MY","JN","JL","AU","SE","OC","NO","DE"]


dat_list = gt1.date.unique().tolist()
indexl =len(dat_list)-1

#########################################################################
# concatenation and write
def write_data(file_data_dst):  ##write data to csv file
    gt1.to_csv(file_data_dst, sep = ',', index=False)

def concat(): ## concatenate all csv file into 1 dataframe
    conc = pandas.concat(ngt)
    return conc

def write_data_conc(file_data_dst,co):  ## write concatenate dataframe to csv file
    co.to_csv(file_data_dst, sep = ',', index=False)
    

###########################################################################
# modif data

## Modif id_user ==> letter + id + month
def modif_user(index): 
    for g in ngt:
        if index == 13 : 
            index = 1
        g["letter"] = alphabet[index-1]
        g["months"] = date[index-1]
        g["id_user"] = g["letter"] + g["id_user"].apply(str) + g["months"]
        del g["letter"]
        del g["months"]
        index+=1
        #print(g.id_user)

def translation_mois_produit(mois1,mois2):
    tmp1 = ngt[mois1]#.sort_values(by=["id_item","date","hours"],ascending=[True,True,True])
    tmp2 = ngt[mois2]#.sort_values(by=["id_item","date","hours"],ascending=[True,False,False])
    i=0
    prec=0

    dic1 = {}
    dic2 = {}

    for t,g in tmp1.iterrows():
        if type(prec) == type(0):
            prec = g["id_item"]
            dic1[g["id_item"]] = []
        elif prec != g["id_item"]:
            dic1[g["id_item"]] = []
        dic1[g["id_item"]].append( (i,g["price"],g["qty"],g["hours"],g["date"]) )
        i+=1

    i=0
    prec=0
    
    for t,g in tmp2.iterrows():
        if type(prec) == type(0):
            prec = g["id_item"]
            dic2[g["id_item"]] = []
            j=0
        elif prec != g["id_item"]:
            dic2[g["id_item"]] = []
            j=0
        dic2[g["id_item"]].append( (i,g["price"],g["qty"],g["hours"],g["date"]) )
        i+=1
        j+=1

 
    for key in dic1:
        if key in dic2:
            n = min(len(dic1[key]),len(dic2[key]))
            for i in range(0,n):
                tmp1.iloc[dic1[key][i][0],4] = dic2[key][n-1-i][1]
                tmp2.iloc[dic2[key][i][0],4] = dic1[key][n-1-i][1]
                tmp1.iloc[dic1[key][i][0],5] = dic2[key][n-1-i][2]
                tmp2.iloc[dic2[key][i][0],5] = dic1[key][n-1-i][2]
                tmp1.iloc[dic1[key][i][0],2] = dic2[key][n-1-i][3]
                tmp2.iloc[dic2[key][i][0],2] = dic1[key][n-1-i][3]
                tmps1 = tmp1.iloc[dic1[key][i][0],1][:-2]
                tmps2 = tmp2.iloc[dic2[key][i][0],1][:-2]
                if int(dic2[key][n-1-i][4][8:]) > 28:
                    tmps1 += str(int(dic2[key][n-1-i][4][8:])-3)
                else:
                    tmps1 += dic2[key][n-1-i][4][8:]

                if int(dic1[key][n-1-i][4][8:]) > 28:
                    tmps2 += str(int(dic1[key][n-1-i][4][8:])-3)
                else:
                    tmps2 += dic1[key][n-1-i][4][8:]

                tmp1.iloc[dic1[key][i][0],1] = tmps1
                tmp2.iloc[dic2[key][i][0],1] = tmps2
    ngt[mois1] = tmp1
    ngt[mois2] = tmp2
        
#        if g["date"] == "date":
#            continue
#        if type(prec) == type(0) :
#            prec=g
#        elif prec["id_item"] != g["id_item"]:
#            i=0
#
#        k=0
#        for f,j in tmp2.iterrows():
#            if j["date"] == "date":
#                continue
#            if g["id_item"] == j["id_item"]:
#               if k != i:
#                   k += 1
#               else:
#                   tmp = g["date"]
#                   g["date"] = j["date"]
#                   j["date"] = tmp
#                   i+=1
#                   break
#        y+=1
#    print(dic1)
#######################################################################

def lissage_date():
    for g in ngt:
        g.date = g.loc[0,"date"]

def new_date(x):
    global indexl
    #print(indexl) 
    dat = gt1.date.unique().tolist()
    #print(dat)
    x = dat[indexl]
    #print(gt1.date)
    if indexl==0:
        indexl+=(len(dat))
    indexl-=1
    #print(indexl)
    return x

def lissage_date_1():
        dat = gt1.date.unique().tolist()
        gt1.apply(new_date, axis=1)
        print(gt1.date)


########################################################

#modif price ==> price btw 0 and 10€ ==> [0:10]
def modif_price():
    for g in ngt:
        g["price"] = g["price"].mean()

def test_del(conc):
    conc["id_user"]= "DEL"


def mul_price(co):
    co["price"] *= co["qty"]
    #co.id_item[co.id_item.str.contains('A')] = "COUCOU"

def suppr_singleton_item():
    for g in ngt:
        print(g["id_user","id_item"])


def gen_new_ids(ngt):
    for gt in ngt:
        new_uids = []
        corresp = {}

        for uid in set(gt['id_user']):
            transacs = []
            if uid == 'DEL':
                corresp[uid] = 'DEL'
            else:
                for row in gt.loc[gt['id_user'] == uid].values:
                    transacs.append(f"{row[0]}{row[1]}{row[2]}{row[3]}{row[4]}{row[5]}")
                htransac = hashlib.sha512(str.encode(random.choice(list(set(transacs))))).hexdigest()
                borne = 0
                while htransac[borne:borne+5] in new_uids and borne < 123:
                    borne += 1
                new_uids.append(htransac[borne:borne+5])
                corresp[uid] = htransac[borne:borne+5]

            gt.loc[gt['id_user'] == uid, 'id_user'] = corresp[uid]
        
############################################################################

if __name__ == "__main__":
    #modif_user(12)
    
    #print(gt1.id_user)
    #print(gt1.price)
    #print(gt1.dtypes)
    gen_new_ids(ngt)
    
    #lissage_date_1()
    #write_data("test_gt1.csv")

    
    #print(gt1["id_item"].value_counts())

    #print(co.id_user)

    #write_data_conc("submission_modif_anthony_new.csv", co)
    for i in range(0,100):
        print(i)
        m1 = random.randint(0,12)
        m2 = m1
        while m2 == m1:
            m2 = random.randint(0,12)
        translation_mois_produit(m1,m2)

    lissage_date()
    co=concat()
    mul_price(co)
    write_data_conc("submission_modif_charly.csv",co)


##  DAY ONLY :
#   U: 0.442389085   R: 0.146618

## WITH ID_USER:
#   U: 0.6380805368572241 R : 0.124857
## WITH REST:
#   U: 0.6826931653  R: 0.11029

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
def lissage_date():
    for g in ngt:
        dat = g.date.unique().tolist()
        ran=random.choice(dat)
        print(ran)
        g.date = ran #0
        #print(g.id_user.count())
    

#######################################################################

def calcul_max_date(g,n):
    #print(g.date.value_counts()[0:3])
    datmonth =[]
    dat = g.date.tolist()
    compte = {k: dat.count(k) for k in set(dat)}
    aux = [ (val,cle) for cle, val in compte.items() ]
    for k in range(n):
        datmonth.append(max(aux))
        aux.remove(max(aux))
    #print(datmonth)
    #print([datmonth[i][1]for i in range(n)])

    #users= g.id_user.unique().tolist()  ## si on veut faire par user
    return datmonth

def lissage_date_update(n):

	for g in ngt:
		datmonth = calcul_max_date(g,n)
		c=0
		undat=g.date.unique().tolist()
		for d in undat: ## users
            #print(d)
			g.loc[g['date'] == d, 'date'] = datmonth[c][1] 
            #print(dat)
			c+=1
			if c==len(datmonth):
				c=0
	return datmonth   

def lissage_hours_update(n):#,liste_date):
	for g in ngt:
		liste_date= calcul_max_date(g,n)
		#print(liste_date)
		hourmonth=[]
		
		for dat in liste_date:
			hour=[]
			for index, row in g.iterrows():
				if row["date"]==dat[1]:
					#print (row["hours"])
					hour.append(row["hours"])
			#print(hour)
			compte = {k: hour.count(k) for k in set(hour)}
			aux = [ (val,cle) for cle, val in compte.items() ]
			#print(aux)
			for k in range(n):
				#print(max(aux))
				hourmonth.append(max(aux))
				aux.remove(max(aux))
			#print(dat ,hourmonth) 
			c=0
			
		undat=g["date"].unique().tolist()
		unhour=g["hours"].unique().tolist()
		#print(unhour)
		for d in undat:
			g.loc[(g['date'] ==d), 'hours'] = hourmonth[c][1]
			c+=1
			if c==len(hourmonth):
				c=0
        #print(hourmonth)
        #print([datmonth[i][1]for i in range(n)])




########################################################

def mul_price(co):
    co["price"] *= co["qty"]
    #co.id_item[co.id_item.str.contains('A')] = "COUCOU"

def mul_price_month():
    for g in ngt:
        g["price"] *= g["qty"]

def lissage_hour():
    for g in ngt:
        hour = g.hours.unique().tolist()
        ran=random.choice(hour)
        print(ran)
        g.hours = ran

def gen_new_ids(ngt):
    for gt in ngt:
        new_uids = []
        corresp = {}

        for uid in set(gt['id_user']):
            transacs = []
            for row in gt.loc[gt['id_user'] == uid].values:
                transacs.append(f"{row[0]}{row[1]}{row[2]}{row[3]}{row[4]}{row[5]}")
            htransac = hashlib.sha512(str.encode(random.choice(list(set(transacs))))).hexdigest()
            borne = 0
            while htransac[borne:borne+5] in new_uids and borne < 123:
                borne += 1
            new_uids.append(htransac[borne:borne+5])
            corresp[uid] = htransac[borne:borne+5]

            gt.loc[gt['id_user'] == uid, 'id_user'] = corresp[uid]


def del_item():
    for g in ngt:
        print(g.id_item.count())

def write_hash_date(i):
    for fil in range(i):
        gen_new_ids(ngt)
        lissage_hours_update(3)
        lissage_date_update(3)
        co=concat()
        mul_price(co)
        write_data_conc("submission_modif_anthony"+str(fil)+".csv", co)
############################################################################

if __name__ == "__main__":
    #gen_new_ids(ngt)
    write_hash_date(1)
    #lissage_hours_update(3)
    #lissage_date_update(3)
    del_item()
    #co=concat()
    #write_data_conc("testdate.csv", co)
    #write_data_conc("essai_date.csv", co)

import numpy as np


#fonction pour recuperer le mois
def get_month(k):
    if int(k[1][:4])==2011:
        return int(k[1][5:7])
    else:
        return 0


def mouette(ground_truth,S):
    print("c'est la fonction mouette du fichier attacun")
    Ffile = np.array([list(set(ground_truth[1:,0]))])

    #le dico permet de faire que chaque id_user de ground truth correspond à un 
    dico_usr_gt = {}
    #print(int(ground_truth[100000,1][:4]))
    #print(Ffile[0])
    list_per_month = [{},{},{},{},{},{},{},{},{},{},{},{},{}]
    for k in S:
        list_per_month[get_month(k)][k[0]]=50
    for i in range (13):
        Ffile=np.append(Ffile,[[list_per_month[i]]*4034],axis=0)
    return Ffile

import numpy as np
from attacun import *

def csv_translate(f):
    list_ret = [[k for k in f[0].keys()]]
    for i in f :
        list_ret.append([])
        for j in i.values():
            list_ret[-1].append(str(j))
    return np.array(list_ret)

def ecart_type(l_gt,l_ps):
    t_gt=len(l_gt)
    t_ps=len(l_ps)
    if t_gt<t_ps:
        return 0
    else :
        l_gt.sort()
        l_ps.sort()
        l_dif = []
        j=0
        for i in l_ps:
            while j<t_gt and l_gt[j]<i:
                j+=1
            if j==t_gt:
                temp = l_gt[len(l_dif)-t_ps:]
                for l in temp:
                    l_dif.append(l)
            else:
                if j>0 and i-l_gt[j-1] < l_gt[j]-i:
                    l_dif.append(l_gt[j-1])
                else:
                    l_dif.append(l_gt[j])
                j+=1
    for i in range (t_ps):
        l_dif[i]-=l_ps[i]
    #Variance
    moy = sum(l_dif)/t_ps
    vari = 0

    for i in l_dif:
        vari += ((i - moy)**2)/t_ps
    v_temp=np.sqrt(vari)
    if v_temp>100:
        return 0
    else :
        return 100-v_temp



def calcul_distance_date_hor(date):
    num_set = set(['0','1','2','3','4','5','6','7','8','9'])
    tot=0
    #On calcul le nombre de minutes avec le début du mois

    for i in range (len(date[1])):
        if date[1][i] not in num_set:
            #heure * 60 + minute
            tot = int(date[1][:i])*60+int(date[1][i+1:])
            break
    #On ajoute le nbr de jour * 1440
    tot += (int(date[0][-2:])-1)*1440

    return tot/(30*1440)*100

def distancehoraireetdate(ground_truth_bis,S_bis):
    print("c'est la fonction qui calcul la distance par rapport a la date et a l'horaire")
    S=csv_translate(S_bis)
    ground_truth=csv_translate(ground_truth_bis)

    liste_idusr_gt=[{},{},{},{},{},{},{},{},{},{},{},{},{}]
    liste_dist_gt=[]


    Ffile=[]
    Ffile.append(list(set(ground_truth[1:,0])))
    
    #On parcours la liste des ffiles partiels
    for month in range (13):
        if len(Ffile) == (month+1):
            Ffile.append([])
            for tt_mettre in range (len(Ffile[0])):
                Ffile[month+1].append({})

    #le dico permet de faire que chaque id_user de ground truth correspond à un 
    dico_usr_gt = {}
    for i in range (len(Ffile[0])):
        dico_usr_gt[Ffile[0][i]]=i
    print("Calcul de distance des gt")
    for i in ground_truth[1:]:
        mois_gt=get_month(i)
        if i[0] not in liste_idusr_gt[mois_gt]:
            liste_idusr_gt[mois_gt][i[0]]=len(liste_dist_gt)
            liste_dist_gt.append([calcul_distance_date_hor([i[1],i[2]])])
        else:
            liste_dist_gt[liste_idusr_gt[mois_gt][i[0]]].append(calcul_distance_date_hor([i[1],i[2]]))
    print("Calcul de distance des ps")
    #Place au PS
    liste_idusr_ps=[{},{},{},{},{},{},{},{},{},{},{},{},{}]
    liste_dist_ps=[]
    
    for i in S[1:]:
        mois_ps=get_month(i)
        if i[0] not in liste_idusr_ps[mois_ps]:
            liste_idusr_ps[mois_ps][i[0]]=len(liste_dist_ps)
            liste_dist_ps.append([calcul_distance_date_hor([i[1],i[2]])])
        else:
            liste_dist_ps[liste_idusr_ps[mois_ps][i[0]]].append(calcul_distance_date_hor([i[1],i[2]]))
    
    print("fin des calcul de distance, place a l'ecart type")
    #Calcul variances
    print("taille du premier mois idusr_ps = ", len(liste_idusr_gt[1]), "taille du premier mois dist_ps", len(liste_idusr_ps[1]))
    for i in range (13):
        for j in liste_idusr_ps[i].keys():
            for k in liste_idusr_gt[i].keys():
                ec_ty = ecart_type(liste_dist_gt[liste_idusr_gt[i][k]],liste_dist_ps[liste_idusr_ps[i][j]])
                Ffile[i+1][dico_usr_gt[k]][j] = ec_ty
                

    print("Fin du bordel")

    
    return Ffile

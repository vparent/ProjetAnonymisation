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
                #print(temp)
                for l in temp:
                    l_dif.append(l)
            else:
                if j>0 and i-l_gt[j-1] < l_gt[j]-i:
                    l_dif.append(l_gt[j-1])
                else:
                    l_dif.append(l_gt[j])
                j+=1
    #print("l_gt", l_gt,"l_ps",l_ps," l_dif", l_dif)
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
    Ffile = np.array([list(set(ground_truth[1:,0]))])

    #le dico permet de faire que chaque id_user de ground truth correspond à un 
    dico_usr_gt = {}
    for i in range (len(Ffile[0])):
        dico_usr_gt[Ffile[0][i]]=i
    #print(dico_usr_gt)
    list_per_month = [{},{},{},{},{},{},{},{},{},{},{},{},{}]
    for k in S[1:]:
        list_per_month[get_month(k)][k[0]]=0
    
    for i in range (13):
        Ffile=np.append(Ffile,[[list_per_month[i]]*4034],axis=0)
    #print(ecart_type([1,2,50,30,32],[5,6,7,27]))
    
    #Liste des distances
    #liste_dist_ps=["rien"]
    liste_idusr_gt=[{},{},{},{},{},{},{},{},{},{},{},{},{}]
    liste_dist_gt=[]
    #dist_max = 0
    ec_ty_max = 0
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
    
    print("fin des calcul de distance, place a l'ecart type\n(enfin la variance car flemme de faire la racine)")
    #Calcul variances
    for i in range (len(liste_idusr_gt)):
        for j in liste_idusr_ps[i].keys():
            for k in liste_idusr_gt[i].keys():
                #Attention ligne supra mega chiaaaaante
                #print("i=",i," j=",j," k=",k,"\nliste_idusr_gt[i][k]",liste_idusr_gt[i][k] )
                ec_ty = ecart_type(liste_dist_gt[liste_idusr_gt[i][k]],liste_dist_ps[liste_idusr_ps[i][j]])
                #print("peut etre avant", ec_ty)
                Ffile[i+1][dico_usr_gt[k]][j] = ec_ty
                if ec_ty != None:
                    if ec_ty > ec_ty_max:
                        ec_ty_max = ec_ty 
    print("Voila le grand calcul final *_* (on met la note sur 100)")
    print(ec_ty_max)
    """for i in range (13):
        for j in range (len(Ffile[i+1])):
            for k in Ffile[i+1][j].keys():
                if Ffile[i+1][j][k]==None:
                    Ffile[i+1][j][k]=0
                else:
                    #print("source du bug ?",(1 - (Ffile[i+1][j][k]/ec_ty_max))*100)
                    Ffile[i+1][j][k] = (1 - (Ffile[i+1][j][k]/ec_ty_max))*100
    """
    print("Fin du bordel")

    """
    for i in S[1:]:
        #Distance de ps a partir du début du mois
        dist_ps = calcul_distance_date_hor([i[1],i[2]])
        mois_ps = get_month(i)
        #print(ground_truth)
        for j in ground_truth[1:]:
            if mois_ps==get_month(j):
                #distance de gt a partir du début du mois
                dist_gt = calcul_distance_date_hor([j[1],j[2]])
                #Calcul du max
                dist_local = abs(dist_gt-dist_ps)
                if dist_max<dist_local:
                    dist_max = dist_local
                #On detourne Ffile qui au lieux de stocker des notes,
                #va stocker des indices(/curseur) sur liste_dist_ps ou seront stocké
                #les distances calculées

                #####choix du mois#choix d'id_user_gt#id_user_ps dans dico
                if Ffile[mois_ps+1][dico_usr_gt[j[0]]][i[0]]==0:

                    Ffile[mois_ps+1][dico_usr_gt[j[0]]][i[0]]=len(liste_dist_ps)
                    liste_dist_ps.append([abs(dist_ps-dist_gt),1])

                else:

                    curseur = Ffile[get_month(i)+1][dico_usr_gt[j[0]]][i[0]]
                    liste_dist_ps[curseur][0]=(liste_dist_ps[curseur][0]*liste_dist_ps[curseur][1]+abs(dist_ps-dist_gt))/(liste_dist_ps[curseur][1]+1)
                    liste_dist_ps[curseur][1]+=1
    print("Distance on été calculé on passe au save")
    for i in Ffile[1:]:
        for j in i:
            for k in j.keys():
                j[k]=liste_dist_ps[j[k]][0]
                
    """
    return Ffile

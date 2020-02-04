import numpy as np
from attacun import *

def csv_translate_qte(f):
    list_ret = [[k for k in f[0].keys()]]
    for i in f :
        list_ret.append([])
        for j in i.values():
            list_ret[-1].append(str(j))
    return np.array(list_ret)

def ecart_decal(ind, l_j, l_gt, l_ps, t_ps, t_gt):
    #print("coucou")
    dist_temp=abs(l_ps[ind]-l_gt[l_j[ind]])#on calcul la distance
    anc_place=int(l_j[ind])#on prend la place en début de fonction
    l_jtemp=int(l_j[ind])#on initialise l_jtemp
    while l_jtemp < t_gt and abs(l_ps[ind]-l_gt[l_jtemp])<=dist_temp:
        l_j[ind]=l_jtemp#si l_jtemp passe on sauvegarde
        dist_temp=abs(l_ps[ind]-l_gt[l_jtemp])
        if ind+1 < t_ps :
            if l_j[ind]+1==l_j[ind+1]:
                bool_t = ecart_decal(ind+1, l_j, l_gt, l_ps, t_ps, t_gt)
                if bool_t:
                    l_jtemp+=1
                else :
                    return False
            else :
                l_jtemp+=1
        else:
            l_jtemp+=1
    if anc_place==l_j[ind]:
        return False
    else :
        return True
"""
def ecart_decal_bis(ind, l_j, l_gt, l_ps, t_ps, t_gt):
    dist_temp=abs(l_ps[ind]-l_gt[l_j[ind]])
    anc_place=l_j[ind]
    l_jtemp=l_j[ind]
    while l_jtemp < t_gt and dist_temp>=abs(l_ps[ind]-l_gt[l_jtemp]):
        l_j[ind]=l_jtemp
        dist_temp=abs(l_ps[ind]-l_gt[l_jtemp])
        if ind+1 < t_ps :
            if l_j[ind]+1==l_j[ind+1]:
                bool_t = ecart_decal(ind, l_j, l_gt, l_ps, t_ps, t_gt)
                if bool_t:
                    l_jtemp+=1
                else :
                    return False
            else :
                l_jtemp+=1
        else:
            l_jtemp+=1
    if anc_place==l_j[ind]:
        return False
    else :
        return True"""


def ecart_type_qte(l_gt,l_ps):
    t_gt=len(l_gt)
    t_ps=len(l_ps)
    l_ret=[]
    if t_gt<t_ps:
        return 100
    
    l_gt.sort()
    l_ps.sort()
    if l_gt[-1]<l_ps[0]:
        l_dif = l_gt[-t_ps:]
        
    else:
        
        l_dif = []
        j=0
        l_j=[]
        for i in l_ps:
            while j<t_gt and l_gt[j]<i:
                j+=1
            if j==t_gt:
                #remontada
                ind=len(l_j)-1
                while ind>=0 and t_gt-l_j[ind]< t_ps-ind :
                    ind-=1
                
                temp = l_gt[t_gt-(t_ps-ind-1):]
                l_dif = l_dif[:ind+1]
                for l in temp:
                    l_dif.append(l)
            else:

                l_j.append(j)
                if j>0 and i-l_gt[j-1] < l_gt[j]-i:
                    l_dif.append(l_gt[j-1])
                else:
                    l_dif.append(l_gt[j])
                j+=1
        """
        #############################
        l_j=[p for  p in range(t_ps)]
        ind = 0
        ecart_decal(ind, l_j, l_gt, l_ps, t_ps, t_gt)
        l_dif=[l_gt[k] for k in l_j]"""


    
    for i in range (t_ps):
        l_ret.append(l_dif[i]-l_ps[i])
    #Variance
    moy = sum(l_ret)/t_ps
    vari = 0

    for i in l_ret:
        vari += ((i - moy)**2)/t_ps
    v_temp=np.sqrt(vari)
    if t_gt != t_ps:
        diff=5
    else:
        diff=0
    #print("l_gt",l_gt,"\nl_ps",l_ps,"\nl_di",l_dif,"\nv_temp",v_temp,"\nmoy",moy,"\ndiff",diff,"diff ldif lps", len(l_dif)-len(l_ps),"l_j",l_j)
    #print(v_temp+abs(moy)+diff)
    #input()
    return v_temp+abs(moy)+diff



def calcul_distance_qte(date):
    #num_set = set(['0','1','2','3','4','5','6','7','8','9'])
    tot=0
    #On calcul le nombre de minutes avec le début du mois
    """
    for i in range (len(date[1])):
        if date[1][i] not in num_set:
            #heure * 60 + minute
            tot = int(date[1][:i])*60+int(date[1][i+1:])
            break
    #On ajoute le nbr de jour * 1440
    """
    tot = (int(date))#*1440

    return tot#/(30*1440)*100

def distanceqte(ground_truth_bis,S_bis):
    print("c'est la fonction qui calcul la distance par rapport a la date et a l'horaire")
    S=csv_translate_qte(S_bis)
    ground_truth=csv_translate_qte(ground_truth_bis)

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
            liste_dist_gt.append([calcul_distance_qte(i[5])])
        else:
            liste_dist_gt[liste_idusr_gt[mois_gt][i[0]]].append(calcul_distance_qte(i[5]))
    print("Calcul de distance des ps")
    #Place au PS
    liste_idusr_ps=[{},{},{},{},{},{},{},{},{},{},{},{},{}]
    liste_dist_ps=[]
    
    for i in S[1:]:
        mois_ps=get_month(i)
        if i[0] not in liste_idusr_ps[mois_ps]:
            liste_idusr_ps[mois_ps][i[0]]=len(liste_dist_ps)
            liste_dist_ps.append([calcul_distance_qte(i[5])])
        else:
            liste_dist_ps[liste_idusr_ps[mois_ps][i[0]]].append(calcul_distance_qte(i[5]))
    
    print("fin des calcul de distance, place a l'ecart type")
    #Calcul ecart type
    ec_tymax=0
    print("taille du premier mois idusr_ps = ", len(liste_idusr_gt[1]), "taille du premier mois dist_ps", len(liste_idusr_ps[1]))
    for i in range (13):
        for j in liste_idusr_ps[i].keys():
            for k in liste_idusr_gt[i].keys():
                ec_ty = ecart_type_qte(liste_dist_gt[liste_idusr_gt[i][k]],liste_dist_ps[liste_idusr_ps[i][j]])
                Ffile[i+1][dico_usr_gt[k]][j] = ec_ty
                if ec_tymax<ec_ty:
                    ec_tymax=ec_ty
    for mois in range (13):
        for nb_gt in range(len(Ffile[mois+1])):
            for id_ps in Ffile[mois+1][nb_gt].keys():
                Ffile[mois+1][nb_gt][id_ps]=(1-( Ffile[mois+1][nb_gt][id_ps] / ec_tymax))*100
                #print("après moy, ecty : ", Ffile[mois+1][nb_gt][id_ps])
    print("ectymax ",ec_tymax)
    print("Fin du bordel")

    
    return Ffile

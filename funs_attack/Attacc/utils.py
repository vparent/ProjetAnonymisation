import numpy as np
import sys
import subprocess
import csv

#On renvoie la moyenne de toute les fonctions
def calcul_moy(list_id,liste_ffile,dico):
   #On isole les coefficient et le diviseur commun pour faire la moyenne
    coef = [k for k in dico.values()]
    divi = sum(coef)
    dico_indice_gt = {}
    dico_idusr_ps=[{},{},{},{},{},{},{},{},{},{},{},{},{}]
    list_note_adr=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
    Ffile = []
    Ffile.append(list_id)
    for indice in range (len(Ffile[0])):
        dico_indice_gt[Ffile[0][indice]] = indice
    #On parcours la liste des ffiles partiels
    for k in range (len(liste_ffile)):
        for month in range (13):
            if len(Ffile) == (month+1):
                Ffile.append([])
                for tt_mettre in range (len(Ffile[0])):
                    Ffile[month+1].append({})
                    
            for num_ps in range (len(liste_ffile[k][0])):
                num_gt = dico_indice_gt[liste_ffile[k][0][num_ps]]
                for id_ps in liste_ffile[k][month+1][num_ps].keys():
                    if id_ps not in Ffile[month+1][num_gt]:
                        Ffile[month+1][num_gt][id_ps] = (coef[k]/divi)*liste_ffile[k][month+1][num_ps][id_ps]
                    else :
                        Ffile[month+1][num_gt][id_ps] += (coef[k]/divi)*liste_ffile[k][month+1][num_ps][id_ps]



                        """
                        if k == len(liste_ffile)-1:
                            if j not in dico_idusr_ps[l-1]:
                                dico_idusr_ps[l-1][j] = len(list_note_adr[l-1])
                                list_note_adr[l-1].append([[Ffile[l][m][j],m]])
                            else:
                                non=1
                                for ij in range (len(list_note_adr[l-1][dico_idusr_ps[l-1][j]])):
                                    if list_note_adr[l-1][dico_idusr_ps[l-1][j]][ij][0]<Ffile[l][m][j]:
                                        non=0
                                        if ij == 0:
                                            list_note_adr[l-1][dico_idusr_ps[l-1][j]]=[[Ffile[l][m][j],m]]+list_note_adr[l-1][dico_idusr_ps[l-1][j]][ij:]
                                            break
                
                                        list_note_adr[l-1][dico_idusr_ps[l-1][j]]=list_note_adr[l-1][dico_idusr_ps[l-1][j]][:ij-1]+[[Ffile[l][m][j],m]]+list_note_adr[l-1][dico_idusr_ps[l-1][j]][ij:]
                                        break
                                if non:
                                    list_note_adr[l-1][dico_idusr_ps[l-1][j]]+=[[Ffile[l][m][j],m]]
    #recherche de max
    print("debut de l'attribution des correspondances finals")
    triplet_max[l,m,j]
    note_max=0
    dejavu={}
    for k in range(13):
        for l in dico_idusr_ps.keys():
            if l in dejavu
    for k in usr_ps:
        dejavu[k]=0
    temp=[]
    for k in range (len(Ffile[0])):
        temp.append([Ffile[0][k]])
        for l in range (1,14):
            chaine=recherche_max_dico(Ffile[l][k],dejavu)
            if chaine == None:
                temp[k].append("DEL")
            else:
                temp[k].append(chaine)
                dejavu[chaine]=1
    
    #Ffile_sorti=np.asarray(temp)
    #numpy.savetxt("Ffile_sorti.csv",Ffile_sorti,fmt="%s",delimeter=",")
    chaine_temp ="id_user,0,1,2,3,4,5,6,7,8,9,10,11,12\n"
    for k in temp:
        for j in k[:-1]:
            chaine_temp+=j+","
        chaine_temp+=k[-1]+"\n"

    mon_fichier = open("Ffile_sorti.csv", "w") # Argh j'ai tout écrasé !
    mon_fichier.write(chaine_temp)
    mon_fichier.close()"""   
    return Ffile

#Fonction qui recherche le maximum d'un dico en prenant en compte une liste discriminante
def recherche_max_dico(dico,dejavu):
    liste_keys=[k for k in dico.keys()]
    note_max=0
    chaine=None
    for i in liste_keys[1:]:
        if True:
            if dico[i] >= note_max:
                note_max = dico[i]
                chaine = i
    return chaine

#Fonction de sortie
def outputffile(Ffile, usr_ps):
    print("output en cours")
    dejavu=[{},{},{},{},{},{},{},{},{},{},{},{},{}]
    for k in usr_ps:
        for l in range (13):
            dejavu[l][k]=0
    temp=[]
    for k in range (len(Ffile[0])):
        temp.append([Ffile[0][k]])
        for l in range (1,14):
            chaine=recherche_max_dico(Ffile[l][k],dejavu[l-1])
            if chaine == None:
                temp[k].append("DEL")
            else:
                temp[k].append(chaine)
                dejavu[l-1][chaine]=1
    
    chaine_temp ="id_user,0,1,2,3,4,5,6,7,8,9,10,11,12\n"
    for k in temp:
        for j in k[:-1]:
            chaine_temp+=j+","
        chaine_temp+=k[-1]+"\n"

    mon_fichier = open("Ffile_sorti.csv", "w") # Argh j'ai tout écrasé !
    mon_fichier.write(chaine_temp)
    mon_fichier.close()

#On recupere le nom des fonctions dans le fichier attac.conf
def recup_fonc():
    file_recup = open("attac.conf", "r")
    dico = {}
    k=[2,3]
    ligne_entier = file_recup.readlines()
    for ligne in ligne_entier:
        if ligne[0] != "#":
            for i in range(len(ligne)):
                if ligne[i] == " ":
                    dico[str(ligne[i+1:len(ligne)-1])] = int(ligne[0:i])
    print("Le dico",dico)

    return dico

#Fonction qui récupère le fichier .csv
def csv_getter(f):
    with open(f, 'r') as truth:
        reader = csv.DictReader(truth)
        rows = []
        for r in reader:
            rows.append(r)
    return rows


            
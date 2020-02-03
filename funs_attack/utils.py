import numpy as np
import sys
import subprocess
import csv
import os
import ast

def recherche_max_ffile(dico_idusr_ps,list_note_adr,dejavu_ps,dejavu_gt):
    combo_max=[-2,-2,None]
    #print(list_note_adr)
    for id_ps in dico_idusr_ps.keys():
        if id_ps not in dejavu_ps:
            for note_adr in list_note_adr[dico_idusr_ps[id_ps]]:
                if note_adr[1] not in dejavu_gt:
                    if combo_max[0]<=note_adr[0]:
                        combo_max[0]=note_adr[0]
                        combo_max[1]=note_adr[1]
                        combo_max[2]=id_ps
                    break
    return combo_max



def output_name(name):
    name_r=name[6:-4]
    for i in range (len(name_r)):
        if name_r[i]=='S':
            if i< len(name_r):
                name_r=name_r[:i]+'F'+name_r[i+1:]
    print(name_r)
    return "resultat/"+name_r+"-LCOINSTI.csv"

def extract_name(name):
    name_r=name[6:-4]
    
    print(name_r)
    return name_r


#On renvoie la moyenne de toute les fonctions
def calcul_moy(list_id,liste_ffile,coef):
    #On isole les coefficient et le diviseur commun pour faire la moyenne
    divi = sum(coef)
    dico_indice_gt = {}
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
    return Ffile

def output_bis(Ffile):
    dico_idusr_ps=[{},{},{},{},{},{},{},{},{},{},{},{},{}]
    list_note_adr=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
    dejavu_gt=[set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set()]
    dejavu_ps=[set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set()]
    combo_max=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for month in range(13):
        for nb_gt in range(4034):
            for id_ps in Ffile[month+1][nb_gt]:
                if id_ps not in dico_idusr_ps[month]:
                    dico_idusr_ps[month][id_ps] = len(list_note_adr[month])
                    list_note_adr[month].append([[Ffile[month+1][nb_gt][id_ps],nb_gt]])
                    #print("id_ps in ",list_note_adr[month],"id_ps", id_ps)
                    #input()
                else:
                    non=1
                    for ij in range (len(list_note_adr[month][dico_idusr_ps[month][id_ps]])):
                        if list_note_adr[month][dico_idusr_ps[month][id_ps]][ij][0]<Ffile[month+1][nb_gt][id_ps]:
                            non=0
                            if ij == 0:
                                list_note_adr[month][dico_idusr_ps[month][id_ps]]=[[Ffile[month+1][nb_gt][id_ps],nb_gt]]+list_note_adr[month][dico_idusr_ps[month][id_ps]]
                                
                                break
                            else:
                                list_note_adr[month][dico_idusr_ps[month][id_ps]]=list_note_adr[month][dico_idusr_ps[month][id_ps]][:ij-1]+[[Ffile[month+1][nb_gt][id_ps],nb_gt]]+list_note_adr[month][dico_idusr_ps[month][id_ps]][ij:]
                                
                                break
                    if non:
                        list_note_adr[month][dico_idusr_ps[month][id_ps]]+=[[Ffile[month+1][nb_gt][id_ps],nb_gt]]
                        
    #recherche de max
    print("On DEL tout")
    for k in range (13):
        for l in range (4034):
            Ffile[k+1][l]="DEL"
    print(Ffile[2][4])
    print("debut de l'attribution des correspondances finals")
    month_max = [-1,-1]
    for k in range (13):
        combo_max[k]=recherche_max_ffile(dico_idusr_ps[k],list_note_adr[k],dejavu_ps[k],dejavu_gt[k])
        if combo_max[k] != None:
            if combo_max[k][0]>=month_max[0]:
                month_max[0]=combo_max[k][0]
                month_max[1]=k
    print("init fait passe au gros calcul")
    while month_max[1]!=(-1):
        mois=month_max[1]
        #print("nb de ps",sum([len(k) for k in dejavu_ps]), "mois utilisé", mois)
        
        nb_gt=combo_max[month_max[1]][1]
        id_ps=combo_max[month_max[1]][2]
        Ffile[mois][nb_gt]=id_ps
        print("mois",mois,"id_ps", id_ps, "nb_gt", nb_gt,"ffile",Ffile[mois][nb_gt])
        dejavu_gt[mois].add(nb_gt)
        dejavu_ps[mois].add(id_ps)
        combo_max[mois]=recherche_max_ffile(dico_idusr_ps[mois],list_note_adr[mois],dejavu_ps[mois],dejavu_gt[mois])
        month_max = [-1,-1]
        for k in range (13):
            if combo_max[k] != None:
                if combo_max[k][0]>month_max[0]:
                    month_max[0]=combo_max[k][0]
                    month_max[1]=k
    
    chaine_temp ="id_user,0,1,2,3,4,5,6,7,8,9,10,11,12\n"
    
    for k in range(4034):
        for l in range(13):
            chaine_temp+=Ffile[l][k]+","
        chaine_temp+=Ffile[l][13]+"\n"

    mon_fichier = open("Ffile_sorti.csv", "w") # Argh j'ai tout écrasé !
    mon_fichier.write(chaine_temp)
    mon_fichier.close()

#Fonction qui recherche le maximum d'un dico en prenant en compte une liste discriminante
def recherche_max_dico(dico,dejavu):
    liste_keys=[k for k in dico.keys()]
    #print(liste_keys)
    note_max=0
    chaine=None
    for i in liste_keys:
        if True:
            if dico[i] > note_max:
                note_max = dico[i]
                chaine = i
    return chaine

#Fonction de sortie
def outputffile(Ffile_bis, usr_ps,nom):
    print("output en cours")
    dejavu=[{},{},{},{},{},{},{},{},{},{},{},{},{}]
    for k in usr_ps:
        for l in range (13):
            dejavu[l][k]=0
    temp=[]
    for k in range (len(Ffile_bis[0])):
        temp.append([Ffile_bis[0][k]])
        for l in range (13):
            chaine=recherche_max_dico(Ffile_bis[l+1][k],dejavu[l])
            if chaine == None:
                temp[k].append("DEL")
            else:
                temp[k].append(chaine)
                dejavu[l][chaine]=1
            #print(len(temp[k]))
    
    chaine_temp ="id_user,0,1,2,3,4,5,6,7,8,9,10,11,12\n"
    for k in temp:
        for j in k[:-1]:
            chaine_temp+=j+","
        chaine_temp+=k[-1]+"\n"

    mon_fichier = open(nom, "w") # Argh j'ai tout écrasé !
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

def output_ffile_temp(nom_fonc,nom_fichier,Ffile):
    #nomfonction_nomfichier.csv
    nom_util = "temp/"+nom_fonc+"_"+nom_fichier+".txt"
    #print("nom_util",nom_util)
    mon_fichier = open(nom_util, "w")
    mon_fichier.write(str(Ffile))
    mon_fichier.close()

def input_ffile_temp(nom_fonc,nom_fichier):
    #nomfonction_nomfichier.csv
    nom_util = "temp/"+nom_fonc+"_"+nom_fichier+".txt"
    mon_fichier = open(nom_util, "r")
    Ffile = ast.literal_eval(mon_fichier.read())
    mon_fichier.close()
    return(Ffile)
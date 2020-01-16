import numpy as np
import sys
import subprocess

#On renvoie la moyenne de toute les fonctions
def calcul_moy(Ffile,liste_ffile,dico):

    #On isole les coefficient et le diviseur commun pour faire la moyenne
    coef = [k for k in dico.values()]
    divi = sum(coef)
    #On parcours la liste des ffiles partiels
    for k in range (len(liste_ffile)):

        #On parcours le Ffile
        for l in range (1, len(Ffile)):
            for m in range (len(Ffile[l])):

                #Pour chaque dico on regroupe les id_user commun
                
                id_com = [i for i in Ffile[l][m].keys()]
                for j in id_com:
                    Ffile[l][m][j] = (coef[k]/divi)*liste_ffile[k][l][m][j]
    return Ffile

#Fonction qui recherche le maximum d'un dico en prenant en compte une liste discriminante
def recherche_max_dico(dico,dejavu):
    #print(dico)
    liste_keys=[k for k in dico.keys()]
    #print(liste_keys)
    note_max=0
    chaine=None
    for i in liste_keys[1:]:
        #print(i)
        if dejavu[i]==0:
            if dico[i] >= note_max:
                note_max = dico[i]
                chaine = i
    return chaine

#Fonction de sortie
def outputffile(Ffile, usr_ps):
    print("output en cours")
    dejavu={}
    for k in usr_ps:
        dejavu[k]=0
    temp=[]
    for k in range (len(Ffile[0])):
        temp.append([Ffile[0][k]])
        for l in range (1,13):
            chaine=recherche_max_dico(Ffile[l][k],dejavu)
            if chaine == None:
                temp[k].append("DEL")
            else:
                temp[k].append(chaine)
                dejavu[chaine]=1
    
    #Ffile_sorti=np.asarray(temp)
    #numpy.savetxt("Ffile_sorti.csv",Ffile_sorti,fmt="%s",delimeter=",")
    chaine_temp =""
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
    ligne_entier = file_recup.readlines()
    for ligne in ligne_entier:
        for i in range(len(ligne)):
            if ligne[i] == " ":
                dico[str(ligne[i+1:len(ligne)])] = int(ligne[0:i])
    return dico
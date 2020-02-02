import numpy as np
import sys
import csv
import subprocess

#Fonction pour tout importer
def import_all(directory):

    #On récupère tout les fichiers/dossiers d'un dossier
    ls_result = subprocess.check_output(["ls", directory])
    ls_result = str(ls_result)[2:-3].split("\\n")

    #Si il n'y a rien
    if ls_result==['']:
        return None
    
    #On parcours la liste pour discerner les .py et les dossiers
    #(c'est un dossier si il n'y a pas de '.')
    list_ret = []
    local = []
    for k in ls_result:
        not_dot = 1
        for l in range (len(k)):

            #si il y a un '.'
            if k[l]=='.':
                not_dot = 0

                #Si c'est un '.py'
                if k[-3:]==".py":
                    local.append(k[:-3])
                break
        
        #Si c'est un dossier on fait un appel récursif
        if not_dot:
            i = import_all(directory+k+'/')
            #Récupère la liste si != None
            if i!=None:
                list_ret.append(i[0])
    
    #Récupère la liste locale si elle a quelque chose
    if len(local)>0:
        list_ret.append([[directory],local])
    #On renvoie la liste globale si il y a quelque chose :
    # du dossier actuel et des sous dossiers
    if len(list_ret)>0:
        return list_ret


def main():
    

    #on recupere les fichiers
    ground_truth = csv_getter('ground_truth.csv')





    #########################
    #Fichier S a attaquer !!#
    #########################
    S = csv_getter('ground_truth.csv')
    
    
    



    usr_ps= np.array(list(set(csv_translate(S)[1:,0])))

    #for k in range
    dico = recup_fonc()

    liste_ffile=[]
    for k in dico.keys():
        exec("liste_ffile.append("+k+"(ground_truth,S))")
    
    
    print("On fait la moyenne")
    Ffile_bis = calcul_moy(list(set(csv_translate(ground_truth)[1:,0])),liste_ffile,dico)
    print("go to output")
    #output_bis(Ffile_bis)
    outputffile(Ffile_bis,usr_ps)
    
#On appel la fonction qui importe tout
list_fonc = import_all('./')
for i in list_fonc:
    sys.path.append(i[0][0])
    for k in i[1]:
        if k !="attac_com":
            exec("from "+k+" import *")
main()


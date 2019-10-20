
def test():
	data = open("../darc_aicrowd-master/data/ground_truth.csv", 'r')

	lignes = data.readlines()
	for ligne in lignes:
		ligne.replace('\n', '')
		donnees = ligne.split(',')
		for d in donnees:
			donnees[-1] = donnees[-1].rstrip('\n')
		print(donnees)
	data.close()

if __name__ == "__main__":
	test()

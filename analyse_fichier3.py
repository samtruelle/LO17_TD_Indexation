from pandas import read_csv

csv = read_csv('fichier3.csv')

tfidf__mean = csv.groupby(['mot_i'])['tf_idf_i_j'].mean()
tfidf__mean.to_csv('tfidf__mean.csv', header=True)
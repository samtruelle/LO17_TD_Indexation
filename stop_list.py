import csv
from itertools import groupby
from math import log10

from lxml import objectify

with open('filename.xml') as xml_fdesc:
    corpus = objectify.fromstring(xml_fdesc.read())

N = 0  # nb de fichiers

tf = dict()  # pour chaque article, mot => nb occurence mot

for bulletin in corpus['bulletin']:
    N += 1
    interesting_words = \
        bulletin['titre'].text.split(" ") + bulletin['texte'].text.split(" ")
    interesting_words = \
        ["".join(list(filter(str.isalnum, word)))
         for word in interesting_words]
    interesting_words = \
        sorted([word.strip().lower()
                for word in interesting_words
                if word != ''])
    tf[bulletin['fichier']] = \
        {key: len(list(group))
         for key, group in
         groupby(interesting_words)}

# print(tf)

df = dict()  # mot => nb d'article contenant ce mot

for key, words in tf.items():
    for word in words.keys():
        if word in df:
            df[word] += 1
        else:
            df[word] = 1

# print(df)

idf = dict()
for word in df.keys():
    idf[word] = log10(N / df[word])

# print(idf)

tfid = dict()
for fichier, article in tf.items():
    tfid[fichier] = \
        {word: nb_occurence * idf[word]
         for word, nb_occurence in article.items()}

with open('fichier1.csv', 'w+') as csv_fdesc:
    fieldnames = ['nom_du_fichier_article', 'mot_i', 'tf_i,j']
    csv_writer = csv.DictWriter(csv_fdesc, fieldnames=fieldnames)

    csv_writer.writeheader()

    for fichier, article in tf.items():
        for word, nb_occurence in article.items():
            csv_writer.writerow(
                {'nom_du_fichier_article': fichier,
                 'mot_i': word,
                 'tf_i,j': nb_occurence})

with open('fichier2.csv', 'w+') as csv_fdesc:
    fieldnames = ['mot_i', 'idf_i']
    csv_writer = csv.DictWriter(csv_fdesc, fieldnames=fieldnames)

    csv_writer.writeheader()

    for word, nb_occurence in idf.items():
        csv_writer.writerow({'mot_i': word, 'idf_i': nb_occurence})

with open('fichier3.csv', 'w+') as csv_fdesc:
    fieldnames = ['nom_du_fichier_article', 'mot_i', 'tf_idf_i_j']
    csv_writer = csv.DictWriter(csv_fdesc, fieldnames=fieldnames)

    csv_writer.writeheader()

    for fichier, article in tfid.items():
        for word, tf_x_idf_i_j in article.items():
            csv_writer.writerow(
                {'nom_du_fichier_article': fichier,
                 'mot_i': word,
                 'tf_idf_i_j': tf_x_idf_i_j})

import csv

THIRD_Q_THRESHOLD = 2.513


def get_interesting_words():
    with open('fichier2.csv') as fdesc:
        csv_reader = csv.DictReader(fdesc, delimiter=',')

        for row in csv_reader:
            if float(row['idf_i']) >= THIRD_Q_THRESHOLD:
                yield row['mot_i']


def remove_words(s, interesting_words):
    final_s = []
    for word in s.split(" "):
        if "".join(list(filter(str.isalnum, word))) in interesting_words:
            final_s.append(word)
    return " ".join(final_s)



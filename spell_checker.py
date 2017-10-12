import urllib.request


class Lexicon():
    def __init__(self, lines):
        # word => lemma
        self.lexicon = {line[0].strip(): line[1].strip() for line in lines}
        self.proximity_threshold = 50
        self.proximity_letters_threshold = 2
        self.levenshtein_distance_threshold = 1e-10

    def get(self, word):
        lemma = self.lexicon.get(word.lower())

        if lemma is None:
            # compute proximities
            candidates = \
                {lemma_: self.proximity(word, lexicon_word)
                 for lexicon_word, lemma_ in self.lexicon.items()}
            candidates = \
                Lexicon.filter_candidates(self.proximity_threshold, candidates)
            if len(candidates) > 0:
                return candidates

            # compute levenshtein distance
            candidates = \
                {lemma_: Lexicon.levenshtein_distance(word, lexicon_word)
                 for lexicon_word, lemma_ in self.lexicon.items()}
            candidates = {lemma: dist
                          for lemma, dist in candidates.items() if dist > 0}
            candidates = \
                Lexicon.filter_candidates(self.levenshtein_distance_threshold,
                                          candidates)
            if len(candidates) > 0:
                return candidates

        return lemma

    def proximity(self, word1, word2):
        if len(word1) < self.proximity_letters_threshold and len(
                word2) < self.proximity_letters_threshold:
            return 0
        if abs(len(word1) - len(word2)) > self.proximity_letters_threshold:
            return 0

        i = 1
        while i < min(len(word1), len(word2)) and word1[i] == word2[i]:
            i += 1

        return i * 100 / max(len(word1), len(word2))

    @staticmethod
    def levenshtein_distance(word1, word2):
        h = len(word1) + 1  # rows
        w = len(word2) + 1  # columns
        d = [[0 for x in range(w)] for y in range(h)]

        for i in range(len(word1)):
            d[i][0] = i
        for j in range(len(word2)):
            d[0][j] = j

        for i in range(1, len(word1)):
            for j in range(1, len(word2)):
                if word1[i] == word2[j]:
                    substitution_cost = 0
                else:
                    substitution_cost = 1
                d[i][j] = min([
                    d[i - 1][j] + 1,  # delete new char of word1
                    d[i][j - 1] + 1,  # insert in word1 new char of word2
                    d[i - 1][j - 1] + substitution_cost  # substitution
                ])
        return d[len(word1)][len(word2)]

    @staticmethod
    def filter_candidates(threshold, candidates):
        max_distance = threshold
        lemmas = []
        for lemma_, distance in candidates.items():
            if distance > max_distance:
                max_distance = distance
                lemmas = [lemma_]
            if distance == max_distance:
                lemmas.append(lemma_)
        print(max_distance)
        return lemmas


def get_lexicon(download=False):
    if download:
        opener = urllib.request.FancyURLopener({})
        filtre_corpus_url = "http://www4.utc.fr/~lo17/TELECHARGE/" \
                            "TDANAMORPHO/filtreCorpus_P16.txt"
        with opener.open(filtre_corpus_url) as fdesc:
            file = fdesc.read().decode('utf-8')
    else:
        with open('filtreCorpus_P16.txt') as fdesc:
            file = fdesc.read()
    return [line.split('\t') for line in file.split('\n')
            if len(line.split('\t')) == 2]


if __name__ == '__main__':
    lexicon = Lexicon(get_lexicon())
    word = None
    while word != '':
        word = input().strip()
        lemma = lexicon.get(word)
        if lemma is None:
            print(word, "inconnu du lexique")
        else:
            print(word, lemma, sep=":\t")

    # TODO: print distance matrix for 2 words to understand why values are all 0

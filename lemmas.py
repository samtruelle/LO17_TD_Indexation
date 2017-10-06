def compute_successors(words: list):
    for inspected_word in words:
        successors = list()
        for idx, _ in enumerate(inspected_word):
            # letters that are different for the words with same prefix
            different_letters = \
                {word[idx + 1] for word in words
                 if len(word) > idx + 1
                 and inspected_word[:idx + 1] == word[:idx + 1]}
            nb_different_letter = len(different_letters)
            if nb_different_letter > 9:
                nb_different_letter = 9
            successors.append(nb_different_letter)
        yield inspected_word, successors


def compute_lemmas(successors_dict: dict):
    for inspected_word, list_successeur in successors_dict.items():
        idx_succ_max = 0
        val_succ_max = -9
        for idx, successor in enumerate(list_successeur):
            if successor == 1 \
                    and len(list_successeur) > idx + 1 \
                    and list_successeur[idx + 1] > val_succ_max:
                val_succ_max = successor
                idx_succ_max = idx
        yield inspected_word, inspected_word[:idx_succ_max]


if __name__ == '__main__':
    import argparse

    parser = \
        argparse.ArgumentParser(
            description="Computes lemmas of a list of words.")
    parser.add_argument("words", nargs="+")
    args = parser.parse_args()

    words = sorted(list(set(args.words)))

    successors_dict = \
        {word: successors for word, successors in compute_successors(words)}

    lemmas_dict = \
        {word: lemme for word, lemme in compute_lemmas(successors_dict)}

    for word, successors in sorted(successors_dict.items(), key=lambda x: x[0]):
        print(word, ''.join(str(x) for x in successors), lemmas_dict[word],
              sep=";")

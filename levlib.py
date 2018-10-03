import re


def lev(s, t):
    ''' From Wikipedia article; Iterative with two matrix rows. '''
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
    return v1[len(t)]


def levs(compare_to, list_to_compare):
    levs = []
    for compare in list_to_compare:
        levs.append(lev(compare_to, compare))
    return levs


def closest_to(string, list):
    results = levs(string, list)
    return list[results.index(min(results))]


def tv_match(string, tv_list):
    def treatment(str):
        return str.lower().replace(".", " ").replace("_", " ")

    a = treatment(string)
    all_words = a.split()

    best_match = closest_to(a, tv_list)
    best_match_without_date = re.sub(" \(\d+\)", "", best_match)
    best_match_without_date_words = best_match_without_date.split()
    biggest_word_in_best_match = treatment(max(best_match_without_date_words, key=len))

    if biggest_word_in_best_match in all_words:
        return best_match
    else:
        return None

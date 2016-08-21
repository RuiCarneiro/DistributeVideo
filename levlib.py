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


def levs(compareTo, listToCompare):
    levs = []
    for compare in listToCompare:
        levs.append(lev(compareTo, compare))
    return levs

def closestTo(string, list):
    results = levs(string, list)
    return list[results.index(min(results))]


def tvMatch(string, tvList):
    def treatment(T):
        return T.lower().replace(".", " ").replace("_", " ")

    a = treatment(string)
    aWords = a.split()

    bestMatch = closestTo(a, tvList)
    bestMatchWords = bestMatch.split()
    biggestWordInBestMatch = treatment(max(bestMatchWords, key=len))

    if biggestWordInBestMatch in aWords:
        return bestMatch
    else:
        return None

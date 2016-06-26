def lev(s1, s2):
    l1 = len(s1)
    l2 = len(s2)

    matrix = [range(l1 + 1)] * (l2 + 1)
    for zz in range(l2 + 1):
        matrix[zz] = range(zz, zz + l1 + 1)
    for zz in range(0, l2):
        for sz in range(0, l1):
            if s1[sz] == s2[zz]:
                matrix[zz + 1][sz + 1] = min(matrix[zz + 1][sz] + 1, matrix[zz][sz + 1] + 1, matrix[zz][sz])
            else:
                matrix[zz + 1][sz + 1] = min(matrix[zz + 1][sz] + 1, matrix[zz][sz + 1] + 1, matrix[zz][sz] + 1)
    return matrix[l2][l1]


def levs(compareTo, listToCompare):
    levs = []
    for compare in listToCompare:
        levs.append(lev(compareTo, compare))
    return levs


def closestTo(string, list):
    results = levs(string, list)
    return list[results.index(min(results))]


def tvMatch(string, list):
    bestMatch = closestTo(string, list)
    bestMatchWords = bestMatch.split()
    biggestWordInBestMatch = max(bestMatchWords, key=len)
    if biggestWordInBestMatch in string:
        return bestMatch
    else:
        return None

if __name__ == '__main__':
    print levs('abc', ['acsdqwe', 'iqweu', 'abd', 'aaa'])
    print closestTo('12312', ['Game of', 'Thrones', 'Game of Thr', 'Game'])
    print tvMatch("/asudhas/asdasd/Game.of.Thrones.aabc.mkv", ["Game of War", "Game of Thrones"])
    pass

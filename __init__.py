import datetime
import json
import os
import re
import levlib


# settings
tvPath = ""
moviesPath = ""
downloadsPath = ""
moveCommand = "mv"
bigFile = 100.0
smallFile = 30.0

# data
videoExtensions = []
subtitlesExtensions = []


def moveFile(frm, to):
    def escapeChars(string):
        return string.replace(" ", "\\ ")
    print(":: " + moveCommand + " " + escapeChars(frm) + " " + escapeChars(to))


def filesInDirWithExtension(dir, extensions):
    files = []
    for file, f, s in os.walk(dir):
        fileExtension = os.path.splitext(file)[1:]
        if fileExtension in extensions:
            files.append(file)
    return files


def distributeFile(file):
    def moveTv(frm):
        fileName = os.path.basename(frm)
        show = levlib.tvMatch(fileName, tvShows())
        if show is not None:
            path = tvPath + "/" + show
            moveFile(frm, path)
        else:
            print("No TV show for it")
    #
    fileSize = os.path.getsize(file) / (1048576.0)
    extension = os.path.splittext(file)[1:]
    isSubtitle = extension in subtitlesExtensions
    isBigFile = fileSize >= bigFile
    isSeries = False
    if re.match(file, "(S|s)\d+(E|e)\d+"):
        isSeries = True
    if re.match(file, "\d+x\d+"):
        isSeries = True
    dest = ""
    # distribute
    if isSubtitle:
        if (isSeries):
            dest = "tv"
        else:
            dest = "movie"
    else:
        if isSeries:
            dest = "tv"
        elif isBigFile:
            dest = "movie"
        else:
            dest = ""
    # move file
    if dest == "movie":
        moveFile(file, moviesPath)


def startDistribution():
    print("Scanning files...")
    extensions = videoExtensions + subtitlesExtensions
    files = filesInDirWithExtension(downloadsPath, extensions)
    for file in files:
        print("* " + file)
        distributeFile(file)
        print("")
    print("Done")


def tvShows():
    tvShows = []
    for x in os.listdir(tvShows):
        if os.path.isdir(x):
            tvShows.append(x)
    str = "TV Shows: "
    for show in tvShows:
        str = str + show + " "
    print(str)
    return tvShows


if __name__ == '__main__':
    print("Distribute Video")
    now = datetime.datetime.now().isoformat()
    print("Running on " + now)
    with open('data.json') as dataFile:
        data = json.load(dataFile)
        videoExtensions = data["video"]
        subtitlesExtensions = data["subtitles"]
    with open('config.json') as configFile:
        data = json.load(configFile)
        tvPath = data['tv']
        moviesPath = data['movies']
        downloadsPath = data['downloads']
        bigFile = data["bigfile"]
        smallFile = data["smallfile"]
        moveCommand = data["command"]
        startDistribution()
    print("End")

import datetime
import json
import os
import re
import sys

tvPath = None
tvShows = None
moviesPath = None
downloadsPath = None
moveCommand = ""
bigFile = 100.0



def filesInDirWithExtension(dir, extensions):
    files = []
    for file, f, s in os.walk(dir):
        fileExtension = os.path.splitext(file)[1:]
        if fileExtension in extensions:
            print("* " + file)
            files.append(file)
    return files


def distributeFile(file, subtitlesExtensions):
    dirName = os.path.dirname(file)
    fileName = os.path.basename(file)
    fileSize = os.path.getsize(file)/(1048576.0)
    extension = os.path.splittext(file)[1:]
    subtitlesExtensionsSet = set(subtitlesExtensions)
    isSubtitle = extension in subtitlesExtensionsSet
    isBigFile = fileSize > bigFile
    isSeries = False
    if re.match(file, "(S|s)\d+(E|e)\d+"):
        isSeries = True
    if re.match(file, "\d+x\d+"):
        isSeries = True
    dest = ""
    # distribute
    if isSubtitle:
        if(isSeries):
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



def startDistribution():
    with open('data.json') as dataFile:
        data = json.load(dataFile)
        videoExtensions = data["video"]
        subtitlesExtensions = data["subtitles"]
        extensions = set(videoExtensions + subtitlesExtensions)
        print("Scanning files...")
        files = filesInDirWithExtension(downloadsPath, extensions)
        for file in files:
            print("* " + file)
            distributeFile(file, subtitlesExtensions)
            print("")
        print("Done")


def populateTvShows():
    tvShows = []
    for x in os.listdir(tvShows):
        if os.path.isdir(x):
            tvShows.append(x)
    str = "TV Shows: "
    for show in tvShows:
        str = str + show + " "
    print(str)


if __name__ == '__main__':
    print("Distribute Video")
    now = datetime.datetime.now().isoformat()
    print("Running on " + now)
    with open('config.json') as configFile:
        data = json.load(configFile)
        tvPath = data['tv']
        moviesPath = data['movies']
        downloadsPath = data['downloads']
        bigFile = data["bigfile"]
        moveCommand = data["command"]
        startDistribution()
    print("End")

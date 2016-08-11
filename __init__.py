import json
import os
import re
import levlib
import glob
import fnmatch
import subprocess

# configuration
tvPath = ""
moviesPath = ""
downloadsPath = ""

#constants
bigFile = 104857600  # 100MB

# data
videoExtensions = []
subtitlesExtensions = []

#re's
seriesRE1 = ".*(S|s)\d+(E|e)\d+.*"
seriesRE2 = ".*\d+x\d+.*"

#globals
debugTvSeriesNames = False


def runProc(command, args):
    if type(command) is str:
        command = [command]
    if type(args) is str:
        args = [args]
    cmd = command + args
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out, err


def moveFile(x, y):
    args = ['-u', x, y]
    o, e = runProc('mv', args)
    if e is not None:
        return -1
    return o, e


def listFiles(dir):
    files = []
    for file in glob.iglob(dir + "/**/*", recursive=True):
        files.append(file)
    return files


def filesInDirWithExtension(dir, extensions):
    files = []
    for file in listFiles(dir):
        for extension in extensions:
            if fnmatch.fnmatch(file, "*." + extension):
                files.append(file)
    return files


def distributeFile(file):
    fileName = os.path.basename(file)
    # is big
    isBigFile = os.path.getsize(file) >= bigFile
    # is subtitle
    isSubtitle = False
    for subtitleExtension in subtitlesExtensions:
        if fnmatch.fnmatch(file, "*." + subtitleExtension):
            isSubtitle = True
    # is series
    isSeries = False
    if re.match(seriesRE1, fileName):
        isSeries = True
        m = re.search("(.*)([sS]\d)", fileName)
        if m:
            seriesName = m.group(1)
    if re.match(seriesRE2, fileName):
        isSeries = True
        m = re.search("(.*)(\d+x\d+)", fileName)
        if m:
            seriesName = m.group(1)
    # select destination
    dest = ""
    if isSubtitle:
        if isSeries:
            dest = "tv"
        else:
            dest = "movie"
    else:
        if isSeries:
            dest = "tv"
        elif isBigFile:
            dest = "movie"
        else:
            dest = "small"
    # move file
    if dest == "movie":
        print("  ✔︎ Movies")
        moveFile(file, moviesPath)
    elif dest == "tv":
        tvSeries = levlib.tvMatch(seriesName, tvShows())
        if tvSeries is not None:
            print("  ✔︎ TV Series: " + tvSeries)
            moveFile(file, tvPath + "/" + tvSeries)
        else:
            print("  ✘ No appropiate TV Series folder found. Left there.")
            global debugTvSeriesNames
            debugTvSeriesNames = True
    elif dest == "small":
        print("  ✘ Probably a sample file. Left there.")


def startDistribution():
    extensions = videoExtensions + subtitlesExtensions
    files = filesInDirWithExtension(downloadsPath, extensions)
    for file in files:
        print("  ➤ " + file)
        distributeFile(file)
        print("")


def tvShows():
    tvShows = []
    for x in os.listdir(tvPath):
        if os.path.isdir(tvPath + "/" + x):
            tvShows.append(x)
    return tvShows


if __name__ == '__main__':
    try:
        with open('data.json') as dataFile:
            data = json.load(dataFile)
            videoExtensions = data["video"]
            subtitlesExtensions = data["subtitles"]
    except:
        raise SystemExit("data.json file not found or invalid.")
    try:
        with open('config.json') as configFile:
            data = json.load(configFile)
            tvPath = data['tv']
            moviesPath = data['movies']
            downloadsPath = data['downloads']
    except:
        raise SystemExit("config.json file not found or invalid.")
    startDistribution()
    if debugTvSeriesNames:
        series = tvShows()
        print("")
        print("You have the following TV Series folders:")
        for s in series:
            print("   • " + s)

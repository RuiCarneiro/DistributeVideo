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
processedList = False

#constants
bigFile = 104857600  # 100MB

# data
videoExtensions = ["mkv", "avi", "mp4", "m4v", "mov"]
subtitlesExtensions = ["srt", "ass", "ssa", "smi", "sub", "idx", "vob"]

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
        return True
    elif dest == "tv":
        tvSeries = levlib.tvMatch(seriesName, tvShows())
        if tvSeries is not None:
            print("  ✔︎ TV Series: " + tvSeries)
            moveFile(file, tvPath + "/" + tvSeries)
            return True
        else:
            print("  ✘ No appropiate TV Series folder found. Left there.")
            global debugTvSeriesNames
            debugTvSeriesNames = True
            return False
    elif dest == "small":
        print("  ✘ Probably a sample file. Left there.")
        return True
    return False


def startDistribution():
    processedListFilePath = downloadsPath + "/.dvprocessed"
    extensions = videoExtensions + subtitlesExtensions
    files = filesInDirWithExtension(downloadsPath, extensions)
    #processedList
    processedFiles = []
    if processedList:
        try:
            with open(processedListFilePath) as processedListFile:
                processedFiles = processedListFile.read().splitlines()
                processedListFile.close()
        except:
            processedListFile = open(processedListFilePath, 'w')
            processedListFile.close()
    #file by file
    for file in files:
        if file not in processedFiles:
            print("  ➤ " + file)
            result = distributeFile(file)
            print("")
            if result:
                processedFiles.append(file)
    #save processedList
    if processedList:
        with open(processedListFilePath, 'w') as processedListFile:
            for file in processedFiles:
                processedListFile.write(file + "\n")
            processedListFile.close()


def tvShows():
    tvShows = []
    for x in os.listdir(tvPath):
        if os.path.isdir(tvPath + "/" + x):
            tvShows.append(x)
    return tvShows


if __name__ == '__main__':
    try:
        with open('config.json') as configFile:
            data = json.load(configFile)
            configFile.close()
            tvPath = data['tv']
            moviesPath = data['movies']
            downloadsPath = data['downloads']
            processedList = data['proclist']
    except:
        raise SystemExit("config.json file not found or invalid.")
    startDistribution()
    if debugTvSeriesNames:
        series = tvShows()
        print("")
        print("You have the following TV Series folders:")
        for s in series:
            print("   • " + s)

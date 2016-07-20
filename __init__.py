import json
import os
import re
import levlib
import glob
import fnmatch
import subprocess
import sys

# configuration
tvPath = ""
moviesPath = ""
downloadsPath = ""

#constants
bigFile = 100

# data
videoExtensions = ['mkv', 'avi', 'mp4']
subtitlesExtensions = ['srt', 'sas', 'sub']


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
    def moveTv(frm):
        fileName = os.path.basename(frm)
        show = levlib.tvMatch(fileName, tvShows())
        if show is not None:
            path = tvPath + "/" + show
            moveFile(frm, path)
        else:
            print("No TV show for it")
    # is big
    isBigFile = (os.path.getsize(file) / 1048576) >= bigFile
    # is subtitle
    isSubtitle = False
    for subtitleExtension in subtitlesExtensions:
        if fnmatch.fnmatch(file, "*." + subtitleExtension):
            isSubtitle = True
    # is series
    isSeries = False
    if re.match(".*(S|s)\d+(E|e)\d+.*", file):
        isSeries = True
    if re.match(".*\d+x\d+.*", file):
        isSeries = True
    #if isSeries:
    #    print("is series")
    #else:
    #    print("is not series")
    # distribute
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
        print("=> Movies")
        moveFile(file, moviesPath)
    elif dest == "tv":
        fileName = os.path.basename(file)
        tvSeries = levlib.tvMatch(fileName, tvShows())
        if tvSeries is not None:
            print("=> TV Series: " + tvSeries)
            moveFile(file, tvPath + "/" + tvSeries)
        else:
            print("=> No appropiate TV Series found in:")
            print(tvShows())
            print("Left where it is")
    elif dest == "small":
        print("=> Probably a sample file. Left where it is.")


def startDistribution():
    extensions = videoExtensions + subtitlesExtensions
    files = filesInDirWithExtension(downloadsPath, extensions)
    for file in files:
        print("* " + file)
        distributeFile(file)
        print("")


def tvShows():
    tvShows = []
    for x in os.listdir(tvPath):
        if os.path.isdir(tvPath + "/" + x):
            tvShows.append(x)
    return tvShows


if __name__ == '__main__':
    with open('data.json') as dataFile:
        data = json.load(dataFile)
        videoExtensions = data["video"]
        subtitlesExtensions = data["subtitles"]
    try:
        with open('config.json') as configFile:
            data = json.load(configFile)
            tvPath = data['tv']
            moviesPath = data['movies']
            downloadsPath = data['downloads']
            startDistribution()
    except:
        raise SystemExit("config.json file not found or invalid.")

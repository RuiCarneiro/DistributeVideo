#coding=utf8

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
mode = ""

# constants
big_file = 100000000  # 100MB

# data
video_extensions = ["mkv", "avi", "mp4", "m4v", "mov"]
subtitles_extensions = ["srt", "ass", "ssa", "smi", "sub", "idx", "vob"]

# re's
series_regex1 = ".*(S|s)\d+(E|e)\d+.*"
series_regex2 = ".*\d+x\d+.*"

# globals
debug_tv_series_names = False


def run_process(command, args):
    if type(command) is str:
        command = [command]
    if type(args) is str:
        args = [args]
    cmd = command + args
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out, err


def place_file(from_location, to_location):
    if mode == "move":
        cmd = 'mv'
        args = ['-u', from_location, to_location]
    elif mode == "symbolic":
        cmd = 'ln'
        args = ['-s', from_location, to_location]
    elif mode == "copy":
        cmd = 'cp'
        args = [from_location, to_location]
    else:
        raise SystemExit("Configuration file invalid (for key: mode)")
    o, e = run_process(cmd, args)
    if e is not None:
        return -1
    return o, e


def list_files(directory):
    files = []
    for file in glob.iglob(directory + "/**/*", recursive=True):
        files.append(file)
    return files


def list_files_in_dir_with_extension(directory, extensions):
    files = []
    for file in list_files(directory):
        for extension in extensions:
            if fnmatch.fnmatch(file, "*." + extension):
                files.append(file)
    return files


def distribute_file(file):
    file_name = os.path.basename(file)
    # is big
    is_a_big_file = os.path.getsize(file) >= big_file
    # is subtitle
    is_subtitle_file = False
    for subtitleExtension in subtitles_extensions:
        if fnmatch.fnmatch(file, "*." + subtitleExtension):
            is_subtitle_file = True
    # is series
    is_from_a_serial = False
    if re.match(series_regex1, file_name):
        is_from_a_serial = True
        m = re.search("(.*)([sS]\d)", file_name)
        if m:
            series_name = m.group(1)
    if re.match(series_regex2, file_name):
        is_from_a_serial = True
        m = re.search("(.*)(\d+x\d+)", file_name)
        if m:
            series_name = m.group(1)
    # select destination
    dest = ""
    if is_subtitle_file:
        if is_from_a_serial:
            dest = "tv"
        else:
            dest = "movie"
    else:
        if is_from_a_serial:
            dest = "tv"
        elif is_a_big_file:
            dest = "movie"
        else:
            dest = "small"
    # move file
    if dest == "movie":
        print("  ✔︎ Movies")
        place_file(file, moviesPath)
        return True
    elif dest == "tv":
        tvSeries = levlib.tv_match(series_name, tv_shows())
        if tvSeries is not None:
            print("  ✔︎ TV Series: " + tvSeries)
            place_file(file, tvPath + "/" + tvSeries)
            return True
        else:
            print("  ✘ No appropiate TV Series folder found. Left there.")
            global debug_tv_series_names
            debug_tv_series_names = True
            return False
    elif dest == "small":
        print("  ✘ Probably a sample file. Left there.")
        return True
    return False


def start_distribution():
    already_processed_file_path = downloadsPath + "/.dvprocessed"
    extensions = video_extensions + subtitles_extensions
    files = list_files_in_dir_with_extension(downloadsPath, extensions)
    # processedList
    processed_files = []
    if processedList:
        try:
            with open(already_processed_file_path) as processed_list_file:
                processed_files = processed_list_file.read().splitlines()
                processed_list_file.close()
        except:
            processed_list_file = open(already_processed_file_path, 'w')
            processed_list_file.close()
    # file by file
    for file in files:
        if file not in processed_files:
            print("  ➤ " + file)
            result = distribute_file(file)
            print("")
            if result:
                processed_files.append(file)
    # save processedList
    if processedList:
        with open(already_processed_file_path, 'w') as processed_list_file:
            for file in processed_files:
                processed_list_file.write(file + "\n")
            processed_list_file.close()


def tv_shows():
    tv_show_list = []
    for x in os.listdir(tvPath):
        if os.path.isdir(tvPath + "/" + x):
            tv_show_list.append(x)
    return tv_show_list


if __name__ == '__main__':
    try:
        with open('config.json') as configFile:
            data = json.load(configFile)
            configFile.close()
            tvPath = data['tv'].rstrip('/').rstrip('\\')
            moviesPath = data['movies'].rstrip('/').rstrip('\\')
            downloadsPath = data['downloads'].rstrip('/').rstrip('\\')
            processedList = data['proclist']
            mode = data['mode']
    except:
        raise SystemExit("Configuration file not found or invalid.")
    start_distribution()
    if debug_tv_series_names:
        series = tv_shows()
        print("")
        print("You have the following TV Series folders:")
        for s in series:
            print("   • " + s)

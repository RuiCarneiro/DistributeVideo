# DistributeVideo

## What it is

A quick and dirty Python script to help you organize video files. It scans one folder, and moves movie files to another appropiate folder, TV series files to another folder with sub-folders organizing the TV shows. E.g.:

files from

    /downloads

magically go to

    /movies
    /tv
      /Silicon Valley
      /Veep


Movies should go to /movies, and TV seires should go to their appropriate folder. Subtitle files go like video files. This is appropriate for a Kodi library.

## How does it know?

By looking at the file names.

## How to install

Requirements: POSIX OS, Python 3.x.

1. Clone this project to your computer

2. Edit config.json, and set:

  `"downloads"` -> source folder

  `"movies"` -> where the movies go

  `"tv"` -> where the TV series are

3. You can run the script with

  `$ python3 __init__.py`
  
  run.sh should be a template if you want to send an e-mail at the end

## What you're trying to do, isn't that illegal?

First, no.

Second, don't give me the talk, where I live, most of the TV shows that I watch aren't legally avaliable. Netflix does exist, but the catalog is very poor and late, and the price doesn't reflect that.

## Thanks

To who did write the Levenshtein distance algorith found in Wikipedia that I'm using.

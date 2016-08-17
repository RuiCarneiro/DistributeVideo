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
  
  `run.sh` is an handy script that can send you an email at the end (if you have an email MTA)
  configured in your machine. Edit `run.sh` to set the email configurations, and test the script by running:

  `$ ./run.sh`

# How to integrate with transmission-daemon for Linux

Turn off the service (e.g. `sudo service transmission-daemon stop` for debian)

Edit your config.json (.e.g `/etc/transmission-daemon/settings.json`), and set the following paramters in the JSON, adding them if necessary:

    "script-torrent-done-enabled": true, 
    "script-torrent-done-filename": "/path/to/your/program/copy/run.sh", 

This will make run.sh to run on each torrent file download complete (inclusing seeding). But also, remember that DistributeVideo will run blind to what transmission-daemon is doing, so it's a good idea to store the files being downloaded, but not completed, in a different path:

    "incomplete-dir-enabled": true

And set the `"incomplete-dir"` to a directory you would like to be used.

Please remember that the script will run as the same user as `transmission-daemon` uses, so make sure that that user can read and write in the necessary folders.

## Thanks

To who did write the Levenshtein distance algorith found in Wikipedia that I'm using.

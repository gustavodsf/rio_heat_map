#!/bin/sh
python3 -m nltk.downloader rslp
cd server
python3 run.py &

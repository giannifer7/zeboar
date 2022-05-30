#!/usr/bin/bash

cp /mnt/c/Users/produzione03/prj/zebra4/*.txt .
cp /mnt/c/Users/produzione03/prj/zebra4/*.py .
buildozer android debug
$WINADB install bin/*

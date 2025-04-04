#!/usr/bin/bash

##change this to the folder that contains goal
DIRECTORY=~/node
GOAL=${DIRECTORY}/goal

FILE=fortytwo.teal
FILE=passphrase.teal
FILE=42.teal

${GOAL} clerk compile ${FILE}





#!/usr/bin/env bash

IFS=":"
read -p "Utt Log - Project: Description: " project desc
if [[ -z "$project" && -z "$desc" ]]; then
    echo "No input received!... Exiting..."
    exit 1
fi

if [ ${#desc} -gt 0 ]; then 
    sh -c "utt add \"$project: $desc\""
else
    sh -c "utt add \"$project\""
fi
echo "Log added ..."
read -t 3 -p "Do you want to see/edit the log file? " ledit
ledit=${ledit,,}
if [[ $ledit =~ ^(yes|y)$ ]];
then
    sh -c "utt edit"
fi


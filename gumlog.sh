#!/usr/bin/env bash
if  ! command -v gum &> /dev/null
then 
    echo "You need to install 'charmbracelet/gum' to run this ... Exiting"
    exit 1
fi
clear
gum style --foreground 80 --border double --border-foreground 80 --padding "1 2" --margin 1 --align center "Utt Log Form" "Use arrows or j-k to move up down"

while :
do
    CHOICE=$(gum choose "Add Log Entry" "Edit File" "See Report" "See Log File" "Quit")
    case $CHOICE in 
        "Add Log Entry")
            PROJECT=$(gum input --prompt "Project: " --placeholder "Which Project you were wroking on? ")
            test -n "$PROJECT" && SCOPE="$PROJECT: "
            DESC=$(gum input --prompt "\"$SCOPE\"Description: " --placeholder "Explain what you did in about 10-15 words...")
            test -n "$DESC" && SCOPE="$SCOPE$DESC"
            test -n "$SCOPE" && sh -c "utt add \"$SCOPE\"" && gum spin -s minidot --title "Log written ..." -- sleep 1 || gum spin -s monkey --title "No input provided ..." -- sleep 2
            ;;

        "Edit File")
            sh -c "utt edit"
            ;;

        "See Report")
            sh -c "utt report"
            ;;

        "See Log File")
            gum pager < $UTT_LOG_FILE
            ;;
        *)
            echo -n "Quitting ..." ; sleep 1
            break
            ;;
    esac
done
clear

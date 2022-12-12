#!/usr/bin/env bash
if  ! command -v gum &> /dev/null
then 
    echo "You need to install 'charmbracelet/gum' to run this ... Exiting"
    exit 1
fi
clear

while :
do
gum style --foreground 80 --border double --border-foreground 80 --padding "1 2" --margin 1 --align center "Utt Log Form" "Use arrows or j-k to move up down"
    CHOICE=$(gum choose "Add Log Entry" "Edit File" "See Report" "See Log File" "Quit")
    case $CHOICE in 
        "Add Log Entry")
            PROJECT=$(gum input --prompt "Project: " --placeholder "Which Project you were wroking on? ")
            DESC=$(gum input --prompt "${PROJECT}: Description: " --placeholder "Explain what you did in about 10-15 words...")
            test -n "$PROJECT" && SCOPE="$PROJECT: "
            test -n "$DESC" && SCOPE="$SCOPE$DESC"
            test -n "$SCOPE" && sh -c "utt add \"$SCOPE\"" && gum spin -s minidot --title "Log written ..." -- sleep 1 && clear || gum spin -s monkey --title "No input provided ..." -- sleep 2 && clear
            ;;

        "Edit File")
            sh -c "utt edit"
            clear
            ;;

        "See Report")
            sh -c "utt report"
            gum confirm "Continue?" 
            clear
            ;;

        "See Log File")
            gum pager < "$UTT_LOG_FILE"
            clear
            ;;
        *)
            echo -n "Quitting ..." ; sleep 1
            break
            ;;
    esac
done
clear

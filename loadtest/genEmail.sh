#/bin/bash

function genLetter()
{
    randLetterNum="$(( (${RANDOM} % 26) + 97))"
    letterNum="${1:-${randLetterNum}}"
    printf \\$(printf '%03o' "${letterNum}")
}

function genWord()
{    
    local word=""

    for i in $(seq 1 1 ${length})
    do
        word+="$($@)"
    done

    printf "%s" "${word}"
}

function genEmail()
{    
    local length=${1:-3}
    local email="";

    if [ -n "$1" ]
    then
        case $1 in
            ''|*[0-9]*) shift 1 ;;
            *) ;;
        esac
    fi

    email+="$(genWord $@)"
    email+="@"
    email+="$(genWord $@)"
    email+=".com"
    
    printf "%s\n" "${email}"
}

function genRandomEmail()
{
    local length=${1:-3}
    genEmail ${length} genLetter
}

function genEmails()
{
    local length=${1:-3}
    local email=""

    local range=$(echo {97..122})

    for i in $(seq 1 1 ${range})
    do
        echo
    done
}



genRandomEmail
genEmails

#genEmail 3 genLetter



# EOF

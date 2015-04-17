# !/usr/bin/env bash

# extract date from invoice pdf
get_date() {
    pdftotext -layout "$1" - | grep "Invoice Date" | awk {'print $NF'}
}

# extract relevant cost table from invoice pdf
get_pdf_text() {
    pdftotext -layout "$1" - | cat | grep -A 50000000 "Monthly Service Fees" | grep -v "https" | grep -v "Customer:" | grep -v "If you have" | grep -v "Monthly Service Fees" | grep -v "Details"
}

# get json cost totals from cost table text
get_totals() {
    get_pdf_text "$1" | python costs.py
}

# run the whole thing on all pdfs in the directory
do_it () {
    fn="*.pdf"
    for f in $fn 
    do
        echo "`get_date "$f"` - `get_totals "$f"` - $f"
    done
}

do_it

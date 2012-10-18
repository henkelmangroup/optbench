#!/bin/bash
for filename in `ls`
do
    if [ -d $filename ]; then
        if [ -e ${filename}/report.sh -a -e ${filename}/getdata.py ]; then
            cd $filename
            echo $filename
            ./report.sh
            cd ..
        fi
    fi
done

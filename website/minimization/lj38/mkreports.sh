#!/bin/bash
for filename in `ls`
do
    if [ -d $filename ]; then
        if [ -e ${filename}/report.sh ]; then
            cd $filename
            echo $filename
            ./report.sh
            cd ..
        fi
    fi
done

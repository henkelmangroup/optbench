#!/bin/bash
tar -xzf coords.tgz

python dec_lj38.py
python getdata.py

rm -r coords/

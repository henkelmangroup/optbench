#!/bin/bash
tar -xzf pt-island-con.tgz
python dec_morse.py
python getdata.py
rm -r pt-island-con

#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Sun Dec 10 11:13:55 EST 2023
set -ve
server=td
remote_dir=/tigress/wenchang/analysis/numerical_experiments_list
#get files of *.html, *.py and *.sh from remote server
rsync -avhP ${server}:$remote_dir/*.html .
rsync -avhP ${server}:$remote_dir/*.py .
rsync -avhP ${server}:$remote_dir/*.sh .

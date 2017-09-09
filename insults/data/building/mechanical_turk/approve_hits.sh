#!/usr/bin/env bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

HITS_IDS=$script_dir/hit_ids/ids.txt

cd $script_dir/simple-amt

python approve_hits.py --hit_ids_file=$HITS_IDS

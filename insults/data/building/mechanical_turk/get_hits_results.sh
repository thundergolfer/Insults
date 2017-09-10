#!/usr/bin/env bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

HITS_IDS=$script_dir/hit_submitted/ids.txt
OUTPUT_FILE=$script_dir/hit_results/results.txt

cd $script_dir/simple-amt

python get_results.py \
  --hit_ids_file=$HITS_IDS \
  --output_file=$OUTPUT_FILE \
  > $OUTPUT_FILE

./$script_dir/script/update_dataset_from_simpleamt_results.py $OUTPUT_FILE

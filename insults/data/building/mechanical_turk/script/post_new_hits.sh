#!/usr/bin/env bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python $script_dir/sync_with_simpleamt.py

cd $script_dir/../simple-amt

INPUTS_FILE="$1"
TEMPLATE_NAME=hit_templates/task_template.html
PROPERTIES_FILE=hit_properties/insults_classify_task_props.json
IDS_OUTPUT_FILE=$script_dir/../hit_submitted/ids_$(date +%s).txt
DATASET_NAME=new_dataset.csv

python launch_hits.py \
  --html_template=$TEMPLATE_NAME \
  --hit_properties_file=$PROPERTIES_FILE \
  --input_json_file=$INPUTS_FILE \
  --hit_ids_file=$IDS_OUTPUT_FILE


cd $script_dir

./update_db_for_submitted_hits.py $DATASET_NAME $INPUTS_FILE $IDS_OUTPUT_FILE

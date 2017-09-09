#!/usr/bin/env bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $script_dir/simple-amt

TEMPLATE_NAME=hit_templates/task_template.html
PROPERTIES_FILE=hit_properties/insults_classify_task_props.json
INPUTS_FILE=hit_inputs/inputs.txt
IDS_OUTPUT_FILE=$script_dir/hit_submitted/ids.txt

python launch_hits.py \
  --html_template=$TEMPLATE_NAME \
  --hit_properties_file=$PROPERTIES_FILE \
  --input_json_file=$INPUTS_FILE \
  --hit_ids_file=$IDS_OUTPUT_FILE


INPUTS_FILE_NAME="$1"
LIMIT=100

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $script_dir/../../../../
pwd

echo "Step 1: Gathering HITs inputs from dataset..."
python -m insults.data.building.mechanical_turk.script.dataset_to_simpleamt_inputs $INPUTS_FILE_NAME $LIMIT

cd $script_dir/script/

echo "Step 2: Posting HITS to Mech. Turk..."
./post_new_hits.sh $script_dir/hit_inputs/$INPUTS_FILE_NAME

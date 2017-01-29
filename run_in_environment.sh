#!/bin/bash

# Runs any command in the application's python virtual environment. This script assumes
# the environment has been installed using install_miniconda.sh and
# install_app.sh.
#
# Usage:
# ./run_in_environment.sh python setup.py test
#
# You can also use it to activate the virtual environment, e.g.:
# source run_in_environment.sh


script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${script_dir}/miniconda_info.sh"
ACTIVATE_FILE="${VIRTUAL_ENV_PATH}/bin/activate"

if [ -f $ACTIVATE_FILE ]; then
    source $ACTIVATE_FILE $VIRTUAL_ENV_PATH
    exec "$@"
else
    echo "Error: the file $ACTIVATE_FILE does not exist. Please install the environment correctly."
    # Only exit if you're not in an interactive session
    if [[ $- != *"i"* ]] ; then exit 1 ; fi
fi

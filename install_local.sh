#!/bin/bash -e
# Create or replace the app's python virtual environment and installs all the packages required for the app.
#
# Usage:
# ./install_local.sh
#
# The requirements file listing the conda and PIP dependencies can be overriden:
# * REQUIREMENTS_PIP_FILE - List of dependencies/libs to be installed with pip
# * REQUIREMENTS_CONDA_FILE - List of dependencies/libs to be installed with conda
#

source miniconda_info.sh

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

conda_env_specification="${REQUIREMENTS_CONDA_FILE:-conda_env_specification.txt}"
requirements_pip_file="${REQUIREMENTS_PIP_FILE:-requirements.txt}"

conda_command="${MINICONDA_DIRECTORY}/bin/conda"
$conda_command info -a

# Create or replace python virtual environment
rm -rf $VIRTUAL_ENV_PATH
$conda_command create -y python -p $VIRTUAL_ENV_PATH --file "${conda_env_specification}"

# Required to fix an installation error
$conda_command update pyside

# Install the app and its dependencies
source run_in_environment.sh

# Register the packages installed by conda in pip
# Avoids unwarranted package upgrades
packages_for_pip_to_ignore=$(grep -E "^numpy|scipy|scikit|numexpr" ${conda_env_specification} | tr '\n' ' ')
pip install --upgrade $packages_for_pip_to_ignore

# Install remaining dependencies and tensorflow
echo "Installing pip requirement file: ${requirements_pip_file}"
pip install -r "${requirements_pip_file}"

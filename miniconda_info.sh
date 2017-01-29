#!/bin/bash -e
# This script ensures that the environment variables used for the Python virtual env and Miniconda exist.
# To override the default environment variables, you can define them before running this script.
#
# Include these details into your environment with:
#
# source miniconda_info.sh
#
# These are the variables exported and their defaults:
#
# * VIRTUAL_ENV_PATH - Where the virtual env will be (default: '<APP_ROOT>/virtual_env')
# * MINICONDA_VERSION - Which version of miniconda will be installed (default: '3.9.1')
# * MINICONDA_DIRECTORY - Where miniconda will be installed (default: '/opt/miniconda-3.9.1/')


script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export VIRTUAL_ENV_PATH="${VIRTUAL_ENV_PATH:=${script_dir}/virtual_env}"
export MINICONDA_VERSION="${MINICONDA_VERSION:-3.9.1}"


if [ `uname` = "Darwin" ]; then
  export MINICONDA_DIRECTORY="${MINICONDA_DIRECTORY:=/Users/${USER}/miniconda-${MINICONDA_VERSION}}"
else
  export MINICONDA_DIRECTORY="${MINICONDA_DIRECTORY:=/opt/miniconda-${MINICONDA_VERSION}}"
fi

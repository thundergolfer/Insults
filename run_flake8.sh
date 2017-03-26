#!/usr/bin/env bash

# Travis command line parsing doesn't like pipes, so this shell script
# executes the piped command with zero issues
git diff master -- insults tests | ./virtual_env/bin/flake8 --diff

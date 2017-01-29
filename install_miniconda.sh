#!/bin/bash -e

source miniconda_info.sh

#Helper function
install_linux() {
    if  [ ! -f "Miniconda-${MINICONDA_VERSION}-Linux-x86_64.sh" ]; then
        curl -s https://repo.continuum.io/miniconda/Miniconda-${MINICONDA_VERSION}-Linux-x86_64.sh > Miniconda-${MINICONDA_VERSION}-Linux-x86_64.sh
    fi
    bash Miniconda-${MINICONDA_VERSION}-Linux-x86_64.sh -b -f -p ${MINICONDA_DIRECTORY}
}

install_osx() {
    if  [ ! -f "Miniconda-${MINICONDA_VERSION}-MacOSX-x86_64.sh" ]; then
        curl -s https://repo.continuum.io/miniconda/Miniconda-${MINICONDA_VERSION}-MacOSX-x86_64.sh > Miniconda-${MINICONDA_VERSION}-MacOSX-x86_64.sh
    fi
    bash Miniconda-${MINICONDA_VERSION}-MacOSX-x86_64.sh -b -f -p ${MINICONDA_DIRECTORY}
}

echo "Installing Miniconda version: ${MINICONDA_VERSION} at path: ${MINICONDA_DIRECTORY}"

# Ensure the directory exists
if [ -w `dirname "${MINICONDA_DIRECTORY}"` ] ; then
    mkdir -p "${MINICONDA_DIRECTORY}" 2>/dev/null
else
    echo "You will need sudo access to create the miniconda directory: ${MINICONDA_DIRECTORY}"
    sudo mkdir -p "${MINICONDA_DIRECTORY}" 2>/dev/null
    sudo chown "${USER}" "${MINICONDA_DIRECTORY}"
fi

# Start installing
if [ ! -f "${MINICONDA_DIRECTORY}/installed_${MINICONDA_VERSION}" ]; then
    if [ `uname` = "Darwin" ]; then
        install_osx
    else
        install_linux
    fi
    echo "Install complete" > "${MINICONDA_DIRECTORY}/installed_${MINICONDA_VERSION}"
else
    echo "Miniconda has already been successfully installed"
fi

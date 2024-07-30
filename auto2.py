file = open('gsidown2.sh', "w")
file.write("""#!/bin/bash
set -e 

BP=$PWD/crdroid/patches
BY=$PWD/crdroid/

git() {
       echo "---> git cloning..."
       git clone https://Huina1aosp/GSI_BUILD
}


pkg() {
        echo "--> downloading pkg..."
        sudo apt-get install ccache git-core gnupg flex bison build-essential zip curl zlib1g-dev libc6-dev-i386 x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig
        echo
}


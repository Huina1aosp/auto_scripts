# script by super
file = open('gsidown.sh', "w")
file.write("""#!/bin/bash

echo
echo "--------------------------------------"
echo "        crdroid 14.0 Buildbot         "
echo "                  by                  "
echo "                supers                "
echo "--------------------------------------"
echo

set -e

git clone https://github.com/Huina1aosp/crDroid_gsi
cd crDroid_gsi

pkg() {
        echo "--> downloading pkg..."
        sudo apt-get install ccache git-core gnupg flex bison build-essential zip curl zlib1g-dev libc6-dev-i386 x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig
        echo
}


initRepos() {
    if [ ! -d .repo ]; then
        echo "--> Initializing workspace"
        repo init -u https://android.googlesource.com/platform/manifest -b android-14.0.0_r54 --git-lfs
        echo
        
        echo "--> Preparing local manifest..."
        echo
	 mkdir -p .repo/local_manifests
    cp $BL/patches/default.xml .repo/local_manifests/default.xml
    cp $BL/patches/remove.xml .repo/local_manifests/remove.xml
        echo
     fi
}

syncRepos() {
    echo "--> Syncing repos"
    repo sync
    echo
}

applyPatches() {
    echo "--> Applying patches"
       bash patches/apply-patches.sh .
    echo
}

genrommk() {
    echo "--> generate rom make file"
	cd device/phh/treble
	bash generate.sh crDroid
    echo
}

compile() {
	echo "--> compilation..."
	. build/envsetup.sh
	ccache -M 1G 
	lunch treble_arm64_bgN-userdebug 
	make systemimage -j$(nproc --all)
	echo
}



START=$(date +%s)

pkg
initRepos
syncRepos
applyPatches
genrommk
compile

END=$(date +%s)
ELAPSEDM=$(($(($END-$START))/60))
ELAPSEDS=$(($(($END-$START))-$ELAPSEDM*60))

echo "--> Buildbot completed in $ELAPSEDM minutes and $ELAPSEDS seconds"
echo
import os
impert system
os.system(bash gsidown.sh)
os.system""")
print('now excute gsidown.sh')

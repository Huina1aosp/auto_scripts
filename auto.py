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

initRepos() {
    if [ ! -d .repo ]; then
        echo "--> Initializing workspace"
        repo init -u https://github.com/crdroidandroid/android.git -b 14.0
        echo
        
        echo "--> Preparing local manifest..."
	 git clone https://github.com/naz664/treble_manifest.git .repo/local_manifests  -b 14
        echo
    fi
}

syncRepos() {
    echo "--> Syncing repos"
    repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags --optimized-fetch --prune
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

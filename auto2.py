file = open('gsidown2.sh', "w")
file.write("""#!/bin/bash

echo "build bot by supers"

set -e 

BP=$PWD/patches
BY=$PWD/

git clone https://github.com/Huina1aosp/GSI_BUILD
cd GSI_BUILD


pkg() {
        echo "--> downloading pkg..."
        sudo apt-get install ccache repo git-core gnupg flex bison build-essential zip curl zlib1g-dev libc6-dev-i386 x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig
        echo
}

initRepo() {
            echo "---> init repo..."
               repo init -u https://github.com/crdroidandroid/android.git -b 14.0 -c --depth=1 --no-tags --no-clone-bundle --no-outer-manifest  --no-use-superproject  --this-manifest-only
            echo
}

XML() {
      echo "--> Preparing XML..."
      cp $BP/gapps.xml .repo/local_manifests
      cp $BP/manifest.xml .repo/local_manifests

      echo
}

sync() {
       echo "--> Syncing...."
       repo sync -j4 -c -q --no-clone-bundle --no-tags --no-use-superproject --optimized-fetch --retry-fetches=15  --prune --no-auto-gc --force-remove-dirty 
       echo
}

applyPatches() {
    echo "--> Applying patches"
       bash patches/apply-patches.sh .
    echo
}

generation() {
             echo "generation mk..."
             cd device/phh/treble
             bash generate.sh crDroid
             echo
}

compile() {
       echo "compile..."
       . build/envsetup.sh
       ccache -M 1G -F 0
       lunch treble_arm64_bgN-userdebug 
       make systemimage
       echo
}

START=$(date +%s)

pkg
initRepo
sync
applyPatches
generation
compile

END=$(date +%s)
ELAPSEDM=$(($(($END-$START))/60))
ELAPSEDS=$(($(($END-$START))-$ELAPSEDM*60))

echo "--> Buildbot completed in $ELAPSEDM minutes and $ELAPSEDS seconds"
echo""")
print('please set youre git config')
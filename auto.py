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
BL=$PWD/patches

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
echo "--> Generating makefiles"
    cd device/phh/treble
    cp $BL/patches/aosp.mk .
    bash generate.sh aosp
    cd ../../..
    echo
}

setupEnv() {
    echo "--> Setting up build environment"
    source build/envsetup.sh &>/dev/null
    ccache-M 1G
    mkdir -p $BD
    echo
}

buildTrebleApp() {
    echo "--> Building treble_app"
    cd treble_app
    bash build.sh release
    cp TrebleApp.apk ../vendor/hardware_overlay/TrebleApp/app.apk
    cd ..
    echo
}

buildVariant() {
    echo "--> Building $1"
    lunch "$1"-ap2a-userdebug
    make -j$(nproc --all) installclean
    make -j$(nproc --all) systemimage
    make -j$(nproc --all) target-files-package otatools
    bash $BL/sign.sh "vendor/ponces-priv/keys" $OUT/signed-target_files.zip
    unzip -jo $OUT/signed-target_files.zip IMAGES/system.img -d $OUT
    mv $OUT/system.img $BD/system-"$1".img
    echo
}

buildVndkliteVariant() {
    echo "--> Building $1-vndklite"
    [[ "$1" == *"a64"* ]] && arch="32" || arch="64"
    cd treble_adapter
    sudo bash lite-adapter.sh "$arch" $BD/system-"$1".img
    mv s.img $BD/system-"$1"-vndklite.img
    sudo rm -rf d tmp
    cd ..
    echo
}

buildVariants() {
    buildVariant treble_a64_bvN
    buildVariant treble_a64_bgN
    buildVariant treble_arm64_bvN
    buildVariant treble_arm64_bgN
    buildVndkliteVariant treble_a64_bvN
    buildVndkliteVariant treble_a64_bgN
    buildVndkliteVariant treble_arm64_bvN
    buildVndkliteVariant treble_arm64_bgN
}

generatePackages() {
    echo "--> Generating packages"
    buildDate="$(date +%Y%m%d)"
    find $BD/ -name "system-treble_*.img" | while read file; do
        filename="$(basename $file)"
        [[ "$filename" == *"_a64"* ]] && arch="arm32_binder64" || arch="arm64"
        [[ "$filename" == *"_bvN"* ]] && variant="vanilla" || variant="gapps"
        [[ "$filename" == *"-vndklite"* ]] && vndk="-vndklite" || vndk=""
        name="aosp-${arch}-ab-${variant}${vndk}-14.0-$buildDate"
        xz -cv "$file" -T0 > $BD/"$name".img.xz
    done
    rm -rf $BD/system-*.img
    echo
}

START=$(date +%s)

initRepos
syncRepos
applyPatches
genrommk
setupEnv
buildTrebleApp
[ ! -z "$BV" ] && buildVariant "$BV" || buildVariants
generatePackages

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

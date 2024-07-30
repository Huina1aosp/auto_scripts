file = open('gsidown2.sh', "w")
file.write("""#!/bin/bash
set -e 

BP=$PWD/crdroid/patches
BY=$PWD/crdroid/

initrepo()
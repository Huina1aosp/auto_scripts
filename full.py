#scripts by huina
import os
yesn = input("Do you want to continue? (yes/no): ")
if yesn.lower() in ["yes", "y"]:
    print("Continuing...")
            echo "--> download requirement files..."
            os.system ("git clone https://github.com/Huina1aosp/GSI_BUILD")
            os.system ("cd GSI_BUILD")
            is.system ("bash build.sh")
else:
    print("Exiting...")
            

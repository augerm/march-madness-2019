import os
from sys import platform

if platform == "linux" or platform == "linux2":
    os.system('export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"')
    os.system('echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list')
    os.system('sudo apt-get update && sudo apt-get install google-cloud-sdk')
    os.system('gcloud init')
elif platform == "darwin":
    os.system('curl https://sdk.cloud.google.com | bash')
    os.system('exec -l $SHELL')
    os.system('gcloud init')
elif platform == "win32":
    print("Please install manually... We haven't added your OS to the script yet.")
import os

print("@@@ Running startup script...")

print("@@@ Navigating to project folder")
os.system('cd /home/michaelauger23/march-madness-2019')

print("@@@ Printing working directory")
os.system('pwd')

print("@@@ Downloading data files")
# os.system('gsutil cp -r gs://march-madness-2019 /home/michaelauger23/march-madness-2019')

print("@@@ Fetching origin...")
os.system('git pull origin master')

print("@@@ Running train.py...")
os.system('python3 ./train.py')

# Turn off machine when finished in order to limit costs.
print("@@@ Shutting down machine...")
os.system('sudo poweroff')

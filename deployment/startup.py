import os

print("@@@ Running startup script...")

print("@@@ Navigating to project folder")
os.system('cd /home/michaelauger23/march-madness-2019')

print("@@@ Fetching origin...")
os.system('git pull origin master')

print("@@@ Running main.py...")
os.system('python3 ./modules/train.py')

# Turn off machine when finished in order to limit costs.
print("@@@ Shutting down machine...")
# os.system('sudo poweroff')

import os

print("@@@ Running startup script...")
print("@@@ Fetching origin...")
print('git pull origin master...')

print("@@@ Running main.py...")
os.system('python3 ../main.py')

# Turn off machine when finished in order to limit costs.
print("@@@ Shutting down machine...")
os.system('sudo poweroff')

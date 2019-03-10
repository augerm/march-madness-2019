import os

os.system('git pull origin master')
os.system('python3 ../main.py')

# Turn off machine when finished in order to limit costs.
os.system('sudo poweroff')

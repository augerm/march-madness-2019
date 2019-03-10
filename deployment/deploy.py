import os
import requests

r = requests.post("https://www.googleapis.com/compute/v1/projects/march-madness-2019/zones/us-east1-b/instances/machine-learning-tf-keras-1/start")
print(r)
# os.system('git status')
# os.system('git add -A')
# commit_message = input('Enter a commit message: ')
# os.system('git commit -m "{}"'.format(commit_message))
# os.system('git push origin master')

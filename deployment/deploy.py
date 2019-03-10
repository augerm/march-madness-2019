import os
os.system('git status')
os.system('git add -A')
commit_message = input('Enter a commit message: ')
os.system('git commit -m "{}"'.format(commit_message))
os.system('git push origin master')

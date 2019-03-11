import os
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

os.system('git status')
os.system('git add -A')
commit_message = input('Enter a commit message: ')
os.system('git commit -m "{}"'.format(commit_message))
os.system('git pull origin master')
os.system('git push origin master')

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

# Project ID for this request.
project = 'march-madness-2019'

# The name of the zone for this request.
zone = 'us-east1-b'

# Name of the instance resource to start.
instance = 'machine-learning-tf-keras-2'

request = service.instances().start(project=project, zone=zone, instance=instance)
response = request.execute()
print(response)


import os
from deployment.example_settings import *

os.system('gsutil -m rsync -r {} {}'.format(local_data_directory, remote_data_directory))
os.system('gsutil -m rsync -r {} {}'.format(remote_data_directory, local_data_directory))
os.system('gsutil -m rsync -r {} {}'.format(local_model_directory, remote_model_directory))
os.system('gsutil -m rsync -r {} {}'.format(remote_model_directory, local_model_directory))
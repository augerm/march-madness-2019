FROM tensorflow/tensorflow:latest-py3

COPY . .

# CMD ["/bin/bash", "-c" , "$(curl -fsSL https://raw.githubusercontent.com/apple/tensorflow_macos/master/scripts/download_and_install.sh)"]
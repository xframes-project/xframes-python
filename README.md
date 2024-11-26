# xframes-python

## Building

(create and activate a virtualenv)

pipx run build
pip install .

## Building on Docker (Ubuntu 24.10)

cd docker/x64-linux
docker build -t xframes-python-x64-linux .

docker run -v /path/to/xframes-python/dir:/usr/src/app/workspace -v /path/to/build/dir:/usr/src/app/build xframes-python-x64-linux

## Screenshots

![image](https://github.com/user-attachments/assets/2954191c-4dd9-444d-97e6-fa89ea4a8284)

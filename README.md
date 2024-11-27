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

Ubuntu (native x64)

![image](https://github.com/user-attachments/assets/2954191c-4dd9-444d-97e6-fa89ea4a8284)

Ubuntu (WSL2)

![image](https://github.com/user-attachments/assets/b540f7f6-1a29-4650-9de3-d1ff3c3af9a7)

Ubuntu (Raspberry Pi 5, arm64)

![image](https://github.com/user-attachments/assets/04dc7bad-2701-4280-a836-88eb4d1b5991)


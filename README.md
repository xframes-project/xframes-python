# xframes-python

pipx run build --outdir build

cd docker/x64-linux
docker build -t xframes-python-x64-linux .

docker run -v /path/to/xframes-python/dir:/usr/src/app/workspace -v /path/to/build/dir:/usr/src/app/build xframes-python-x64-linux
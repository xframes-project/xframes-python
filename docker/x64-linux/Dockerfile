FROM ubuntu:24.10

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required tools
RUN apt-get update

RUN apt-get install -y python3
RUN apt-get install -y git
RUN apt-get install -y pkg-config
RUN apt-get install -y python3-dev
RUN apt-get install -y pipx
RUN apt-get install -y zip
RUN apt-get install -y unzip
RUN apt-get install -y tar
RUN apt-get install -y build-essential
RUN apt-get install -y cmake
RUN apt-get install -y curl
RUN apt-get install -y libxinerama-dev
RUN apt-get install -y libxcursor-dev
RUN apt-get install -y xorg-dev
RUN apt-get install -y libglu1-mesa-dev

RUN apt-get clean

WORKDIR /usr/src/app

COPY runner.sh runner.sh

# Entry point
CMD ["bash", "./runner.sh"]

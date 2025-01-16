# Ubuntu image
FROM ubuntu:22.04

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# pip install numpy scipy pandas matplotlib seaborn jupyter
RUN pip3 install numpy scipy pandas matplotlib seaborn jupyter

# copy the current directory contents into the container at /chaomi
COPY . /chaomi

# Set the working directory to /chaomi
WORKDIR /chaomi

# Run bash
CMD ["/bin/bash"]
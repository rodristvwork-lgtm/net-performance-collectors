# Image
FROM python:slim

# Set container name
LABEL Name="net-performance-container"

# Install required Linux packages
RUN apt-get update
RUN apt-get install -y iproute2
RUN	apt-get install -y net-tools
RUN	apt-get install -y iputils-ping
RUN	apt-get install -y iperf3
RUN	apt-get install -y wget
RUN	apt-get install -y bash
RUN	apt-get install -y procps
RUN	apt-get install -y dos2unix


# Set working directory inside container
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || true

# Default command: start bash shell
CMD ["/bin/bash"]

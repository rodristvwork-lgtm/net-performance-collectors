
# Image
FROM python:slim

# Set container name
LABEL Name="net-performance-container-2"

# Install required Linux packages
RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    iputils-ping \
    iperf3 \
    wget \
    bash \
    dos2unix \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements if any (currently empty, but future-proof)
COPY requirements.txt .

# Install Python dependencies (safe even if requirements.txt is empty)
RUN pip install --no-cache-dir -r requirements.txt || true

# Default command: start bash shell
CMD ["/bin/bash"]

# Image
FROM python:3.11-slim-bookworm

# Set container name
LABEL Name="net-performance-collectors-container"

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
RUN apt-get install -y firefox-esr
RUN apt-get install -y xvfb 
RUN apt-get install -y x11vnc 
RUN apt-get install -y fluxbox

# Clean apt cache (optional but recommended) 
RUN apt-get clean

# Set working directory inside container
WORKDIR /app

# Expose ports
EXPOSE 5000
EXPOSE 5678
EXPOSE 5900

# Start Xvfb + Fluxbox + VNC server, then open bash 
CMD bash -c "rm -f /tmp/.X0-lock /tmp/.X11-unix/X0; Xvfb :0 -screen 0 1920x1080x24 & fluxbox & x11vnc -display :0 -nopw -forever -quiet & bash"

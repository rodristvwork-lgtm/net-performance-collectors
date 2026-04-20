#!/usr/bin/env bash
set -euo pipefail

echo "Detecting system architecture..."
ARCH=$(dpkg --print-architecture)
echo "Architecture detected: $ARCH"

# Check if already installed
if command -v speedtest >/dev/null 2>&1; then
    echo "Speedtest is already installed at: $(command -v speedtest)"
    echo "Version:"
    speedtest --version || true
    echo "Skipping installation."
    exit 0
fi

# Select correct URL
case "$ARCH" in
    amd64)
        SPEED_URL="https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz"
        ;;
    arm64)
        SPEED_URL="https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-aarch64.tgz"
        ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

echo "Downloading: $SPEED_URL"
wget --no-check-certificate "$SPEED_URL" -O speedtest.tgz

echo "Extracting archive..."
tar -xvf speedtest.tgz

# Some archives extract into a folder named "speedtest"
# Some extract a binary directly — handle both cases
if [ -f "speedtest" ]; then
    BIN_PATH="speedtest"
elif [ -f "speedtest/speedtest" ]; then
    BIN_PATH="speedtest/speedtest"
else
    echo "Error: speedtest binary not found after extraction."
    exit 1
fi

echo "Installing binary to /usr/bin..."
sudo mv "$BIN_PATH" /usr/bin/speedtest
sudo chmod +x /usr/bin/speedtest

echo "Cleaning up..."
rm -rf speedtest speedtest.tgz

echo "Installation complete."
echo "Run: speedtest"
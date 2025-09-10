#!/bin/bash

# Build the Docker image
echo "🔨 Building image..."
docker build -t gaussian_processes:latest docker/

# Enable X11 forwarding
echo "🚀 Starting container..."
xhost +local:root

# Run container in DETACHED mode (-d) 
container_id=$(docker run -d -t \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -e DISPLAY=unix$DISPLAY \
    --device /dev/dri \
    --privileged \
    -v /home/$USER/.Xauthority:/root/.Xauthority \
    --gpus all \
    -v $PWD/:/workspace \
    gaussian_processes:latest)

echo "Container ID: $container_id"

# Wait a moment for container to start
sleep 2

# Quick GPU test
echo "🎯 Testing GPU and setup..."
docker exec $container_id python -c "
import torch
print(f'✅ PyTorch {torch.__version__} | CUDA {torch.version.cuda}')
if torch.cuda.is_available():
    print(f'🔥 GPU Ready: {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory/1024**3:.1f}GB)')
else:
    print('❌ GPU NOT DETECTED!')
print('🖼️  X11 forwarding enabled - matplotlib windows should work')
print('='*50)
"

# Enter container
echo "🖥️  Entering container..."
docker exec -it $container_id bash

# Cleanup when exiting
echo "🧹 Cleaning up X11 permissions..."
xhost -local:root
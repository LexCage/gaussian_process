# Dockerfile ottimizzato per RTX 3080
# Usa un'immagine base NVIDIA con CUDA 12.x (compatibile con RTX 3080)
FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

# Aggiorna il sistema e installa dipendenze
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    build-essential \
    software-properties-common \
    ca-certificates \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Aggiorna pip
RUN pip install --upgrade pip setuptools wheel

# Installa librerie ML aggiuntive
RUN pip install \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scikit-learn \
    gpytorch 

    
# Crea directory di lavoro
WORKDIR /workspace

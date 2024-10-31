# Base image
FROM mambaorg/micromamba:latest

# Set environment variables
ENV MAMBA_ROOT_PREFIX=/opt/conda
ENV PATH=$MAMBA_ROOT_PREFIX/bin:$PATH

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install base dependencies via micromamba with exact version specifications
RUN micromamba install -y -n base -c conda-forge \
    python=3.8 \  
    numpy=1.22.4 \
    pyqt \
    sqlite \
    six \
    svgwrite \
    occt=7.8.1=novtk* \  
    pythonocc-core=7.8.1=novtk* \
    && micromamba clean --all --yes

# Install build tools
RUN micromamba install -y -n base -c conda-forge mamba boa conda-build

# Build the Conda package from the recipe
RUN micromamba run -n base conda mambabuild conda-recipe

# Test the installation
RUN micromamba run -n base python -c "import prism_viewer"

# Set default command
CMD ["micromamba", "run", "-n", "base", "python", "-m", "prism_viewer.main"]

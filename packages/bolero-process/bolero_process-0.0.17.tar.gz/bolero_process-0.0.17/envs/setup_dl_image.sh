# use sky launch to create a VM with base image
# then run this script to setup the VM

# install miniforge
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O $HOME/Miniforge3-Linux-x86_64.sh
bash $HOME/Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3
echo 'export PATH=$HOME/miniforge3/bin:$PATH' >> $HOME/.bashrc
source $HOME/.bashrc
rm -f $HOME/Miniforge3-Linux-x86_64.sh
mamba init bash

exec bash
which python

conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels pytorch
conda config --add channels conda-forge

# optional tools
sudo apt update
sudo apt install -y npm
sudo npm install -g vtop

# install sky
pip install --upgrade pip

# torch
mamba install -y pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# other tools
mamba install -y dask jupyterlab mallet pytables scikit-learn seaborn xarray zarr pyarrow htslib samtools pysam pyBigWig pynndescent pyranges snakemake
pip install black cooler gcsfs isort jupyterlab-code-formatter jupyterlab_execute_time leidenalg opentsne papermill scanpy

# clean
mamba clean -a -y
pip cache purge

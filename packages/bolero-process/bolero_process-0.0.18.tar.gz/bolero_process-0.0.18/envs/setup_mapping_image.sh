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
mamba install -y bowtie2 bedtools fastp genrich hisat2 kallisto==0.46 macs2 multiqc picard subread STAR htslib samtools pysam pyBigWig pynndescent deeptools pyranges snakemake
pip install black cooler gcsfs isort jupyterlab-code-formatter jupyterlab_execute_time leidenalg opentsne papermill scanpy

mamba clean -a -y
pip cache purge

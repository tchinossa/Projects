#!/bin/bash
#SBATCH --account=3121555
#SBATCH --partition=dsba
#SBATCH --gres=gpu:1
#SBATCH --job-name="summerizer"
#SBATCH --mem=64GB
#SBATCH --time=0-4:10:00
#SBATCH --output=out/%x_%j.out
#SBATCH --error=err/%x_%j.err


module load modules/miniconda3
eval "$(conda shell.bash hook)"
nvidia-smi
rm -fr OUTpy

conda activate summer2
python summer.py  > OUTpy

module purge

echo "This is the end"

#!/bin/bash
#SBATCH --account=3121555
#SBATCH --partition=dsba
#SBATCH --gres=gpu:3
#SBATCH --job-name="llama_test"
#SBATCH --mem=64GB
#SBATCH --output=out/%x_%j.out
#SBATCH --error=err/%x_%j.err


module load modules/miniconda3
eval "$(conda shell.bash hook)"
nvidia-smi
rm -fr OUTpy

conda activate torch_test_3
python llama3.py > OUTpy

module purge

echo "This is the end"

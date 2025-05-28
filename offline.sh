#!/bin/bash

#SBATCH --job-name=training_data_thoughts
#SBATCH --partition=debug
#SBATCH --output=logs/training_data_thoughts.out
#SBATCH --error=logs/training_data_thoughts.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:A6000:1
#SBATCH --mem=100G

source venv/bin/activate
python3 agent.py > logs/main.out 2>logs/main.out
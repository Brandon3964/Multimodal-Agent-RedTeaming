#!/bin/bash

# Activate your virtual environment
source attack_env/bin/activate

cd attack
# Run the attack script in the background using nohup
nohup bash -c 'CUDA_VISIBLE_DEVICES=3 python test.py' > test_log.txt 2>&1 &


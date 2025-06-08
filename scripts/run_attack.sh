#!/bin/bash


export DISPLAY=:1


python3 automatic_attack.py \
    --api_key "" \
    --llm_backbone "gpt-4.1-mini" \
    --data_path "./data/attack_data/demo_data.json"


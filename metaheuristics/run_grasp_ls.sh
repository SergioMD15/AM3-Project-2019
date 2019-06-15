#!/bin/bash
for filename in config/grasp_ls/*; do
    python src/Main.py "$filename"
done

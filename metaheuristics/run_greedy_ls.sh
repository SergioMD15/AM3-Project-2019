#!/bin/bash
for filename in config/greedy_ls/*; do
    python src/Main.py "$filename"
done

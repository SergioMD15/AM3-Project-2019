#!/bin/bash
for filename in config/greedy/*; do
    python src/Main.py "$filename"
done

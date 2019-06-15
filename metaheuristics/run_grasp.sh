#!/bin/bash
for filename in config/grasp/*; do
    python src/Main.py "$filename"
done

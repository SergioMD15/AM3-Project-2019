#!/bin/bash
for filename in config/*; do
    python src/Main.py "$filename"
done

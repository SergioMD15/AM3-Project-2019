#!/bin/bash
for filename in data/*; do
    echo "$filename"
    /home/ubuntu/CPLEX/opl/bin/x86-64_linux/oplrun Model.mod "$filename"
done

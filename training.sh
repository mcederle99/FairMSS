#!/bin/bash

# Script to reproduce results

for ((i=0;i<=10;i+=1))
do
        python training.py \
        --beta $i
done
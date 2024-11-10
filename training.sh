#!/bin/bash

# Script to reproduce results
for ((s=100;s<110;s+=1))
do
  for ((c=2;c<=5;c+=1))
  do
    for ((i=0;i<=10;i+=1))
    do
            python training.py \
            --beta $i \
            --categories $c \
            --seed $s
    done
  done
done

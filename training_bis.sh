#!/bin/bash

# Script to reproduce results
for ((s=0;s<1;s+=1))
do
  for ((c=2;c<=2;c+=1))
  do
    for ((i=4;i<=7;i+=1))
    do
            python training.py \
            --beta $i \
            --categories $c \
            --seed $s
    done
  done
done

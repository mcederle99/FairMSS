#!/bin/bash

# Script to reproduce results
for ((s=1;s<4;s+=1))
do
  for ((c=3;c<=3;c+=1))
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

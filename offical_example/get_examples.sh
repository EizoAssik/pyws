#!/bin/bash
base="http://compsoc.dur.ac.uk/whitespace/"
examples=("calc.ws" "fibonacci.ws" "hanoi.ws" "hworld.ws" "name.ws")
for example in ${examples[@]}; do
    wget $base$example
done

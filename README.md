# ISE 315 – Homework 2  
## Greedy Coin Change Algorithms

This repository contains my solution for Homework 2 of ISE 315.
The purpose of this assignment is to implement and compare different greedy strategies
for the coin change problem and analyze their behavior.

## Problem Overview
Given a set of coin denominations and a target value V, the goal is to represent V using
the minimum number of coins. In this homework, I udes only greedy strategies and
these strategies does not guarantee an optimal solution.

## Implemented Greedy Strategies
- **Largest Coin First**:  
  Always selects the largest coin that does not exceed the remaining value.

- **Closest to Half**:  
  Selects the coin whose value is closest to half of the remaining amount.

- **Maximum Remainder Strategy**:  
  Chooses a coin that leaves a remainder which is divisible by the largest possible
  denomination in the coin set.

## Input Format
My program reads input from a text file.  
Each line contains a coin set and a target value in the following format: coin1,coin2,coin3 | V


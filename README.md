# 8Puzzle

## Problem Statement

The 8 puzzle problem is a puzzle invented by Noyes Palmer Chapman. It is played on a 3- by-3 grid with 8 square blocks labeled from 1 to 8 and a blank square. The goal is to rearrange the blocks so that they are in order. We are permitted to slide the blocks horizontally or vertically into the blank space. The following shows the sequence of legal moves from initial to goal position.

## Approach

### A* Search Algorithm

A* search is an algorithm that searches for the shortest path from the initial to goal node. A* search combines two evaluation functions from Greedy search algorithm and uniform cost search algorithm. h(n) is the minimized estimated cost to the goal used by greedy search and g(n) is the minimized cost of path used in uniform cost search.

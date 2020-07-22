# Semi-streaming Algorithms for Matchings
This project contains implementation of several semi-streaming algorithms for solving Bipartite Matching on Graph streams.  

## Algorithms Implemented
The following algorithms for bipartite matching from the paper **"Maximum Matching in Semi-streaming with Few Passes"** by Konrad et. al. have been implemented:
 - Greedy Algorithm
 - One Pass Derterministic Algorithm 
 - Two Pass Randomized Algorithm
 - Two Pass Deterministic Algorithm
 - Three Pass Algorithm

## How to Run the Code
This code was designed to be run on the IMDB and NotreDame_actors datasets from the SuiteSparse Matrix Collection. The following instruction assumes that you want to run the code on the IMDB dataset:

1. Download the IMDB dataset in the MatrixMarket format from the SuiteSparse Matrix Collection. 
2. Extract the content of the archive downloaded in the root directory of this repository.
3. Run `python matching.py ./IMDB/IMDB.txt` from the terminal. 
4. Various files are created in the directory `./IMDB/`, each of which contain the results for a particular algorithms.
5. For running on more number of shuffles/permutations of the stream edit the value of the variable `num_shuffles` in `matching.py`.

## Collaborators
- Mrinal Anand
- Kishen Gowda
- Vraj Patel
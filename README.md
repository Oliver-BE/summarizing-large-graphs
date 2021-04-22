# Summarizing Large Graphs with VoG
An implementation of the VoG algorithm (Vocabulary-based summarization of Graphs) developed in the 2014 research paper "Summarizing and Understanding Large Graphs" (Koutra et al.)

## Pseudocode

**Input**: Graph G(V, E)  
**Step 1**: Generate subgraphs of G using the SlashBurn graph decomposition algorithm.  
**Step 2**: Label subgraphs generated from SlashBurn as one of six of graph types from the following "vocabulary": 
> **{full clique, near clique, full bi-partite core, near bi-partite core, star, chain}**

Each subgraph **x** is first tested against each vocabulary structure type above. If a perfect match for any of the above six structures is not found, the subgraph **x** is then encoded as __*each*__ substructure and is labeled as that which results in the lowest encoding cost according to MDL.

## Getting set up
From the base directory, create your own virtual environment (running Python 3.9.0), activate it, and install the necessary package dependencies:
1. `$ python3.9 -m venv env` 
2. `$ source ./env/bin/activate`
3. `$ pip install -r ./requirements.txt`
> When done working, deactivate your virtual environment by running `$ deactivate`

> After you install a new package, add it to the `requirements.txt` file by running `$ pip3 freeze > requirements.txt`

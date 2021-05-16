# Summarizing Large Graphs with VoG
An implementation of the VoG algorithm (Vocabulary-based summarization of Graphs) developed in the 2014 research paper "Summarizing and Understanding Large Graphs" (Koutra et al.)

## Pseudocode

**Input**: Graph G(V, E)  
**Step 1**: Generate subgraphs of G using the SlashBurn graph decomposition algorithm.  
**Step 2**: Label subgraphs generated from SlashBurn as one of six of graph types from the following "vocabulary": 
> **{full clique, near clique, full bi-partite core, near bi-partite core, star, chain}**

Each subgraph **x** is first tested against each vocabulary structure type above. If a perfect match for any of the above six structures is not found, the subgraph **x** is then encoded as __*each*__ substructure and is labeled as that which results in the lowest encoding cost according to MDL.

**Step 3**: Once we have represented each subgraph **x** as one of the vocabulary structures, MDL is used to associate the candidate structure with its encoding cost and is added to the candidate set **C**.

**Step 4**: Now, given a set of candidate structures **C** and their associated encoding costs, the heuristics "Plain", "Top 10", "Top 100", and "Greedy 'N Forget" are used to select a non-redundant subset of candidate structures to represent the graph model **M**. The model of the heuristic with the lowest description cost is selected.

**Output**: A graph summary model **M** and its associated encoding cost.

## Getting set up
From the base directory, create your own virtual environment (running Python 3.9.0), activate it, and install the necessary package dependencies:
1. `$ python3.9 -m venv env` 
2. `$ source ./env/bin/activate`
3. `$ pip install -r ./requirements.txt`
> When done working, deactivate your virtual environment by running `$ deactivate`

> After you install a new package (by running `pip install <package_name>`), add it to the `requirements.txt` file by running `$ pip freeze > requirements.txt`

> Note: Make sure you run the command `export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"` so that the local Python modules get set up correctly (important for running files in the `test` directory). See [here](https://towardsdatascience.com/how-to-fix-modulenotfounderror-and-importerror-248ce5b69b1c) for more information. `PYTHONPATH` is an environment variable which you can set to add additional directories where Python will look for modules and packages.

## Running the algorithm
From the base directory, run `python3 src/main.py path_to_input_graph`. Run `python3 src/main.py -h` to see all possible configuration options.

> To run test files run `python3 test/name_of_file.py` from the base directory.

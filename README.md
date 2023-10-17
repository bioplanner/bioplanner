# Bioplanner 
Repo for BioPlanner: Automatic Evaluation of LLMs on Protocol Planning in Biology https://arxiv.org/abs/2310.10632

# Prerequisites 
- Conda (https://conda.io/projects/conda/en/latest/user-guide/install/macos.html#install-macos-silent)

# Install steps
```conda env create -f environment.yml```
```conda activate bioplanner```
```poetry install```

# Evaluation
To run an Evaluation, add a correctly filled out json file to the to_evaluate folder then run ```python src/run_evaluate.py```. The results of the evaluation will be in a json file results.json
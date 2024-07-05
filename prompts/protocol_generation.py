prompt = """You are tasked with generating pseudocode for a given protocol based on its title, description, and an admissible set of pseudofunctions. The pseudocode should correctly plan and execute the protocol steps. The evaluation will focus on the accuracy of the function calls and their arguments, as well as the correct order of the functions.

Instructions:

1. Protocol Title: Given the title of the protocol, understand the general purpose and context.
2. Protocol Description: Based on the detailed description, identify the specific steps and their sequence.
3. Admissible Pseudofunctions: Use only the provided set of pseudofunctions to construct the pseudocode.

Your output will be evaluated based on the following criteria:
- Function-Level Evaluation:
- Precision: Correctness of the functions called in the pseudocode.
- Recall: Coverage of all necessary functions.
- Levenshtein Distance (Ld): Correctness of the order of function calls.

- Argument-Level Evaluation:
- Precision: Correctness of the arguments passed to the functions.
- Recall: Coverage of all necessary arguments.
- SciBERTScore: Semantic similarity of the predicted arguments to the ground truth.
- BLEU: The similarity of the predicted arguments to the ground truth in terms of sequence.

Example:

Protocol Title: Sterilization of Lab Equipment

Protocol Description:
This protocol describes the steps to sterilize lab equipment using an autoclave. The process includes cleaning the equipment, loading it into the autoclave, running the autoclave, and ensuring the equipment is sterile.

Admissible Pseudofunctions:
1. `clean_equipment(equipment)`
2. `load_autoclave(equipment)`
3. `run_autoclave(time, temperature)`
4. `verify_sterility(equipment)`

Expected Pseudocode:
```python
clean_equipment(equipment="all")
load_autoclave(equipment="all")
run_autoclave(time="30 minutes", temperature="121C")
verify_sterility(equipment="all")
```

Your Task:
Given the following input, generate the corresponding pseudocode.

---

Input:

Protocol Title: [Insert Protocol Title]

Protocol Description: [Insert Protocol Description]

Admissible Pseudofunctions:
1. [Insert Pseudofunction 1]
2. [Insert Pseudofunction 2]
3. [Insert Pseudofunction 3]
...

Your Output:
Provide the pseudocode in the following format:
```python
# Your generated pseudocode here
```

---

Evaluation Criteria:

- Functions:
- Precision: The percentage of correctly predicted functions out of all predicted functions.
- Recall: The percentage of correctly predicted functions out of all actual functions.
- Ldn (Normalized Levenshtein Distance): The similarity between the predicted sequence of functions and the ground truth sequence. Lower values are better.

- Arguments:
- Precision: The percentage of correctly predicted function arguments out of all predicted arguments.
- Recall: The percentage of correctly predicted function arguments out of all actual arguments.
- SciBERTScore: Evaluates the similarity of the predicted arguments to the ground truth arguments.
- BLEU: Measures the quality of the text which has been machine-translated, adapted here to measure the similarity of predicted arguments to the ground truth arguments.

Example Input and Output:

Input:
```
Protocol Title: Preparation of Agar Plates

Protocol Description: This protocol describes how to prepare agar plates for bacterial culture. The process includes mixing agar powder with water, sterilizing the mixture, pouring it into Petri dishes, and allowing it to solidify.

Admissible Pseudofunctions:
1. mix_solution(ingredient, quantity, solvent)
2. sterilize_solution(solution, method, time)
3. pour_solution_into_dishes(solution, dishes)
4. allow_to_solidify(dishes, time)
```

Output:
```python
mix_solution(ingredient="agar powder", quantity="15g", solvent="1L water")
sterilize_solution(solution="agar mixture", method="autoclave", time="30 minutes")
pour_solution_into_dishes(solution="sterilized agar", dishes="Petri dishes")
allow_to_solidify(dishes="Petri dishes", time="1 hour")
```

Please generate the pseudocode for the given protocol.
"""

prompt = """You are an AI that generates python pseudocode for molecular biology protocols. This pseudocode must accurately describe a complete scientific protocol to obtain a result. You have access to a database of pseudocode functions that you can use to generate this pseudocode - you must only use these functions.

When you are generating pseudocode, you will be given a protocol title, protocol details, and the results of a database search for the most relevant pseudocode functions that could be used for this task. Your first task is to pick out the necessary functions required for the experiment from the database search results. You will then use these results to generate pseudocode for the protocol.

Here is an example of how to generate pseudocode for a molecular biology protocol.

**EXAMPLE TASK**:
TOPIC:
Cyanobacteria Trace Metal Mixture (CTMM)

DETAILS:
Preparation of the trace metal mixture for addition to seawater for the cultivation of marine cyanobacteria, Prochlorococcus and Synechococcus

DATABASE SEARCH RESULTS:
Here are the results of a database search for the most relevant pseudocode functions that could be used for this task:

def heat_vessel(vessel, temperature, time):
    pass

def adjust_volume(vessel, target_volume, solvent):
    pass

def add_ingredient(ingredient, quantity, hydrated=True, stock_volume=\"1 L\"):
    pass

def filter_solution(syringe_type, filter_size, solution_container):
    pass

def mix_solution(mixing_method, mixing_sterility_level):
    pass

def filter_solution(solution, filter_size, container, environment="laminar flow hood"):
    pass

def weigh_and_dissolve(compound, amount, flask, method, optional_heating=None):
    pass

def adjust_volume(flask, target_volume, water_type):
    pass

def work_under_sterile_conditions(sterility_level):
    pass

def dissolve_chemical(chemical, vessel, dissolve_method="inversion"):
    pass

def prepare_edta_stock(edta_quantity, final_volume, adjust_pH=True, pH_value=8.0):
    pass

def store_solution(solution, storage_conditions):
    pass

def weigh_compound(compound, amount):
    pass

def weigh_chemical(chemical, weight, weigh_paper=True):
    pass

def add_trace_metal_stocks(stock_list, target_vessel, volume_each):
    pass

def store_solution(solution, temperature):
    pass

def add_primary_trace_metals(flask, metal_list, protocol_link):
    pass

def transfer_compound(compound, to_flask, volume):
    pass

def transfer_chemical(chemical, target_vessel, volume=None):
    pass

def dissolve_compound(compound, flask, method, optional_heating=None):
    pass

def autoclave_solution(autoclave_conditions):
    pass

SELECTED FUNCTIONS:

def weigh_chemical(chemical, weight, weigh_paper=True):
    pass

def transfer_chemical(chemical, target_vessel, volume=None):
    pass

def dissolve_chemical(chemical, vessel, dissolve_method="inversion"):
    pass

def heat_vessel(vessel, temperature, time):
    pass

def add_trace_metal_stocks(stock_list, target_vessel, volume_each):
    pass

def adjust_volume(vessel, target_volume, solvent):
    pass

def filter_solution(solution, filter_size, container, environment="laminar flow hood"):
    pass

def store_solution(solution, temperature):
    pass
    
Now your try.

**YOUR TASK**:
TOPIC:
Select functions for a protocol for {title}.

DETAILS:
Here are some extra details about the protocol:

{details}

DATABASE SEARCH RESULTS:
Here are the results of a database search for the most relevant pseudocode functions that could be used for this task:

{db_results}


**YOUR RESPONSE**:
SELECTED FUNCTIONS:
"""
